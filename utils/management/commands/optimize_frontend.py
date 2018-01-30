import csv
import logging
import os
import re
from collections import Counter, OrderedDict
from itertools import zip_longest

from django import template
from django.conf import settings
from django.contrib.staticfiles import finders
from django.core.management.base import BaseCommand


logger = logging.getLogger(__name__)

RE_PATTERNS = {
    'view_html': '[\'\"](.*\.html)',
    'html_html': '{% (?:extends|include) [\'\"]?(.*\.html)',
    'html_style': '{% static [\'\"]?(.*\.css)',
    'css_selector': (
        '^\s*([.#\[:_A-Za-z][.#\[\]\(\)=:+~\-_A-Za-z0-9\s>,]*)'
        '{([\s\S]*?)}'
    ),
    'html_class': 'class=[\'\"]([a-zA-Z0-9-_\s]*)',
    'html_id': 'id=[\'\"]([a-zA-Z0-9-_]*)'
}


class Command(BaseCommand):
    help = 'Finds and fixes unused css styles in the templates'
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
            help='optimize only css rules in each file'
        )

    def handle(self, *args, **options):
        apps_list = options['apps']
        for app in apps_list:
            if options['css']:
                self.optimize_css(app)
            else:
                self.optimize_all(app)

    def optimize_css(self, app_name):
        # get html and css files used in the app
        files = self.get_files(app_name)
        # get_selectors_from_css
        css_selectors = self.get_selectors_css(files['style'])
        # get_selectors_from_html
        html_selectors = self.get_selectors_html(files['html'])

        # duplicate css selectors in stylesheets
        for file, selectors in css_selectors.items():
            count = {}
            for selector in selectors:
                if selector[0] in count:
                    count[selector[0]] += 1
                    print(file, selector[0], count[selector[0]])
                else:
                    count[selector[0]] = 1

    def get_files(self, app_name):
        # the view file for the app
        app_view = os.path.join(settings.PROJECT_DIR, app_name, 'views.py')
        # get template files called from the view
        all_html_list = file_match_pattern(app_view, ['view_html'])[0]
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
        print(result)
        return result

    def get_selectors_css(self, files):
        selectors = {}
        for file in files:
            if any(vendor in file for vendor in ['bootstrap', 'font-awesome']):
                continue
            result = finders.find(file)
            if result:
                selectors[file] = file_match_pattern(
                    result, ['css_selector']
                )[0]
        return selectors

    def get_selectors_html(self, files):
        selectors = {}
        for file in files:
            results = templates_match_pattern(file, ['html_class', 'html_id'])
            selectors[file] = {
                'class': results[0],
                'id': results[0],
            }
        return selectors

    def selectors_css(self, results, filename='frontend'):
        full_filename = '../optimize_' + filename + '.csv'
        output_file = os.path.join(
            settings.PROJECT_DIR, full_filename
        )
        with open(output_file, 'w', newline='') as f:
            w = csv.writer(f)
            print(zip_longest(*results))
            for r in zip_longest(*results):
                w.writerow(r)


def file_match_pattern(file, patterns):
    results = []
    with open(file) as f:
        data = f.read()
    for p in patterns:
        results.append(
            re.findall(re.compile(RE_PATTERNS[p], re.MULTILINE), data)
        )
    return results


def templates_match_pattern(template_name, patterns):
    t = template.loader.get_template(template_name)
    data = t.template.source
    results = []
    for p in patterns:
        results.append(
            re.findall(re.compile(RE_PATTERNS[p], re.MULTILINE), data)
        )
    return results


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

exempt_classes = [
    "active",
]
