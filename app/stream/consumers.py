# app/stream/consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer

class StreamConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.stream_id = self.scope['url_route']['kwargs']['stream_id']
        self.stream_group_name = f'stream_{self.stream_id}'

        # Join stream group
        await self.channel_layer.group_add(
            self.stream_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave stream group
        await self.channel_layer.group_discard(
            self.stream_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']

        # Send message to stream group
        await self.channel_layer.group_send(
            self.stream_group_name,
            {
                'type': 'stream_message',
                'message': message
            }
        )

    # Receive message from stream group
    async def stream_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))
