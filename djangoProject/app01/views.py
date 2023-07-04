from django.http import JsonResponse
from django.core import serializers
from app01.models import event_info

# Create your views here.

def eventinfo_all(request):
    data_list = event_info.objects.all()
    data_list_json = serializers.serialize('json', data_list)
    print(data_list_json)

    return JsonResponse(data_list_json, safe=False)
