from django.conf.urls import url
from django.contrib.auth import views as auth_views

from .views import DjangoHostingView, RailsHostingView, PaymentVMView,\
    NodeJSHostingView, LoginView, SignupView, SignupValidateView, SignupValidatedView, IndexView, \
    OrdersHostingListView, OrdersHostingDetailView, VirtualMachinesPlanListView,\
    VirtualMachineView, OrdersHostingDeleteView, NotificationsView, \
    MarkAsReadNotificationView, PasswordResetView, PasswordResetConfirmView, HostingPricingView,\
    CreateVirtualMachinesView, HostingBillListView, HostingBillDetailView, \
    SSHKeyDeleteView, SSHKeyCreateView, SSHKeyListView, SSHKeyChoiceView

urlpatterns = [
    url(r'index/?$', IndexView.as_view(), name='index'),
    url(r'django/?$', DjangoHostingView.as_view(), name='djangohosting'),
    url(r'nodejs/?$', NodeJSHostingView.as_view(), name='nodejshosting'),
    url(r'rails/?$', RailsHostingView.as_view(), name='railshosting'),
    url(r'pricing/?$', HostingPricingView.as_view(), name='pricing'),
    url(r'payment/?$', PaymentVMView.as_view(), name='payment'),
    url(r'orders/?$', OrdersHostingListView.as_view(), name='orders'),
    url(r'orders/(?P<pk>\d+)/?$', OrdersHostingDetailView.as_view(), name='orders'),
    url(r'bills/?$', HostingBillListView.as_view(), name='bills'),
    url(r'bills/(?P<pk>\d+)/?$', HostingBillDetailView.as_view(), name='bills'),
    url(r'cancel_order/(?P<pk>\d+)/?$', OrdersHostingDeleteView.as_view(), name='delete_order'),
    url(r'create_virtual_machine/?$', CreateVirtualMachinesView.as_view(), name='create_virtual_machine'),
    url(r'my-virtual-machines/?$', VirtualMachinesPlanListView.as_view(), name='virtual_machines'),
    url(r'my-virtual-machines/(?P<pk>\d+)/?$', VirtualMachineView.as_view(),
        name='virtual_machines'),
    url(r'ssh_keys/?$', SSHKeyListView.as_view(),
        name='ssh_keys'),
    url(r'ssh_keys_choice/?$', SSHKeyChoiceView.as_view(),
        name='choice_ssh_keys'),
    url(r'delete_ssh_key/(?P<pk>\d+)/?$', SSHKeyDeleteView.as_view(),
        name='delete_ssh_key'),
    url(r'create_ssh_key/?$', SSHKeyCreateView.as_view(),
        name='create_ssh_key'),
    url(r'^notifications/$', NotificationsView.as_view(), name='notifications'),
    url(r'^notifications/(?P<pk>\d+)/?$', MarkAsReadNotificationView.as_view(),
        name='read_notification'),
    url(r'login/?$', LoginView.as_view(), name='login'),
    url(r'signup/?$', SignupView.as_view(), name='signup'),
    url(r'signup-validate/?$', SignupValidateView.as_view(), name='signup-validate'),
    url(r'reset-password/?$', PasswordResetView.as_view(), name='reset_password'),
    url(r'reset-password-confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
        PasswordResetConfirmView.as_view(), name='reset_password_confirm'),
    url(r'^logout/?$', auth_views.logout,
        {'next_page': '/hosting/login?logged_out=true'}, name='logout'),
    url(r'^validate/(?P<validate_slug>.*)/$', SignupValidatedView.as_view(), name='validate')
]
