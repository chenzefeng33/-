# from app01.views.unjson import UnJson
# import uuid
# from channels.generic.websocket import WebsocketConsumer
#
# clients = {}  # 创建客户端列表，存储所有在线客户端
# cameras = {}  # 摄像头列表
#
# class ChatConsumer(WebsocketConsumer):
#     def connect(self):
#         self.accept()
#
#     def disconnect(self, close_code):
#         pass
#
#     def receive(self, text_data):
#         """
#         接收消息
#         :param text_data: 客户端发送的消息
#         :return:
#         """
#         userid = str(uuid.uuid4())
#         data = UnJson(text_data)
#         print(data.msg)
#         # str(text_data.username, encoding="utf-8")
#         self.send("客户端链接成功：")
#
# class VideoConsumer(WebsocketConsumer):
#     def connect(self):
#         self.accept()
#
#     def disconnect(self, close_code):
#         pass
#
#     def receive(self, text_data):
#         """
#         接收消息
#         :param text_data: 客户端发送的消息
#         :return:
#         """
#         print(text_data)
#         self.send()

