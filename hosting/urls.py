from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views as hosting_views

urlpatterns = [
    url(r'index/?$', hosting_views.IndexView.as_view(), name='index'),
    url(r'django/?$', hosting_views.DjangoHostingView.as_view(), name='djangohosting'),
    url(r'nodejs/?$', hosting_views.NodeJSHostingView.as_view(), name='nodejshosting'),
    url(r'rails/?$', hosting_views.RailsHostingView.as_view(), name='railshosting'),
    url(r'pricing/?$', hosting_views.HostingPricingView.as_view(), name='pricing'),
    url(r'payment/?$', hosting_views.PaymentVMView.as_view(), name='payment'),
    url(r'orders/?$', hosting_views.OrdersHostingListView.as_view(), name='orders'),
    url(r'orders/(?P<pk>\d+)/?$', hosting_views.OrdersHostingDetailView.as_view(), name='orders'),
    url(r'cancel_order/(?P<pk>\d+)/?$', hosting_views.OrdersHostingDeleteView.as_view(), name='delete_order'),
    url(r'my-virtual-machines/?$', hosting_views.VirtualMachinesPlanListView.as_view(), name='virtual_machines'),
    url(r'my-virtual-machines/(?P<pk>\d+)/?$', hosting_views.VirtualMachineView.as_view(),
        name='virtual_machines'),
    # url(r'my-virtual-machines/(?P<pk>\d+)/delete/?$', VirtualMachineCancelView.as_view(),
        # name='virtual_machines_cancel'),
    url(r'my-virtual-machines/(?P<pk>\d+)/key/?$', hosting_views.GenerateVMSSHKeysView.as_view(),
        name='virtual_machine_key'),
    url(r'^notifications/$', hosting_views.NotificationsView.as_view(), name='notifications'),
    url(r'^notifications/(?P<pk>\d+)/?$', hosting_views.MarkAsReadNotificationView.as_view(),
        name='read_notification'),
    url(r'login/?$', hosting_views.LoginView.as_view(), name='login'),
    url(r'signup/?$', hosting_views.SignupView.as_view(), name='signup'),
    url(r'reset-password/?$', hosting_views.PasswordResetView.as_view(), name='reset_password'),
    url(r'reset-password-confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
        hosting_views.PasswordResetConfirmView.as_view(), name='reset_password_confirm'),
#    url(r'^logout/?$', 'auth_views.logout',name='logout')
       # {'next_page': '/hosting/login?logged_out=true'}, name='logout')
       url('^logout/?$', auth_views.logout, {'next_page': '/hosting/login?logged_out=true'})
]
