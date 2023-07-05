from rest_framework.response import Response
from rest_framework.views import APIView

from djangoProject.serializer import EventSerializer
from app01.models import event_info

class eventList(APIView):
    def get(self,request):
        serialize = EventSerializer(instance=event_info.objects.all(), many=True)
        return Response(serialize.data)