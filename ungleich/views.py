from django.conf import settings
from django.http import Http404
from django.shortcuts import render
from django.views.generic import DetailView
from django.utils.translation import get_language
from djangocms_blog.models import Post
from djangocms_blog.views import PostListView
from djangocms_blog.settings import get_setting
from django.utils.translation import ugettext_lazy as _
from djangocms_blog.models import BlogCategory


def blog(request):
    posts = Post.objects.all()
    context = {
        'post_list': posts
    }

    # PostListView.base_template_name='post_list.html'
    return render(request, 'ungleich/djangocms_blog/post_list_ungleich.html', context=context)


class PostListViewUngleich(PostListView):
    category = None
    model = Post
    context_object_name = 'post_list'
    base_template_name = 'post_list_ungleich.html'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(PostListView, self).get_context_data(**kwargs)
        context['TRUNCWORDS_COUNT'] = get_setting('POSTS_LIST_TRUNCWORDS_COUNT')
        context['languages'] = settings.LANGUAGES
        context['current_language'] = get_language()

        return context

    def get_paginate_by(self, queryset):
        return get_setting('PAGINATION')

    def get_queryset(self):
        language = get_language()
        if self.category:
            blog_category = (
                BlogCategory
                ._default_manager
                .language(language)
                .filter(
                    translations__language_code=language,
                    translations__slug=self.category
                )
            )

            queryset = (self.model
                        .objects
                        .filter(categories=blog_category, publish=True)
                        .translated(language))
        else:
            queryset = (self.model
                            .objects
                            .filter(publish=True)
                            .translated(language))
        setattr(self.request, get_setting('CURRENT_NAMESPACE'), self.config)
        return queryset


class PostDetailViewUngleich(DetailView):
    model = Post
    template_name = 'ungleich/djangocms_blog/post_detail.html'
    context_object_name = 'post'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_object(self, queryset=None):

        # Use a custom queryset if provided; this is required for subclasses
        # like DateDetailView

        language = get_language()
        if queryset is None:
            queryset = self.get_queryset()
        # Next, try looking up by primary key.
        pk = self.kwargs.get(self.pk_url_kwarg)
        slug = self.kwargs.get(self.slug_url_kwarg)
        if pk is not None:
            queryset = queryset.filter(pk=pk)
        # Next, try looking up by slug.
        if slug is not None and (pk is None or self.query_pk_and_slug):
            slug_field = self.get_slug_field()
            queryset = queryset.translated(language, **{slug_field: slug})
        # If none of those are defined, it's an error.
        if pk is None and slug is None:
            raise AttributeError("Generic detail view %s must be called with "
                                 "either an object pk or a slug."
                                 % self.__class__.__name__)
        try:
            # Get the single item from the filtered queryset
            obj = queryset.first()
        except queryset.model.DoesNotExist:
            raise Http404(_("No %(verbose_name)s found matching the query") %
                          {'verbose_name': queryset.model._meta.verbose_name})
        return obj
