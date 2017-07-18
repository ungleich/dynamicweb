from django.conf.urls import url
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import views as auth_views

from . import views
from .views import ContactView, IndexView, HistoryView, LoginView, SignupView,\
    PasswordResetView, PasswordResetConfirmView, MembershipPaymentView, MembershipActivatedView,\
    MembershipPricingView, BookingSelectDatesView, BookingPaymentView, OrdersBookingDetailView,\
    BookingOrdersListView, MembershipOrdersListView, OrdersMembershipDetailView, \
    MembershipDeactivateView, MembershipDeactivateSuccessView, UserBillingAddressView, EditCreditCardView, \
    MembershipReactivateView, SupportusView


# from membership.views import LoginRegistrationView

urlpatterns = [
    url(_(r'booking/payment/edit/?$'), EditCreditCardView.as_view(), name='edit_credit_card'),
    url(_(r'^$'), IndexView.as_view(), name='landing'),
    # url(_(r'new_credit_card/?$'), TermsAndConditions, name='TermsAndConditions'),
    url(_(r'support-us/?$'), SupportusView.as_view(), name='supportus'),
    url(_(r'contact/?$'), ContactView.as_view(), name='contact'),
    url(_(r'login/?$'), LoginView.as_view(), name='login'),
    url(_(r'signup/?$'), SignupView.as_view(), name='signup'),
    url(r'^logout/?$', auth_views.logout,
        {'next_page': '/digitalglarus/login?logged_out=true'}, name='logout'),
    url(r'reset-password/?$', PasswordResetView.as_view(), name='reset_password'),
    url(r'reset-password-confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
        PasswordResetConfirmView.as_view(), name='reset_password_confirm'),
    url(_(r'history/?$'), HistoryView.as_view(), name='history'),
    url(_(r'users/billing_address/?$'), UserBillingAddressView.as_view(),
        name='user_billing_address'),
    url(_(r'booking/?$'), BookingSelectDatesView.as_view(), name='booking'),
    url(_(r'booking/payment/?$'), BookingPaymentView.as_view(), name='booking_payment'),
    url(_(r'booking/orders/(?P<pk>\d+)/?$'), OrdersBookingDetailView.as_view(),
        name='booking_orders_detail'),
    # url(_(r'booking/orders/(?P<pk>\d+)/cancel/?$'), BookingCancelView.as_view(),
    #     name='booking_orders_cancel'),
    url(_(r'booking/orders/?$'), BookingOrdersListView.as_view(),
        name='booking_orders_list'),
    url(_(r'membership/payment/?$'), MembershipPaymentView.as_view(), name='membership_payment'),
    url(_(r'membership/activated/?$'), MembershipActivatedView.as_view(),
        name='membership_activated'),
    url(_(r'membership/deactivate/?$'), MembershipDeactivateView.as_view(),
        name='membership_deactivate'),
    url(_(r'membership/reactivate/?$'), MembershipReactivateView.as_view(),
        name='membership_reactivate'),
    url(_(r'membership/deactivate/success/?$'), MembershipDeactivateSuccessView.as_view(),
        name='membership_deactivate_success'),
    url(_(r'membership/pricing/?$'), MembershipPricingView.as_view(),
        name='membership_pricing'),
    url(_(r'membership/orders/(?P<pk>\d+)/?$'), OrdersMembershipDetailView.as_view(),
        name='membership_orders_detail'),
    url(_(r'membership/orders/?$'), MembershipOrdersListView.as_view(),
        name='membership_orders_list'),
    url(_(r'supporters/?$'), views.supporters, name='supporters'),
    # url(_(r'support-us/?$'), views.support, name='support'),
    url(r'^blog/(?P<slug>\w[-\w]*)/$', views.blog_detail, name='blog-detail'),
    url(r'blog/$', views.blog, name='blog'),
]
