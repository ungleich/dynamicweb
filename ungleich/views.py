from django.shortcuts import render
from django.utils.translation import get_language
from djangocms_blog.models import Post
from djangocms_blog.views import PostListView
from djangocms_blog.settings import get_setting



def blog(request):
    posts = Post.objects.all()
    print(posts)
    context = {
        'post_list': posts
    }

    # PostListView.base_template_name='post_list.html'
    return render(request, 'ungleich/djangocms_blog/post_list_ungleich.html', context=context)


class PostListViewUngleich(PostListView):
    model = Post
    context_object_name = 'post_list'
    base_template_name = 'post_list_ungleich.html'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(PostListView, self).get_context_data(**kwargs)
        context['TRUNCWORDS_COUNT'] = get_setting('POSTS_LIST_TRUNCWORDS_COUNT')
        return context

    def get_paginate_by(self, queryset):
        return get_setting('PAGINATION')

    def get_queryset(self):
        language = get_language()
        queryset = self.model.objects.translated(language)
        setattr(self.request, get_setting('CURRENT_NAMESPACE'), self.config)
        return queryset


def details(request, year, month, day, slug):
    #should be this way
    language = get_language()
    #but currently the posts are not trasnlated
    # language = 'en-us'
    post = Post.objects.translated(language, slug=slug).first()
    context = {'post': post}
    return render(request, 'ungleich/djangocms_blog/post_detail.html', context=context)

