from time import sleep
from xml.etree import ElementTree

from django.conf import settings
from django.core.management.base import BaseCommand
from membership.models import StripeCustomer
from hosting.models import UserHostingKey, HostingOrder
from membership.models import CustomUser
from opennebula_api.models import OpenNebulaManager
from utils.hosting_utils import ping_ok


class Command(BaseCommand):
    help = '''Fixes issue 5509'''

    def add_arguments(self, parser):
        parser.add_argument('vm_ids', type=str)

    def handle(self, *args, **options):
        vm_ids = []
        try:
            vm_ids = [int(x) for x in options['vm_ids'].split(",")]
        except ValueError as ve:
            print(str(ve))
            exit(1)

        if not self.boolean_input(
            question="This is going to update {}. Are you "
                     "sure to continue ? (y/n)".format(options['vm_ids']),
            default=False
        ):
            print("You chose No. Hence, Not proceeding further.")
            exit(1)

        SSH_PUBLIC_KEY = settings.ONEADMIN_USER_SSH_PUBLIC_KEY
        keys_to_remove = [{'value': SSH_PUBLIC_KEY, 'state': False}]
        print("To remove:")
        print(keys_to_remove)

        for vm_id in vm_ids:
            if not self.boolean_input(
                    question="This is going to update {}. Are you "
                             "sure to continue ? (y/n)".format(vm_id),
                    default=False
            ):
                print("You chose No. Hence, Not proceeding further "
                      "with {}.".format(vm_id))
                continue
            try:
                hosting_orders = HostingOrder.objects.filter(vm_id=vm_id)
            except HostingOrder.DoesNotExist:
                print("HostingOrder for VM_ID: {} does not exiting. Not "
                      "proceeding further.".format(vm_id))
                continue

            if len(hosting_orders) > 1:
                print("More than 1 HostingOrder exist for VM_ID: {}. "
                      "Not proceeding further.".format(vm_id))
                continue
            hosting_order = hosting_orders.first()

            try:
                stripe_customers = StripeCustomer.objects.filter(
                    id=hosting_order.customer_id
                )
            except StripeCustomer.DoesNotExist:
                print("StripeCustomer for id={} does not exist. "
                      "Not proceeding further.".format(
                            hosting_order.customer_id
                        )
                )
                continue

            if len(stripe_customers) > 1:
                print("More than 1 StripeCustomer exist for VM_ID: {}. "
                      "Not proceeding further.".format(vm_id))
                continue

            stripe_customer = stripe_customers.first()
            m_user = stripe_customer.user
            on_manager = OpenNebulaManager(m_user.email, m_user.password)

            vm = on_manager.get_vm(vm_id)
            vm_ipv6 = on_manager.get_ipv6(vm_id)
            print("Processing VM_ID: {}, OWNER: {}".format(vm_id, vm.uname))

            on_manager.manage_public_key(
                keys_to_remove, hosts=[vm_ipv6]
            )
            print("Removed SSH key")
            on_manager.oneadmin_client.call('vm.action', 'poweroff',
                                                   vm_id)
            print("After call to powereoff")

            for i in range(0, 10):
                print("Waiting 10 seconds for VM to poweroff")
                sleep(10)
                vm = on_manager.get_vm(vm_id)
                if vm.str_state == "POWEROFF":
                    print("VM in POWEROFF state, so we can proceed")
                    break
                else:
                    print("VM in {} state.".format(vm.str_state))

            if vm.str_state != "POWEROFF":
                print("vm's state is {}. Not proceeding further.".format(
                    vm.str_state))
                continue

            # Find the first SSH-Key of the user
            print("Searching keys of user: {}".format(vm.uname))
            try:
                custom_user = CustomUser.objects.filter(email=vm.uname).first()
            except CustomUser.DoesNotExist:
                print(
                    "CustomUser {} does not exist. Not proceeding further.".format(
                        vm.uname))
                continue

            ukeys = UserHostingKey.objects.filter(user_id=custom_user.id)

            if len(ukeys) > 1:
                print("{} has more than 1 key".format(custom_user.email))
                key_to_set = ukeys[0].public_key
                print("Setting key {}".format(key_to_set))
            elif len(ukeys) < 1:
                print("{} does not have a key. Not proceeding further.".format(
                    custom_user.email))
                continue
            else:
                print("{} has only 1 key".format(custom_user.email))
                key_to_set = ukeys[0].public_key
                print("Setting key {}".format(key_to_set))

            tmpl = None
            for tmpl in vm.xml.iter('TEMPLATE'):
                print(ElementTree.tostring(tmpl, encoding='utf-8').decode(
                    'utf-8'))
                for ssh_key in tmpl.iter('SSH_PUBLIC_KEY'):
                    ssh_key.text = key_to_set
                    print('set ssh key')
            if tmpl is None:
                print(
                    "Not found TEMPLATE element in vm.xml. Not proceeding further.")
                continue

            xmlconfig = ElementTree.tostring(tmpl, encoding='utf-8').decode(
                'utf-8')
            print("*********")
            print(xmlconfig)
            print("*********")
            resu = on_manager.oneadmin_client.call(
                'vm.updateconf',
                vm_id,
                xmlconfig
            )

            if vm_id == resu:
                print("Ran vm.updateconf successfully")
            else:
                print("vm.updateconf not successful. Not proceeding further.")
                continue

            resu = on_manager.oneadmin_client.call('vm.action', 'resume',
                                                   vm_id)

            if vm_id == resu:
                print("Ran vm.action resume successfully")
            else:
                print(
                    "vm.action resume not successful. Not proceeding further.")
                continue

            for i in range(0, 15):
                if ping_ok(vm_ipv6):
                    print(
                        "{} is pingable. ".format(vm_ipv6)
                    )
                    break
                else:
                    print(
                        "Can't ping {}. Wait 5 secs".format(
                            vm_ipv6
                        )
                    )
                    sleep(5)

            if not ping_ok(vm_ipv6):
                print("Waited for over 75 seconds and {} is not pingable. "
                      "Not proceeding further.".format(vm_ipv6))
                continue

            print("SUCCESS {} {} {}".format(vm_id, vm.uname, vm_ipv6))
            print()
            print()
        print("Finished all VMs")

    def boolean_input(self, question, default=None):
        result = input("%s " % question)
        if not result and default is not None:
            return default
        while len(result) < 1 or result[0].lower() not in "yn":
            result = input("Please answer yes or no: ")
        return result[0].lower() == "y"
