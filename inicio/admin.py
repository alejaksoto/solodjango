# Register your models here.
from django.contrib import admin
from .models import Empresa
from .models import Usuario  # Reemplaza con el nombre de tu modelo

@admin.register(Empresa)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'email', 'whatsapp_id', 'telefono', 'direccion', 'fecha_creacion')
    search_fields = ('nombre', 'email', 'whatsapp_id')
    


admin.site.register(Usuario)