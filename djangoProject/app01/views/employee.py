import json

from django.core import serializers
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse
from rest_framework.response import Response

from app01.views.cookie import checkToken, TokenCheckFailedException
from app01.views.unjson import UnJson
from rest_framework.decorators import api_view
from app01.models import employee_info
from djangoProject.serializer import EmployeeSerializer


@api_view(['GET'])
def get_all_employee(request):
    try:
        data = UnJson(request.data)
        token = request.headers.get('Authorization')
        checkToken(token)
        page = request.GET.get('page')
        pageSize = int(request.GET.get('pageSize'))
        response = {}
        employee_list = employee_info.objects.all()
        paginator = Paginator(employee_list, pageSize)
        response['total'] = paginator.count
        try:
            employee = paginator.page(page)
        except PageNotAnInteger:
            employee = paginator.page(1)
        except EmptyPage:
            employee = paginator.page(paginator.num_pages)
        response['code'] = 200
        response['list'] = json.loads(serializers.serialize("json", employee))
        return Response(response)
    except TokenCheckFailedException as e:
        return JsonResponse(e.res, status=402)


@api_view(['POST'])
def select_employee_byname(request):
    try:
        token = request.headers.get('Authorization')
        checkToken(token)
        page = request.GET.get('page')
        pageSize = int(request.GET.get('pageSize'))
        response = {}
        data = UnJson(request.data)
        try:
            employee_list = employee_info.objects.filter(username__contains=data.username)
        except:
            return JsonResponse({'status': '该工作人员不存在'}, safe=False)
        paginator = Paginator(employee_list, pageSize)
        response['total'] = paginator.count
        try:
            employee = paginator.page(page)
        except PageNotAnInteger:
            employee = paginator.page(1)
        except EmptyPage:
            employee = paginator.page(paginator.num_pages)
        response['code'] = 200
        response['list'] = json.loads(serializers.serialize("json", employee))
        return Response(response)
    except TokenCheckFailedException as e:
        return JsonResponse(e.res, status=402)


@api_view(['POST'])
def select_employee_byidcard(request):
    try:
        token = request.headers.get('Authorization')
        checkToken(token)
        page = request.GET.get('page')
        pageSize = int(request.GET.get('pageSize'))
        response = {}
        data = UnJson(request.data)
        try:
            employee_list = employee_info.objects.filter(id_card=data.id_card)
        except:
            return JsonResponse({'status': '该工作人员不存在'}, safe=False)
        paginator = Paginator(employee_list, pageSize)
        response['total'] = paginator.count
        try:
            employee = paginator.page(page)
        except PageNotAnInteger:
            employee = paginator.page(1)
        except EmptyPage:
            employee = paginator.page(paginator.num_pages)
        response['code'] = 200
        response['list'] = json.loads(serializers.serialize("json", employee))
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
            volunteers = employee_info.objects.get(id=data.ID)
        except:
            return JsonResponse({'status': '未知错误'}, safe=False)
        volunteers.delete()
        return JsonResponse({'status': '工作人员删除成功', 'code': 200}, safe=False)
    except TokenCheckFailedException as e:
        return JsonResponse(e.res, status=402)


@api_view(['POST'])
def add_employee(request):
    try:
        data = UnJson(request.data)
        token = request.headers.get('Authorization')
        checkToken(token)
        same_volunteers = employee_info.objects.filter(id_card=data.id_card)
        if same_volunteers.exists():
            return JsonResponse({'status': '该义工已存在'}, safe=False)
        else:
            serializer = EmployeeSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({'status': '新增工作人员成功', 'code': 200}, safe=False)
            else:
                return JsonResponse({'status': '新增工作人员失败', 'code': 404}, safe=False)
    except TokenCheckFailedException as e:
        return JsonResponse(e.res, status=402)


@api_view(['POST'])
def modify_employee(request):
    try:
        data = UnJson(request.data)
        token = request.headers.get('Authorization')
        checkToken(token)
        try:
            volunteers = employee_info.objects.get(id=data.ID)
        except:
            return JsonResponse({'status': '未知错误'}, safe=False)
        serializer = EmployeeSerializer(volunteers, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({'status': '工作人员信息修改成功', 'code': 200}, safe=False)
        else:
            return JsonResponse({'status': '工作人员信息修改失败', 'code': 404}, safe=False)
    except TokenCheckFailedException as e:
        return JsonResponse(e.res, status=402)

