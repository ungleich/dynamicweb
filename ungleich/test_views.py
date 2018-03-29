# from utils.tests import BaseTestCase
# from django.conf import settings
# from django.core.urlresolvers import reverse
# from django.core.urlresolvers import resolve
# from django.utils.translation import get_language
# from django.utils.translation import activate
# from djangocms_blog.settings import get_setting
# from djangocms_blog.models import Post

# from model_mommy import mommy

# from .views import PostListViewUngleich, PostDetailViewUngleich


# class PostListViewUngleichTest(BaseTestCase):

#     DE_LANGUAGE_CODE = 'de'
#     EN_LANGUAGE_CODE = 'en-us'

#     def setUp(self):
#         super(PostListViewUngleichTest, self).setUp()
#         self.url = reverse('ungleich:post-list')
#         self.view = PostListViewUngleich
#         self.expected_template = 'djangocms_blog/post_list_ungleich.html'
#         activate(self.EN_LANGUAGE_CODE)
#         en_post_titles = ['post-title-1', 'post-title-2']
#         self.en_posts = [mommy.make(Post, title=x, publish=True) for x in en_post_titles]
#         # activate DE language in order to create DE POSTS
#         activate(self.DE_LANGUAGE_CODE)
#         de_post_titles = ['post-title-3', 'post-title-4']
#         self.de_posts = [mommy.make(Post, title=x, publish=True) for x in de_post_titles]

#         self.expected_context = {
#             'TRUNCWORDS_COUNT': get_setting('POSTS_LIST_TRUNCWORDS_COUNT'),
#             'languages': settings.LANGUAGES,
#             'current_language': get_language()

#         }

#     def test_url_resolve_to_view_correctly(self):
#         found = resolve(self.url)
#         self.assertEqual(found.func.__name__, self.view.__name__)

#     def test_queryset(self):
#         # testing EN-US Post queryset
#         activate(self.EN_LANGUAGE_CODE)
#         view = self.setup_view(self.view())
#         queryset = view.get_queryset()
#         self.assertEqual(self.en_posts, list(queryset.order_by('id')))

#         # testing DE Post queryset
#         activate(self.DE_LANGUAGE_CODE)
#         view = self.setup_view(self.view())
#         queryset = view.get_queryset()
#         self.assertEqual(self.de_posts, list(queryset.order_by('id')))

#     def test_get_context(self):
#         view = self.setup_view(self.view())
#         queryset = view.get_queryset()
#         view.object_list = queryset
#         context = view.get_context_data()
#         self.assertEqual(self.expected_context.get('current_language'),
#                          context['current_language'])


# class DetailsViewTest(BaseTestCase):

#     DE_LANGUAGE_CODE = 'de'
#     EN_LANGUAGE_CODE = 'en-us'

#     def setUp(self):
#         super(DetailsViewTest, self).setUp()
#         self.url = reverse('ungleich:post-list')
#         self.view = PostDetailViewUngleich
#         self.expected_template = 'djangocms_blog/post_detail.html'
#         self.en_post = mommy.make(Post, publish=True, title='post-title-en')
#         # activate DE language in order to create DE POSTS
#         activate(self.DE_LANGUAGE_CODE)
#         self.de_post = mommy.make(Post, publish=True, title='post-title-de')

#         self.en_post_kwargs = {
#             'slug': self.en_post.slug,
#             'year': self.en_post.date_created.year,
#             'month': self.en_post.date_created.month,
#             'day': self.en_post.date_created.day
#         }
#         self.en_post_url = reverse('ungleich:post-detail', kwargs=self.en_post_kwargs)

#         self.de_post_kwargs = {
#             'slug': self.de_post.slug,
#             'year': self.de_post.date_created.year,
#             'month': self.de_post.date_created.month,
#             'day': self.de_post.date_created.day
#         }
#         self.de_post_url = reverse('ungleich:post-detail', kwargs=self.de_post_kwargs)

#     def test_url_resolve_to_view_correctly(self):
#         found = resolve(self.en_post_url)
#         self.assertEqual(found.func.__name__, self.view.__name__)

#         found = resolve(self.de_post_url)
#         self.assertEqual(found.func.__name__, self.view.__name__)

#     def test_get_object(self):
#         # Testing get_object view method on an EN Post instance
#         activate(self.EN_LANGUAGE_CODE)
#         view = self.setup_view(self.view(), **self.en_post_kwargs)
#         obj = view.get_object()
#         self.assertEqual(self.en_post, obj)

#         # Testing get_object view method on an DE Post instance
#         activate(self.DE_LANGUAGE_CODE)
#         view = self.setup_view(self.view(), **self.de_post_kwargs)
#         obj = view.get_object()
#         self.assertEqual(self.de_post, obj)
