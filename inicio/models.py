from django.contrib.auth.models import AbstractUser
from django.db import models

class Empresa(models.Model):
    nombre = models.CharField(max_length=255)
    identificador = models.CharField(max_length=100, unique=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.nombre


class Usuario(AbstractUser):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name="usuarios", null=True, blank=True)
    ROLES = [
        ('super_admin', 'Super Admin'),
        ('admin', 'Admin'),
        ('staff', 'Staff'),
    ]
    rol = models.CharField(max_length=50, choices=ROLES, default='staff')

    def es_super_admin(self):
        return self.rol == 'super_admin'

    def es_admin(self):
        return self.rol == 'admin'
    
    def tiene_permiso(self, permiso):
        if self.rol and permiso in self.rol.permisos:
            return self.rol.permisos[permiso]
        return False
class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

class PlantillaMensaje(models.Model):
    nombre = models.CharField(max_length=255)
    cuerpo = models.TextField()
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name="plantillas")
    es_aprobada = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    creada_por = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True)
    def clean(self):
        from django.core.exceptions import ValidationError
        import re
        
        # Validación: No terminar con parámetros
        if self.cuerpo.strip().endswith("{{"):
            raise ValidationError("La plantilla no puede finalizar con un parámetro.")
        
        # Validación: Parámetros disparejos o no secuenciales
        parametros = re.findall(r"\{\{(\d+)\}\}", self.cuerpo)
        secuencia_correcta = list(map(str, range(1, len(parametros) + 1)))
        if parametros != secuencia_correcta:
            raise ValidationError("Los parámetros deben ser secuenciales y correctos.")

        
        
class CampaniaMarketing(models.Model):
    nombre = models.CharField(max_length=255)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name="campanias")
    plantillas = models.ManyToManyField(PlantillaMensaje)
    fecha_inicio = models.DateTimeField()
    estado = models.BooleanField(default=True)

    def validar_plantilla(plantilla_texto):
        import re
        errores = []

        # Validación de llaves disparejas
        if re.search(r"\{\{[^\d]+\}\}", plantilla_texto):
            errores.append("Faltan parámetros o las llaves están disparejas.")

        # Validación de caracteres no permitidos
        if re.search(r"[#$%]", plantilla_texto):
            errores.append("Los parámetros no deben contener caracteres especiales (#, $, %).")

        # Validación de parámetros no secuenciales
        parametros = re.findall(r"\{\{(\d+)\}\}", plantilla_texto)
        secuencia_correcta = list(map(str, range(1, len(parametros) + 1)))
        if parametros != secuencia_correcta:
            errores.append("Los parámetros deben ser secuenciales.")

        return errores
