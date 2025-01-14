from rest_framework import permissions

class EsAdminOStaffConPermiso(permissions.BasePermission):
    """
    Permite acceso solo a usuarios autenticados con roles específicos en la empresa.
    """

    def has_permission(self, request, view):
        # Requiere que el usuario esté autenticado y tenga el permiso adecuado
        return request.user.is_authenticated and request.user.tiene_permiso("crear_plantilla")
