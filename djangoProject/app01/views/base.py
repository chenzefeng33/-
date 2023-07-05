from django.http import JsonResponse
from .unjson import UnJson
from rest_framework.decorators import api_view
from app01.models import sys_user
from djangoProject.serializer import SysUserSerializer

@api_view(['POST'])
def login(request):
    data = UnJson(request.data)
    try:
        user = sys_user.objects.get(UserName=data.username)
    except:
        return JsonResponse({'status': '该用户不存在'}, safe=False)
    if user.Password == data.Password:
        return JsonResponse({'status': '登录成功'}, safe=False)
    return JsonResponse({'status': '密码错误'}, safe=False)

@api_view(['POST'])
def register(request):
    data = UnJson(request.data)
    try:
        if data.username and data.Password:
            same_user = sys_user.objects.filter(UserName=data.username)
            if same_user.exists():
                return JsonResponse({'status': '该用户名已被占用'}, safe=False)
            else:
                sys_user.objects.create(UserName=data.username, Password=data.Password)
    except:
        return JsonResponse({'status': '未知错误'}, safe=False)
    return JsonResponse({'status': '注册成功'}, safe=False)

@api_view(['POST'])
def modify_pwd(request):
    data = UnJson(request.data)
    try:
        user = sys_user.objects.get(UserName=data.username)
    except:
        return JsonResponse({'status': '未知错误'}, safe=False)
    if data.oldPassword == user.Password:
        serializer = SysUserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({'status': '修改成功','code':200}, safe=False)
    else:
        return JsonResponse({'status': '原密码错误','code':404}, safe=False)
