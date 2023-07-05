from django.http import JsonResponse
from app01.models import sys_user

def login(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    if username and password:
        try:
            user = sys_user.objects.get(UserName = username)
        except:
            return JsonResponse({'loginstatus':0}, safe=False)
        if user.Password == password:
            return JsonResponse({'loginstatus':1}, safe=False)
        return JsonResponse({'loginstatus':-1}, safe=False)

def register(request):
    try:
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username and password:
            same_user = sys_user.objects.filter(UserName=username)
            if same_user.exists():
                return JsonResponse({'rigisterstatus': 0}, safe=False)
            else:
                sys_user.objects.create(UserName=username, Password=password)
    except:
        return JsonResponse({'rigisterstatus': -1}, safe=False)
    return JsonResponse({'rigisterstatus': 1}, safe=False)