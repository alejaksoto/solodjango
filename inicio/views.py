import json
from multiprocessing import util
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import logging
# Create your views here.

logger = logging.getLogger(__name__)

def home (request):
    try:
        return render(request, 'inicio/index.html')
    except Exception as e:
        logger.error(f"Error al renderizar la página principal: {str(e)}")
        return HttpResponse("Error interno del servidor.", status=500)

def embedded_callback(request):
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


def index(request):
    return render(request, 'inicio/index.html')

def whatsapp_verify(request):
    try:
        accessToken = "7850AHMCUMROS792O012092928391"
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

#def whatsapp_message(request):
    try:
        body = json.loads(request.body)
        entry = body["entry"][0]
        changes = entry["changes"][0]
        value = changes["value"]
        message = value["messages"][0]
        number = message["from"]

        text = util.GetTextUser(message)
        #responseChatgpt = chatgptservice.getResponse(text)

        if responseChatgpt != "error":
            data = util.TextMessage(responseChatgpt, number)
        else:
            data = util.TextMessage("Lo siento ocurrió un problema", number)

        whatsappservice.SendMessageWhatsapp(data)
        return HttpResponse("EVENT_RECEIVED")
    except:
        return HttpResponse("EVENT_RECEIVED")
