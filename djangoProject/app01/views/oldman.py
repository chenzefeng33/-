from django.http import JsonResponse
from rest_framework.response import Response
from .unjson import UnJson
from rest_framework.decorators import api_view
from app01.models import oldperson_info
from djangoProject.serializer import OldPersonSerializer

@api_view(['GET'])
def get_all_oldman(request):
    serialize = OldPersonSerializer(instance=oldperson_info.objects.all(), many=True)
    return Response(serialize.data)

@api_view(['POST'])
def select_oldman_byname(request):
    data = UnJson(request.data)
    try:
        oldman = oldperson_info.objects.filter(username=data.username)
    except:
        return JsonResponse({'status': '该老人不存在'}, safe=False)
    serialize = OldPersonSerializer(instance=oldman,many=True)
    return Response(serialize.data)

@api_view(['POST'])
def delete_by_id(request):
    data = UnJson(request.data)
    try:
        oldman = oldperson_info.objects.get(ID=data.ID)
    except:
        return JsonResponse({'status': '未知错误'}, safe=False)
    oldman.delete()
    return JsonResponse({'status': '老人删除成功'}, safe=False)

@api_view(['POST'])
def add_oldman(request):
    data = UnJson(request.data)
    same_oldman = oldperson_info.objects.filter(id_card=data.id_card)
    if same_oldman.exists():
        return JsonResponse({'status': '该老人已存在'}, safe=False)
    else:
        serializer = OldPersonSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({'status': '新增老人成功', 'code': 200}, safe=False)
        else:
            return JsonResponse({'status': '新增老人失败', 'code': 404}, safe=False)

@api_view(['POST'])
def modify_oldman(request):
    data = UnJson(request.data)
    try:
        oldman = oldperson_info.objects.get(ID=data.ID)
    except:
        return JsonResponse({'status': '未知错误'}, safe=False)
    serializer = OldPersonSerializer(oldman, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse({'status': '老人信息修改成功','code':200}, safe=False)
    else:
        return JsonResponse({'status': '老人信息修改失败', 'code': 404}, safe=False)