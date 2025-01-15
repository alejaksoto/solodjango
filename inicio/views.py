import json
from multiprocessing import util
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import logging
from rest_framework import generics, status
from inicio.serializers import PlantillaMensajeSerializer
from rest_framework import generics, status
from rest_framework.response import Response
from .models import PlantillaMensaje
from .permissions import EsAdminOStaffConPermiso  # Import the permission class
from .utils import validar_plantilla, send_welcome_message
from django.views.decorators.csrf import csrf_exempt
import requests

logger = logging.getLogger(__name__)
WHATSAPP_API_TOKEN ="7850AHMCUMROS792O012092928391" 
# Vista para renderizar la página principal
# Devuelve la plantilla de la página de inicio o un error en caso de fallo.
def home(request):
    """
    Renderiza la página principal del sitio.

    :param request: Objeto HttpRequest que contiene los metadatos de la solicitud.
    :return: HttpResponse con la plantilla renderizada o mensaje de error.
    """
    try:
        return render(request, 'inicio/index.html')
    except Exception as e:
        logger.error(f"Error al renderizar la página principal: {str(e)}")
        return HttpResponse("Error interno del servidor.", status=500)

# Vista para manejar el callback embebido.
# Procesa parámetros de registro exitoso o errores.
def embedded_callback(request):
    """
    Maneja el callback embebido verificando los parámetros de registro o error.

    :param request: Objeto HttpRequest que contiene los metadatos de la solicitud.
    :return: HttpResponse con el código de registro o mensaje de error.
    """
    try:
        code = request.GET.get('code')
        error = request.GET.get('error')

        if not code and not error:
            logger.warning("Faltan parámetros obligatorios en el callback.")
            return HttpResponse("Faltan parámetros obligatorios.", status=400)

        if code:
            logger.info(f"Registro exitoso con código: {code}")
            return HttpResponse(f"Registro exitoso con código: {code}")
        elif error:
            logger.warning(f"Error en el registro: {error}")
            return HttpResponse(f"Error en el registro: {error}", status=400)
    except Exception as e:
        logger.error(f"Error inesperado en el callback embebido: {str(e)}")
        return HttpResponse("Error interno del servidor.", status=500)

# Vista para renderizar la página de inicio de sesión.
def login(request):
    """
    Renderiza la página de inicio de sesión.

    :param request: Objeto HttpRequest que contiene los metadatos de la solicitud.
    :return: HttpResponse con la plantilla de inicio de sesión.
    """
    return render(request, 'inicio/login.html')

# Vista para la verificación de WhatsApp.
# Valida el token proporcionado y responde con el reto adecuado.
def whatsapp_verify(request):
    """
    Verifica la autenticidad de las solicitudes de webhook de WhatsApp.

    :param request: Objeto HttpRequest que contiene los metadatos de la solicitud.
    :return: HttpResponse con el reto de verificación o un mensaje de error.
    """
    try:
        accessToken = "7850AHMCUMROS792O012092928391"  # Ejemplo; NO usar tokens sensibles directamente en el código.
        token = request.GET.get("hub.verify_token")
        challenge = request.GET.get("hub.challenge")
        
        if token and challenge and token == accessToken:
            return HttpResponse(challenge)

        if token == accessToken:
            logger.info("Verificación de WhatsApp exitosa.")
            return HttpResponse(challenge)
        else:
            logger.warning("Token de verificación no válido.")
            return HttpResponse("Token de verificación no válido.", status=403)
    except Exception as e:
        logger.error(f"Error inesperado en la verificación de WhatsApp: {str(e)}")
        return HttpResponse("Error interno del servidor.", status=500)

# Vista para procesar mensajes entrantes de WhatsApp y responder con el servicio GPT y utilidades adicionales.
# Esta función necesita refactorización para el manejo robusto de errores y modularidad.
#def whatsapp_message(request):
    """
    Procesa mensajes entrantes de WhatsApp y responde mediante servicios adicionales.

    :param request: Objeto HttpRequest que contiene el cuerpo del mensaje JSON.
    :return: HttpResponse indicando la recepción del evento.
    """
    try:
        body = json.loads(request.body)
        entry = body["entry"][0]
        changes = entry["changes"][0]
        value = changes["value"]
        message = value["messages"][0]
        number = message["from"]

        text = util.GetTextUser(message)
        responseChatgpt = chatgptservice.getResponse(text)

        if responseChatgpt != "error":
            data = util.TextMessage(responseChatgpt, number)
        else:
            data = util.TextMessage("Lo siento ocurrió un problema", number)

        whatsappservice.SendMessageWhatsapp(data)
        return HttpResponse("EVENT_RECEIVED")
    except Exception as e:
        logger.error(f"Error procesando mensaje de WhatsApp: {str(e)}")
        return HttpResponse("EVENT_RECEIVED")

@csrf_exempt
def whatsapp_message_handler(request):
    """
    Procesa mensajes entrantes de WhatsApp y responde con mensajes personalizados.
    """
    if request.method == "POST":
        try:
            body = json.loads(request.body.decode("utf-8"))
            entry = body.get("entry", [{}])[0]
            changes = entry.get("changes", [{}])[0]
            value = changes.get("value", {})
            messages = value.get("messages", [{}])

            if not messages:
                return JsonResponse({"status": "No messages to process"}, status=200)

            message = messages[0]
            number = message.get("from")
            text = message.get("text", {}).get("body", "Mensaje vacío")

            # Simulación de respuesta personalizada
            response_text = f"Recibimos tu mensaje: '{text}'"

            # Enviar respuesta (simulado)
            send_message_view(number, response_text)

            return JsonResponse({"status": "EVENT_RECEIVED"}, status=200)

        except Exception as e:
            logger.error(f"Error procesando mensaje de WhatsApp: {str(e)}")
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return HttpResponse("Método no permitido", status=405)

class PlantillaMensajeCreateView(generics.CreateAPIView):
    queryset = PlantillaMensaje.objects.all()
    serializer_class = PlantillaMensajeSerializer
    permission_classes = [EsAdminOStaffConPermiso]

    def get_queryset(self):
        # Filtra las plantillas por empresa del usuario autenticado
        return PlantillaMensaje.objects.filter(empresa=self.request.user.empresa)
    def create(self, request, *args, **kwargs):
        errores = validar_plantilla(request.data.get("cuerpo"))
        if errores:
            return Response({"errores": errores}, status=status.HTTP_400_BAD_REQUEST)
        return super().create(request, *args, **kwargs)
    
@csrf_exempt
def whatsapp_webhook(request):
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            object_type = body.get("object")

            if object_type == "whatsapp_business_account":
                for entry in body.get("entry", []):
                    changes = entry.get("changes", [])
                    for change in changes:
                        if change.get("field") == "messages":
                            messages = change.get("value", {}).get("messages", [])
                            if messages and messages[0].get("type") == "text":
                                from_number = messages[0].get("from")
                                phone_id = change.get("value", {}).get("metadata", {}).get("phone_number_id")

                                # Enviar mensaje de bienvenida
                                try:
                                    response = requests.post(
                                        f"https://graph.facebook.com/v17.0/{phone_id}/messages",
                                        json={
                                            "messaging_product": "whatsapp",
                                            "to": from_number,
                                            "text": {"body": "¡Hola! Bienvenido a nuestro servicio de pruebas de WhatsApp."}
                                        },
                                        headers={
                                            "Authorization": f"Bearer {WHATSAPP_API_TOKEN}",
                                            "Content-Type": "application/json"
                                        }
                                    )
                                    print("Mensaje de bienvenida enviado:", response.json())
                                except requests.RequestException as e:
                                    print("Error al enviar el mensaje:", e)

            return JsonResponse({"status": "success"})
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

    return HttpResponse("Método no permitido", status=405)

@csrf_exempt
def process_token(request):
    """
    Procesa el token recibido desde una solicitud.
    """
    if request.method == "POST":
        try:
            body = json.loads(request.body)
            code = body.get("code")

            if not code:
                return JsonResponse({"error": "Falta el código de autenticación."}, status=400)

            logger.info(f"Código recibido: {code}")

            # Simulación de generación de token de acceso
            fake_access_token = "FAKE_ACCESS_TOKEN"
            return JsonResponse({"success": True, "accessToken": fake_access_token})

        except json.JSONDecodeError:
            return JsonResponse({"error": "Formato de JSON inválido."}, status=400)
        except Exception as e:
            logger.error(f"Error procesando el token: {str(e)}")
            return JsonResponse({"error": "Error al procesar el token."}, status=500)
    else:
        return HttpResponse("Método no permitido", status=405)
def send_message_view(request):
    # Ejemplo de valores, reemplaza con los reales o dinámicos
    phone_number = "1234567890"
    phone_id = "tu_phone_id"
    api_token = "tu_api_token"

    result = send_welcome_message(phone_number, phone_id, api_token)
    
    if result["success"]:
        return JsonResponse({"message": "Mensaje enviado con éxito.", "data": result["data"]})
    else:
        return JsonResponse({"error": result["error"]}, status=400)
    
@csrf_exempt
def register_company(request):
    if request.method == "POST":
        try:
            # Decodificar el JSON del cuerpo de la solicitud
            body = json.loads(request.body)
            company_name = body.get("companyName")
            webhook_url = body.get("webhookUrl")
            phone_number = body.get("phoneNumber")

            # Validar que se reciban todos los datos necesarios
            if not company_name or not webhook_url or not phone_number:
                return JsonResponse({"error": "Faltan datos requeridos (companyName, webhookUrl o phoneNumber)."}, status=400)

            # Variables de entorno (reemplaza con tus propios valores o usa variables del entorno)
            phone_id = "453659504504003"
            api_token = "EAANFZBZCrASAQBO1zPtE901EkRoDNOU6Rfya7IEJUdJevjmD9b..."

            if not phone_id or not api_token:
                return JsonResponse({"error": "No se configuraron correctamente las credenciales para el API de WhatsApp."}, status=500)

            # Llamar a la función de envío de mensaje
            message_response = send_welcome_message(phone_number, phone_id, api_token)

            if message_response["success"]:
                return JsonResponse({
                    "message": f"La empresa '{company_name}' fue registrada exitosamente y el mensaje de bienvenida fue enviado."
                }, status=200)
            else:
                return JsonResponse({
                    "error": "La empresa fue registrada, pero hubo un error al enviar el mensaje de bienvenida.",
                    "details": message_response["error"]
                }, status=500)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Formato de JSON inválido."}, status=400)
        except Exception as e:
            print("Error en el registro:", str(e))
            return JsonResponse({"error": "Ocurrió un error en el servidor."}, status=500)
    else:
        return JsonResponse({"error": "Método no permitido."}, status=405)