import json

from django.core import serializers
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse
from rest_framework.response import Response

from app01.views.cookie import checkToken, TokenCheckFailedException
from app01.views.unjson import UnJson
from rest_framework.decorators import api_view
from app01.models import volunteer_info
from djangoProject.serializer import VolunteerSerializer


@api_view(['GET'])
def get_all_volunteers(request):
    try:
        token = request.headers.get('Authorization')
        checkToken(token)
        page = request.GET.get('page')
        pageSize = int(request.GET.get('pageSize'))
        response = {}
        employee_list = volunteer_info.objects.all()
        paginator = Paginator(employee_list, pageSize)
        response['total'] = paginator.count
        try:
            volunteers = paginator.page(page)
        except PageNotAnInteger:
            volunteers = paginator.page(1)
        except EmptyPage:
            volunteers = paginator.page(paginator.num_pages)
        response['code'] = 200
        response['list'] = json.loads(serializers.serialize("json", volunteers))
        return Response(response)
    except TokenCheckFailedException as e:
        return JsonResponse(e.res, status=402)


@api_view(['POST'])
def select_volunteers_byname(request):
    try:
        data = UnJson(request.data)
        token = request.headers.get('Authorization')
        checkToken(token)
        page = request.GET.get('page')
        pageSize = int(request.GET.get('pageSize'))
        response = {}
        try:
            volunteers_list = volunteer_info.objects.filter(name__contains=data.username)
        except:
            return JsonResponse({'status': '该义工不存在'}, safe=False)
        paginator = Paginator(volunteers_list, pageSize)
        response['total'] = paginator.count
        try:
            volunteers = paginator.page(page)
        except PageNotAnInteger:
            volunteers = paginator.page(1)
        except EmptyPage:
            volunteers = paginator.page(paginator.num_pages)
        response['code'] = 200
        response['list'] = json.loads(serializers.serialize("json", volunteers))
        return Response(response)
    except TokenCheckFailedException as e:
        return JsonResponse(e.res, status=402)


@api_view(['POST'])
def select_volunteers_byidcard(request):
    try:
        data = UnJson(request.data)
        token = request.headers.get('Authorization')
        checkToken(token)
        page = request.GET.get('page')
        pageSize = int(request.GET.get('pageSize'))
        response = {}
        try:
            volunteers_list = volunteer_info.objects.filter(id_card=data.id_card)
        except:
            return JsonResponse({'status': '该义工不存在'}, safe=False)
        paginator = Paginator(volunteers_list, pageSize)
        response['total'] = paginator.count
        try:
            volunteers = paginator.page(page)
        except PageNotAnInteger:
            volunteers = paginator.page(1)
        except EmptyPage:
            volunteers = paginator.page(paginator.num_pages)
        response['code'] = 200
        response['list'] = json.loads(serializers.serialize("json", volunteers))
        return Response(response)
    except TokenCheckFailedException as e:
        return JsonResponse(e.res, status=402)


@api_view(['POST'])
def delete_by_id(request):
    try:
        data = UnJson(request.data)
        token = request.headers.get('Authorization')
        checkToken(token)
        try:
            volunteers = volunteer_info.objects.get(id=data.ID)
        except:
            return JsonResponse({'status': '未知错误'}, safe=False)
        volunteers.delete()
        return JsonResponse({'status': '义工删除成功'}, safe=False)
    except TokenCheckFailedException as e:
        return JsonResponse(e.res, status=402)


@api_view(['POST'])
def add_volunteers(request):
    try:
        data = UnJson(request.data)
        token = request.headers.get('Authorization')
        checkToken(token)
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
    except TokenCheckFailedException as e:
        return JsonResponse(e.res, status=402)


@api_view(['POST'])
def modify_volunteers(request):
    try:
        data = UnJson(request.data)
        token = request.headers.get('Authorization')
        checkToken(token)
        try:
            volunteers = volunteer_info.objects.get(id=data.ID)
        except:
            return JsonResponse({'status': '未知错误'}, safe=False)
        serializer = VolunteerSerializer(volunteers, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({'status': '义工信息修改成功', 'code': 200}, safe=False)
        else:
            return JsonResponse({'status': '义工信息修改失败', 'code': 404}, safe=False)
    except TokenCheckFailedException as e:
        return JsonResponse(e.res, status=402)