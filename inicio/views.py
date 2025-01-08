import json
from multiprocessing import util
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
# Create your views here.

def home (request):
    return render(request, 'inicio/index.html')

def embedded_callback(request):
    code = request.GET.get('code')
    error = request.GET.get('error')

    if code:
        return HttpResponse(f"Registro exitoso con código: {code}")
    elif error:
        return HttpResponse(f"Error en el registro: {error}")
    else:
        return HttpResponse("Callback de registro embebido desconocido.")

def index(request):
    return render(request, 'inicio/index.html')

def whatsapp_verify(request):
    try:
        accessToken = "7850AHMCUMROS792O012092928391"
        token = request.GET.get("hub.verify_token")
        challenge = request.GET.get("hub.challenge")
        if token and challenge and token == accessToken:
            return HttpResponse(challenge)
        else:
            return HttpResponse("", status=400)
    except:
        return HttpResponse("", status=400)

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
