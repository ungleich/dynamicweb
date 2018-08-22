import logging
from django.contrib.sites.models import Site

from datacenterlight.tasks import create_vm_task
from hosting.models import HostingOrder, HostingBill, OrderDetail
from membership.models import StripeCustomer
from utils.forms import UserBillingAddressForm
from utils.models import BillingAddress
from .cms_models import CMSIntegration
from .models import VMPricing, VMTemplate

logger = logging.getLogger(__name__)


def get_cms_integration(name):
    current_site = Site.objects.get_current()
    try:
        cms_integration = CMSIntegration.objects.get(
            name=name, domain=current_site
        )
    except CMSIntegration.DoesNotExist:
        cms_integration = CMSIntegration.objects.get(name=name, domain=None)
    return cms_integration


def create_vm(billing_address_data, stripe_customer_id, specs,
              stripe_subscription_obj, card_details_dict, request,
              vm_template_id, template, user):
    billing_address = BillingAddress(
        cardholder_name=billing_address_data['cardholder_name'],
        street_address=billing_address_data['street_address'],
        city=billing_address_data['city'],
        postal_code=billing_address_data['postal_code'],
        country=billing_address_data['country']
    )
    billing_address.save()
    customer = StripeCustomer.objects.filter(id=stripe_customer_id).first()
    vm_pricing = (
        VMPricing.get_vm_pricing_by_name(name=specs['pricing_name'])
        if 'pricing_name' in specs else
        VMPricing.get_default_pricing()
    )

    final_price = (
        specs.get('total_price')
        if 'total_price' in specs
        else specs.get('price')
    )

    # Create a Hosting Order with vm_id = 0, we shall set it later in
    # celery task once the VM instance is up and running
    order = HostingOrder.create(
        price=final_price,
        customer=customer,
        billing_address=billing_address,
        vm_pricing=vm_pricing
    )

    order_detail_obj, obj_created = OrderDetail.objects.get_or_create(
        vm_template=VMTemplate.objects.get(
            opennebula_vm_template_id=vm_template_id
        ),
        cores=specs['cpu'], memory=specs['memory'], ssd_size=specs['disk_size']
    )
    order.order_detail = order_detail_obj
    order.save()

    # Create a Hosting Bill
    HostingBill.create(customer=customer, billing_address=billing_address)

    # Create Billing Address for User if he does not have one
    if not customer.user.billing_addresses.count():
        billing_address_data.update({
            'user': customer.user.id
        })
        billing_address_user_form = UserBillingAddressForm(
            billing_address_data
        )
        billing_address_user_form.is_valid()
        billing_address_user_form.save()

    # Associate the given stripe subscription with the order
    order.set_subscription_id(
        stripe_subscription_obj.id, card_details_dict
    )

    # Set order status approved
    order.set_approved()

    create_vm_task.delay(vm_template_id, user, specs, template, order.id)

    for session_var in ['specs', 'template', 'billing_address',
                        'billing_address_data', 'card_id',
                        'token', 'customer']:
        if session_var in request.session:
            del request.session[session_var]
