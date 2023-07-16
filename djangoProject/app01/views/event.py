import csv
from datetime import datetime

from django.http import JsonResponse
from rest_framework.decorators import api_view

from app01.models import oldperson_info
from app01.views.cookie import TokenCheckFailedException, checkToken
from app01.views.unjson import UnJson
from djangoProject.serializer import EventSerializer


@api_view(['POST'])
def add_event(request):
    try:
        data = UnJson(request.data)
        if data.type == 'fall':
            filepath = 'app01/fallEvent.csv'
        else:
            filepath = 'app01/elderSmileEvent.csv'
        token = request.headers.get('Authorization')
        checkToken(token)
        result = []
        with open(filepath, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                oldman_id = oldperson_info.objects.filter(username=row[2]).values('ID')
                if oldman_id.exists():
                    row_dict = {
                        'event_type': row[0],
                        'event_location': 'beijing',
                        'event_date': datetime.strptime(row[5], '%Y-%m-%d %H:%M:%S.%f'),
                        'event_desc': row[3],
                        'oldperson_id': int(oldman_id[0]['ID'])
                    }
                    result.append(row_dict)
                else:
                    pass
            # result = J
            serializer = EventSerializer(data=result, many=True)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({'status': '新增事件成功', 'code': 200}, safe=False)
            else:
                return JsonResponse({'status': '新增事件失败', 'code': 404, 'error': serializer.errors}, safe=False)
    except TokenCheckFailedException as e:
        return JsonResponse(e.res, status=402)

