from channels.exceptions import StopConsumer
from channels.generic.websocket import AsyncWebsocketConsumer
from django.http import HttpResponse
from rest_framework.decorators import api_view

video_consumers = []

chat_consumers = []


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("正在常见连接")
        await self.accept()
        chat_consumers.append(self)

    async def disconnect(self, code):
        chat_consumers.remove(self)
        raise StopConsumer()

    async def receive(self, text_data):
        print("接受消息", text_data)
        await self.send(text_data='OK')


class VideoConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("正在创建连接")
        await self.accept()
        video_consumers.append(self)
        await self.send(text_data='Connected to video stream')

    async def disconnect(self, close_code):
        video_consumers.remove(self)
        raise StopConsumer()

    async def receive(self, text_data):
        print("接收消息", text_data)
        await self.send(text_data='OK')


@api_view(['GET'])
async def send(request):
    msg = request.POST.get("msg")
    # 获取到当前所有在线客户端，即clients
    # 遍历给所有客户端推送消息
    print('request:', request)
    print('request.data:', request.POST)
    if msg:
        for consumer in chat_consumers:
            await consumer.send(msg.encode('utf-8'))
        return HttpResponse({"msg": "success"})
    else:
        HttpResponse('发送格式错误')


async def refresh():
    msg = 'refresh'
    for consumer in chat_consumers:
        await consumer.send(msg.encode('utf-8'))
    return HttpResponse('已让所有客户端刷新')
