# Pasos para la instalación de python-django local
1. Instación de ambiente virtual python
python -r venv env
2. activación de ambiente virtual
\env\Scripts> .\activate
3. Instalación de la versión de Django
pip install django djangorestframework django-cors-headers
4. creación de proyecto django
django-admin startproject proyecto_django
5. Ingreso a la carpeta del proyecto
cd .\proyecto_django\
python manage.py startapp inicio
6. ejecutar el proyecto , validando su instalación
python manage.py runserver
-- se debe ejecutar este comando cuando se realice modificaciones dentro de settings
python manage.py migrate
--comando para ver los paquetes instalados
py -m pip freeze
--comando para instalar los paquetes necesarios
pip install -r requirements.txt