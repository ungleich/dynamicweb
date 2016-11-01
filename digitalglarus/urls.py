from django.conf.urls import url
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import views as auth_views
from . import views as digitalglarus_views
# from membership.views import LoginRegistrationView

urlpatterns = [
    url(_(r'^$'), digitalglarus_views.IndexView.as_view(), name='landing'),
    url(_(r'contact/?$'), digitalglarus_views.ContactView.as_view(), name='contact'),
    url(_(r'login/?$'), digitalglarus_views.LoginView.as_view(), name='login'),
    url(_(r'signup/?$'), digitalglarus_views.SignupView.as_view(), name='signup'),
    url(r'^logout/?$', auth_views.logout,{'next_page': '/digitalglarus/login?logged_out=true'}),
    url(r'reset-password/?$', digitalglarus_views.PasswordResetView.as_view(), name='reset_password'),
    url(r'reset-password-confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
        digitalglarus_views.PasswordResetConfirmView.as_view(), name='reset_password_confirm'),
    url(_(r'history/?$'), digitalglarus_views.HistoryView.as_view(), name='history'),
    url(_(r'users/billing_address/?$'), digitalglarus_views.UserBillingAddressView.as_view(), name='user_billing_address'),
    url(_(r'booking/?$'), digitalglarus_views.BookingSelectDatesView.as_view(), name='booking'),
    url(_(r'booking/payment/?$'), digitalglarus_views.BookingPaymentView.as_view(), name='booking_payment'),
    url(_(r'booking/orders/(?P<pk>\d+)/?$'), digitalglarus_views.OrdersBookingDetailView.as_view(),
        name='booking_orders_detail'),
    url(_(r'booking/orders/?$'), digitalglarus_views.BookingOrdersListView.as_view(),
        name='booking_orders_list'),
    url(_(r'membership/payment/?$'), digitalglarus_views.MembershipPaymentView.as_view(), name='membership_payment'),
    url(_(r'membership/activated/?$'), digitalglarus_views.MembershipActivatedView.as_view(),
        name='membership_activated'),
    url(_(r'membership/deactivate/?$'), digitalglarus_views.MembershipDeactivateView.as_view(),
        name='membership_deactivate'),
    url(_(r'membership/deactivate/success/?$'), digitalglarus_views.MembershipDeactivateSuccessView.as_view(),
        name='membership_deactivate_success'),
    url(_(r'membership/pricing/?$'), digitalglarus_views.MembershipPricingView.as_view(),
        name='membership_pricing'),
    url(_(r'membership/orders/(?P<pk>\d+)/?$'), digitalglarus_views.OrdersMembershipDetailView.as_view(),
        name='membership_orders_detail'),
    url(_(r'membership/orders/?$'), digitalglarus_views.MembershipOrdersListView.as_view(),
        name='membership_orders_list'),
    url(_(r'supporters/?$'), digitalglarus_views.supporters, name='supporters'),
    url(r'calendar_api/(?P<month>\d+)/(?P<year>\d+)?$', digitalglarus_views.CalendarApi.as_view(),name='calendar_api_1'),
    url(r'calendar_api/', digitalglarus_views.CalendarApi.as_view(),name='calendar_api'),
    url(_(r'support-us/?$'), digitalglarus_views.support, name='support'),
    url(r'^blog/(?P<slug>\w[-\w]*)/$', digitalglarus_views.blog_detail, name='blog-detail'),
    url(r'blog/$', digitalglarus_views.blog, name='blog'),
]
