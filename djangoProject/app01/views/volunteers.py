from django.http import JsonResponse
from rest_framework.response import Response
from .unjson import UnJson
from rest_framework.decorators import api_view
from app01.models import volunteer_info
from djangoProject.serializer import VolunteerSerializer

@api_view(['GET'])
def get_all_volunteers(request):
    serialize = VolunteerSerializer(instance=volunteer_info.objects.all(), many=True)
    return Response(serialize.data)

@api_view(['POST'])
def select_volunteers_byname(request):
    data = UnJson(request.data)
    try:
        volunteers = volunteer_info.objects.filter(name=data.username)
    except:
        return JsonResponse({'status': '该义工不存在'}, safe=False)
    serialize = VolunteerSerializer(instance=volunteers,many=True)
    return Response(serialize.data)

@api_view(['POST'])
def delete_by_id(request):
    data = UnJson(request.data)
    try:
        volunteers = volunteer_info.objects.get(id=data.ID)
    except:
        return JsonResponse({'status': '未知错误'}, safe=False)
    volunteers.delete()
    return JsonResponse({'status': '义工删除成功'}, safe=False)

@api_view(['POST'])
def add_volunteers(request):
    data = UnJson(request.data)
    same_volunteers = volunteer_info.objects.filter(id_card=data.id_card)
    if same_volunteers.exists():
        return JsonResponse({'status': '该义工已存在'}, safe=False)
    else:
        serializer = VolunteerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({'status': '新增义工成功', 'code': 200}, safe=False)
        else:
            return JsonResponse({'status': '新增义工失败', 'code': 404}, safe=False)

@api_view(['POST'])
def modify_volunteers(request):
    data = UnJson(request.data)
    try:
        volunteers = volunteer_info.objects.get(id=data.ID)
    except:
        return JsonResponse({'status': '未知错误'}, safe=False)
    serializer = VolunteerSerializer(volunteers, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse({'status': '义工信息修改成功','code':200}, safe=False)
    else:
        return JsonResponse({'status': '义工信息修改失败', 'code': 404}, safe=False)



