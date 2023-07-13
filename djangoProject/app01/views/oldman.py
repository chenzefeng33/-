import json

from django.core import serializers
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from rest_framework.response import Response

from app01.views.cookie import checkToken, TokenCheckFailedException
from app01.views.unjson import UnJson
from rest_framework.decorators import api_view
from app01.models import oldperson_info
from djangoProject.serializer import OldPersonSerializer


@api_view(['GET'])
def get_all_oldman(request):
    try:
        data = UnJson(request.data)
        checkToken(data)
        page = request.GET.get('page')
        pageSize = int(request.GET.get('pageSize'))
        response = {}
        oldman_list = oldperson_info.objects.all()
        paginator = Paginator(oldman_list, pageSize)
        response['total'] = paginator.count
        try:
            oldman = paginator.page(page)
        except PageNotAnInteger:
            oldman = paginator.page(1)
        except EmptyPage:
            oldman = paginator.page(paginator.num_pages)
        response['code'] = 200
        response['list'] = json.loads(serializers.serialize("json", oldman))
        return Response(response)
    except TokenCheckFailedException as e:
        return JsonResponse(e.res, status=402)


@api_view(['POST'])
def select_oldman_byname(request):
    try:
        data = UnJson(request.data)
        checkToken(data)
        page = request.GET.get('page')
        pageSize = int(request.GET.get('pageSize'))
        response = {}
        try:
            oldman_list = oldperson_info.objects.filter(username__contains=data.username)
        except:
            return JsonResponse({'status': '该老人不存在'}, safe=False)
        paginator = Paginator(oldman_list, pageSize)
        response['total'] = paginator.count
        try:
            oldman = paginator.page(page)
        except PageNotAnInteger:
            oldman = paginator.page(1)
        except EmptyPage:
            oldman = paginator.page(paginator.num_pages)
        response['code'] = 200
        response['list'] = json.loads(serializers.serialize("json", oldman))
        return Response(response)
    except TokenCheckFailedException as e:
        return JsonResponse(e.res, status=402)


@api_view(['POST'])
def select_oldman_byidcard(request):
    try:
        data = UnJson(request.data)
        checkToken(data)
        page = request.GET.get('page')
        pageSize = int(request.GET.get('pageSize'))
        response = {}
        try:
            oldman_list = oldperson_info.objects.filter(id_card=data.id_card)
        except:
            return JsonResponse({'status': '该老人不存在'}, safe=False)
        paginator = Paginator(oldman_list, pageSize)
        response['total'] = paginator.count
        try:
            oldman = paginator.page(page)
        except PageNotAnInteger:
            oldman = paginator.page(1)
        except EmptyPage:
            oldman = paginator.page(paginator.num_pages)
        response['code'] = 200
        response['list'] = json.loads(serializers.serialize("json", oldman))
        return Response(response)
    except TokenCheckFailedException as e:
        return JsonResponse(e.res, status=402)


@api_view(['POST'])
def delete_by_id(request):
    try:
        data = UnJson(request.data)
        checkToken(data)
        try:
            oldman = oldperson_info.objects.get(ID=data.ID)
        except:
            return JsonResponse({'status': '未知错误'}, safe=False)
        oldman.delete()
        return JsonResponse({'status': '老人删除成功'}, safe=False)
    except TokenCheckFailedException as e:
        return JsonResponse(e.res, status=402)


@api_view(['POST'])
def add_oldman(request):
    try:
        data = UnJson(request.data)
        checkToken(data)
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
    except TokenCheckFailedException as e:
        return JsonResponse(e.res, status=402)


@api_view(['POST'])
def modify_oldman(request):
    try:
        data = UnJson(request.data)
        checkToken(data)
        try:
            oldman = oldperson_info.objects.get(ID=data.ID)
        except:
            return JsonResponse({'status': '未知错误'}, safe=False)
        serializer = OldPersonSerializer(oldman, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({'status': '老人信息修改成功', 'code': 200}, safe=False)
        else:
            return JsonResponse({'status': '老人信息修改失败', 'code': 404}, safe=False)
    except TokenCheckFailedException as e:
        return JsonResponse(e.res, status=402)