from .models import Dht11
from .serializers import DHT11serialize
from rest_framework.decorators import api_view
from rest_framework import generics
from rest_framework.response import Response
from django.core.mail import send_mail
from django.conf import settings

from .utils import send_telegram, send_whatsapp_alert


# from .utils import send_telegram

@api_view(['GET'])
def Dlist(request):
    all_data = Dht11.objects.all()
    data = DHT11serialize(all_data, many=True).data
    return Response({'data': data})

class Dhtviews(generics.CreateAPIView):
    queryset = Dht11.objects.all()
    serializer_class = DHT11serialize

    def perform_create(self, serializer):
        instance = serializer.save()
        temp = instance.temp

        if temp > 25:
            # 1) Email (si tu veux le garder)
            try:
                send_mail(
                    subject="⚠️ Alerte Température élevée (Saad Eddine ELKADIRI,Mohammed EL MIR)",
                    message=f"Nous sommes le binôme Saad Eddine ELKADIRI et Mohammed EL MIR. "
                            f"La température a atteint {temp:.1f} °C à {instance.dt}.",
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=["iliass.elaissaoui14159@gmail.com"],
                    fail_silently=False,  # pour que l'erreur soit levée
                )
                print("✅ Email sent successfully!")
            except Exception as e:
                print(f"❌ Failed to send email: {e}")

            # 2) Telegram (optionnel)
            # msg = f"⚠️ Alerte DHT11: {temp:.1f} °C (>25) à {instance.dt}"
            # send_telegram(msg)
            msg = f"⚠️ Alerte DHT11: {temp:.1f} °C (>25) à {instance.dt}"
            send_telegram(msg)

            whatsapp_phone = "+212617555751"  # recipient number with country code
            msg = f"⚠️ Alerte DHT11: Température {temp:.1f} °C à {instance.dt}"
            send_whatsapp_alert(whatsapp_phone, msg)