# inicio/utils.py
def validar_plantilla(plantilla):
    # Lógica de validación aquí
    pass

import requests

def send_welcome_message(phone_number, phone_id, api_token):
    url = f"https://graph.facebook.com/v17.0/{phone_id}/messages"
    payload = {
        "messaging_product": "whatsapp",
        "to": phone_number,
        "type": "text",
        "text": {"body": "Hola, este es un mensaje de master desde la API de WhatsApp."},
    }
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json",
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()  # Verifica si hubo un error HTTP
        return {"success": True, "data": response.json()}
    except requests.RequestException as e:
        print("Error al enviar el mensaje de bienvenida:", e)
        return {"success": False, "error": str(e)}

def get_chatgpt_response(text):
    # Simulación de una llamada a un servicio de IA (como ChatGPT)
    # Aquí puedes integrar tu lógica real
    return f"Respuesta simulada para: {text}" if text else "Mensaje vacío."

def create_text_message(response_text, number):
    # Crea un objeto de mensaje compatible con la API de WhatsApp
    return {
        "messaging_product": "whatsapp",
        "to": number,
        "type": "text",
        "text": {"body": response_text}
    }