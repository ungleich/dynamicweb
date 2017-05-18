from django.db import models


class BetaAccessVMType(models.Model):
    ssd = models.IntegerField()
    ram = models.IntegerField()
    cpu = models.IntegerField()
    price = models.FloatField()

    def __str__(self):
        return "ID: %s - SSD %s - RAM %s - CPU %s - Price %s " % \
            (self.id, str(self.ssd), self.ram, self.cpu, self.price)


class BetaAccess(models.Model):
    email = models.CharField(max_length=250)
    name = models.CharField(max_length=250)
    # vm = models.ForeignKey(BetaAccessVM)

    def __str__(self):
        vms = self.betaaccessvm_set.all()
        rep = "Email: %s " % self.email
        for vm in vms:
            rep += "(vm:%s - amount:%s) - " % (vm.type.id, vm.amount)
        return rep


class BetaAccessVM(models.Model):
    type = models.ForeignKey(BetaAccessVMType)
    access = models.ForeignKey(BetaAccess)
    amount = models.IntegerField()

    @classmethod
    def create(cls, data):
        VM_KEY_ID = 0
        VM_AMOUNT = 1
        ZERO = 0
        email = data.get('email')
        beta_access = BetaAccess.objects.create(email=email)
        vm_data = [(key, value) for key, value in data.items() if 'vm' in key]
        created_vms = []
        for vm in vm_data:
            if int(vm[VM_AMOUNT]) == ZERO:
                continue
            vm_id = vm[VM_KEY_ID].split('-').pop()
            vm_type = BetaAccessVMType.objects.get(id=vm_id)
            created_vms.append(cls.objects.create(access=beta_access,
                                                  amount=vm[VM_AMOUNT], type=vm_type))

        return created_vms
