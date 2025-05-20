from twilio.rest import Client
import os

# Obtenha essas variáveis da sua conta Twilio
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_NUMBER = "whatsapp:+14155238886"  # número do sandbox Twilio
DESTINO = "whatsapp:+5581992429403"  # substitua por seu número com DDI, ex: +5581999999999

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

def enviar_mensagem_whatsapp(nome_cliente=""):
    try:
        message = client.messages.create(
            from_=TWILIO_WHATSAPP_NUMBER,
            body=f"Olá {nome_cliente or 'cliente'}, sua solicitação foi recebida com sucesso! Em breve entraremos em contato com sua proposta. ✈️",
            to=DESTINO
        )
        print("Mensagem enviada! SID:", message.sid)
    except Exception as e:
        print("Erro ao enviar mensagem:", str(e))
        
        if __name__ == "__main__":
            print("Enviando mensagem para o WhatsApp...")
            enviar_mensagem_whatsapp("Flávio")
