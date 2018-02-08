"""
This command finds and creates a report for all the usage of css rules in
an app. It aims to optimize existing codebase as well as assist the frontend
developer when designing new components by avoiding unnecessary duplication and
suggesting more/optimal alternatives.

Features:
    Currently the command can find out and display:
        - Media Breakpoints used in a stylesheet
        - Duplicate selectors in a stylesheet
        - Unused selectors
    Work in progress to enable these features:
        - Duplicate style declaration for same selector
        - DOM validation
        - Finding out dead styles (those that are always cancelled)
        - Optimize media declarations

Example:
    $ python manage.py optimize_frontend datacenterlight
    above command produces a file ../optimize_frontend.html which contains a
    report with the above mentioned features
"""

# import csv
import json
import logging
import os
import re
from collections import Counter, OrderedDict
# from itertools import zip_longest

from django import template
from django.conf import settings
from django.contrib.staticfiles import finders
from django.core.management.base import BaseCommand


logger = logging.getLogger(__name__)

RE_PATTERNS = {
    'view_html': '[\'\"](.*\.html)',
    'html_html': '{% (?:extends|include) [\'\"]?(.*\.html)',
    'html_style': '{% static [\'\"]?(.*\.css)',
    'css_media': (
        '^\s*\@media([^{]+)\{\s*([\s\S]*?})\s*}'
    ),
    'css_selector': (
        '^\s*([.#\[:_A-Za-z][^{]*?)\s*'
        '\s*{([\s\S]*?)\s*}'
    ),
    'html_class': 'class=[\'\"]([a-zA-Z0-9-_\s]*)',
    'html_id': 'id=[\'\"]([a-zA-Z0-9-_]*)'
}


class Command(BaseCommand):
    help = (
        'Finds unused and duplicate style declarations from the stylesheets '
        'used in the templates of each app'
    )
    requires_system_checks = False

    def add_arguments(self, parser):
        # positional arguments
        parser.add_argument(
            'apps', nargs='+', type=str,
            help='name of the apps to be optimized'
        )

        # Named (optional) arguments
        parser.add_argument(
            '--together',
            action='store_true',
            help='optimize the apps together'
        )
        parser.add_argument(
            '--css',
            action='store_true',
            help='optimize only the css rules declared in each stylesheet'
        )

    def handle(self, *args, **options):
        apps_list = options['apps']
        report = {}
        for app in apps_list:
            if options['css']:
                report[app] = self.optimize_css(app)
        # write report
        write_report(report)

    def optimize_css(self, app_name):
        """Optimize declarations inside a css stylesheet

        Args:
            app_name (str): The application name
        """
        # get html and css files used in the app
        files = get_files(app_name)
        # get_selectors_from_css
        css_selectors = get_selectors_css(files['style'])
        # get_selectors_from_html
        html_selectors = get_selectors_html(files['html'])
        report = {
            'css_dup': get_css_duplication(css_selectors),
            'css_unused': get_css_unused(css_selectors, html_selectors)
        }
        return report


def get_files(app_name):
    """Get all the `html` and `css` files used in an app.

    Args:
        app_name (str): The application name

    Returns:
        dict: A dictonary containing Counter of occurence of each
        html and css file in `html` and `style` fields respectively.
        For example:
        {
            'html': {'datacenterlight/success.html': 1},
            'style': {'datacenterlight/css/bootstrap.min.css': 2}
        }
    """
    # the view file for the app
    app_view = os.path.join(settings.PROJECT_DIR, app_name, 'views.py')
    # get template files called from the view
    all_html_list = file_match_pattern(app_view, 'view_html')
    # list of unique template files
    uniq_html_list = list(OrderedDict.fromkeys(all_html_list).keys())
    # list of stylesheets
    all_style_list = []
    file_patterns = ['html_html', 'html_style']
    # get html and css files called from within templates
    i = 0
    while i < len(uniq_html_list):
        template_name = uniq_html_list[i]
        try:
            # a dict containing 'html' and 'css' files
            temp_files = templates_match_pattern(
                template_name, file_patterns
            )
        except template.exceptions.TemplateDoesNotExist as e:
            print("template file not found: ", str(e))
            all_html_list = [
                h for h in all_html_list if h != template_name
            ]
            del uniq_html_list[i]
        else:
            all_html_list.extend(temp_files[0])
            uniq_html_list = list(
                OrderedDict.fromkeys(all_html_list).keys()
            )
            all_style_list.extend(temp_files[1])
            i += 1
    # counter dict for the html files called from view
    result = {
        'html': Counter(all_html_list),
        'style': Counter(all_style_list)
    }
    # print(result)
    return result


def get_selectors_css(files):
    """Gets the selectors and declarations from a stylesheet.

    Args:
        files (list): A list of path of stylesheets.

    Returns:
        dict: A nested dictionary with the structre as
        `{'file': {'media-selector': [('selectors',`declarations')]}}`
        For example:
        {
            'datacenterlight/css/landing-page.css':{
                '(min-width: 768px)': [
                    ('.lead-right', 'text-align: right;'),
                ]
            }
        }
    """
    selectors = {}
    media_selectors = {}
    # get media selectors and other simple declarations
    for file in files:
        if any(vendor in file for vendor in ['bootstrap', 'font-awesome']):
            continue
        result = finders.find(file)
        if result:
            with open(result) as f:
                data = f.read()
            media_selectors[file] = string_match_pattern(data, 'css_media')
            new_data = string_remove_pattern(data, 'css_media')
            default_match = string_match_pattern(new_data, 'css_selector')
            selectors[file] = {
                'default': [
                    [' '.join(grp.split()) for grp in m] for m in default_match
                ]
            }
    # get declarations from media queries
    for file, match_list in media_selectors.items():
        for match in match_list:
            query = match[0]
            block_text = ' '.join(match[1].split())
            results = string_match_pattern(
                block_text, 'css_selector'
            )
            f_query = ' '.join(query.replace(':', ': ').split())
            if f_query in selectors[file]:
                selectors[file][f_query].extend(results)
            else:
                selectors[file][f_query] = results
    return selectors


def get_selectors_html(files):
    """Get `class` and `id` used in html files.

    Args:
        files (list): A list of html files path.

    Returns:
        dict: a dictonary of all the classes and ids found in the file, in
        `class` and `id` field respectively.
    """
    selectors = {}
    for file in files:
        results = templates_match_pattern(file, ['html_class', 'html_id'])
        class_dict = {c: 1 for match in results[0] for c in match.split()}
        selectors[file] = {
            'classes': list(class_dict.keys()),
            'ids': results[1],
        }
    return selectors


def file_match_pattern(file, patterns):
    """Match a regex pattern in a file

    Args:
        file (str): Complete path of file
        patterns (list or str): The pattern(s) to be searched in the file

    Returns:
        list: A list of all the matches in the file. Each item is a list of
        all the captured groups in the pattern. If multiple patterns are given,
        the returned list is a list of such lists.
        For example:
        [('.lead', 'font-size: 18px;'), ('.btn-lg', 'min-width: 180px;')]
    """
    with open(file) as f:
        data = f.read()
    results = string_match_pattern(data, patterns)
    return results


def string_match_pattern(data, patterns):
    """Match a regex pattern in a string

    Args:
        data (str): the string to search for the pattern
        patterns (list or str): The pattern(s) to be searched in the file

    Returns:
        list: A list of all the matches in the string. Each item is a list of
        all the captured groups in the pattern. If multiple patterns are given,
        the returned list is a list of such lists.
        For example:
        [('.lead', 'font-size: 18px;'), ('.btn-lg', 'min-width: 180px;')]
    """
    if not isinstance(patterns, str):
        results = []
        for p in patterns:
            re_pattern = re.compile(RE_PATTERNS[p], re.MULTILINE)
            results.append(re.findall(re_pattern, data))
    else:
        re_pattern = re.compile(RE_PATTERNS[patterns], re.MULTILINE)
        results = re.findall(re_pattern, data)
    return results


def string_remove_pattern(data, patterns):
    """Remove a pattern from a string

    Args:
        data (str): the string to search for the patter
        patterns (list or str): The pattern(s) to be removed from the file

    Returns:
        str: The new string with all instance of matching pattern
        removed from it
    """
    if not isinstance(patterns, str):
        for p in patterns:
            re_pattern = re.compile(RE_PATTERNS[p], re.MULTILINE)
            data = re.sub(re_pattern, '', data)
    else:
        re_pattern = re.compile(RE_PATTERNS[patterns], re.MULTILINE)
        data = re.sub(re_pattern, '', data)
    return data


def templates_match_pattern(template_name, patterns):
    """Match a regex pattern in the first found template file

    Args:
        file (str): Path of template file
        patterns (list or str): The pattern(s) to be searched in the file

    Returns:
        list: A list of all the matches in the file. Each item is a list of
        all the captured groups in the pattern. If multiple patterns are given,
        the returned list is a list of such lists.
        For example:
        [('.lead', 'font-size: 18px;'), ('.btn-lg', 'min-width: 180px;')]
    """
    t = template.loader.get_template(template_name)
    data = t.template.source
    results = string_match_pattern(data, patterns)
    return results


def get_css_duplication(css_selectors):
    """Get duplicate selectors from the same stylesheet

    Args:
        css_selectors (dict): A dictonary containing css selectors from
        all the files in the app in the below structure.
        `{'file': {'media-selector': [('selectors',`declarations')]}}`

    Returns:
        dict: A dictonary containing the count of any duplicate selector in
        each file.
        `{'file': {'media-selector': {'selector': count}}}`
    """
    # duplicate css selectors in stylesheets
    rule_count = {}
    for file, media_selectors in css_selectors.items():
        rule_count[file] = {}
        for media, rules in media_selectors.items():
            rules_dict = Counter([rule[0] for rule in rules])
            dup_rules_dict = {k: v for k, v in rules_dict.items() if v > 1}
            if dup_rules_dict:
                rule_count[file][media] = dup_rules_dict
    return rule_count


def get_css_unused(css_selectors, html_selectors):
    """Get selectors from stylesheets that are not used in any of the html
    files in which the stylesheet is used.

    Args:
        css_selectors (dict): A dictonary containing css selectors from
        all the files in the app in the below structure.
        `{'file': {'media-selector': [('selectors',`declarations')]}}`
        html_selectors (dict): A dictonary containing the 'class' and 'id'
        declarations from all html files
    """
    with open('utils/optimize/test.json', 'w') as f:
        json.dump([html_selectors, css_selectors], f, indent=4)
    # print(html_selectors, css_selectors)


def write_report(all_reports, filename='frontend'):
    """Write the generated report to a file for re-use

    Args;
        all_reports (dict): A dictonary of report obtained from different tests
        filename (str): An optional suffix for the output file
    """
    full_filename = 'utils/optimize/optimize_' + filename + '.html'
    output_file = os.path.join(
        settings.PROJECT_DIR, full_filename
    )
    with open('utils/optimize/op_frontend.json', 'w') as f:
        json.dump(all_reports, f, indent=4)
    with open(output_file, 'w', newline='') as f:
        f.write(
            template.loader.render_to_string(
                'utils/report.html', {'all_reports': all_reports}
            )
        )
        # w = csv.writer(f)
        # print(zip_longest(*results))
        # for r in zip_longest(*results):
        #     w.writerow(r)


# a list of all the html tags (to be moved in a json file)
html_tags = [
    "a",
    "abbr",
    "address",
    "article",
    "area",
    "aside",
    "audio",
    "b",
    "base",
    "bdi",
    "bdo",
    "blockquote",
    "body",
    "br",
    "button",
    "canvas",
    "caption",
    "cite",
    "code",
    "col",
    "colgroup",
    "datalist",
    "dd",
    "del",
    "details",
    "dfn",
    "div",
    "dl",
    "dt",
    "em",
    "embed",
    "fieldset",
    "figcaption",
    "figure",
    "footer",
    "form",
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "head",
    "header",
    "hgroup",
    "hr",
    "html",
    "i",
    "iframe",
    "img",
    "input",
    "ins",
    "kbd",
    "keygen",
    "label",
    "legend",
    "li",
    "link",
    "map",
    "mark",
    "menu",
    "meta",
    "meter",
    "nav",
    "noscript",
    "object",
    "ol",
    "optgroup",
    "option",
    "output",
    "p",
    "param",
    "pre",
    "progress",
    "q",
    "rp",
    "rt",
    "ruby",
    "s",
    "samp",
    "script",
    "section",
    "select",
    "source",
    "small",
    "span",
    "strong",
    "style",
    "sub",
    "summary",
    "sup",
    "textarea",
    "table",
    "tbody",
    "td",
    "tfoot",
    "thead",
    "th",
    "time",
    "title",
    "tr",
    "u",
    "ul",
    "var",
    "video",
    "wbr"
]
