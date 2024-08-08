import os
from django.conf import settings
import pywhatkit as kit

def send_image_message(telefone_completo, image, message_body, call_hour, call_minute, wait_time):
    try:
        image_path = os.path.join(settings.MEDIA_ROOT, image.name)
        with open(image_path, 'wb+') as destination:
            for chunk in image.chunks():
                destination.write(chunk)
        kit.sendwhats_image(
            telefone_completo,
            image_path,
            message_body,
            call_hour,
            call_minute,
            wait_time
        )
    except Exception as e:
        raise Exception(f'Erro ao enviar imagem: {e}')
