from channels.generic.websocket import AsyncWebsocketConsumer
import json

class EventConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("waiters_group", self.channel_name)
        await self.accept()
        await self.send(json.dumps({"message": "WebSocket connection established!"}))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("waiters_group", self.channel_name)

    async def send_service_call(self, event):
        await self.send(text_data=json.dumps(event["content"]))