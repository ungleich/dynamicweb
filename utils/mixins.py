# coding=utf-8
from guardian.shortcuts import assign_perm


class AssignPermissionsMixin(object):
    permissions = tuple()
    user = None
    obj = None
    kwargs = dict()

    def assign_permissions(self, user):
        for permission in self.permissions:
            assign_perm(permission, user, self)

    # def save(self, *args, **kwargs):
    #     self.kwargs = kwargs
    #     self.get_objs()

    #     create = False
    #     if not self.pk:
    #         create = True

    #     super(AssignPermissionsMixin, self).save(*args, **kwargs)

    #     if create:
    #         self.assign_permissions()

    # def get_objs(self):
    #     self.user = self.kwargs.pop('user', None)
    #     self.obj = self.kwargs.pop('obj', None)
    #     assert self.user, 'Se necesita el parámetro user para poder asignar los permisos'
    #     assert self.obj, 'Se necesita el parámetro obj para poder asignar los permisos'
