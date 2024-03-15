import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

print("\nIn consumer.py baby.\n")
class OrderConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("Connected")
        await self.accept()

    async def disconnect(self, close_code):
        print("Disconnected")
        pass

    async def receive(self, text_data):
        try:
            orders_data = json.loads(text_data)
            response_data = {
            'message': 'Orders data received successfully.',
            }
            # Send the response back to the client as JSON
            await self.send(text_data=json.dumps(response_data))
            
            print("Calling send_to_orders_groups function")
            # Send the orders_data to another WebSocket (ws://localhost:8000/ws/orders)
            await self.send_to_orders_group(orders_data)
        except json.JSONDecodeError:
            # Handle JSON decoding errors here
            pass
    
    async def send_to_orders_group(self, data):
        # Send the data to a group named 'orders'
        await self.channel_layer.group_add('orders', self.channel_name)
        await self.channel_layer.group_send(
            'orders',
            {
                'type': 'send_order_data',
                'data': data,
            }
        )
        # calling the OrdersGroupConsumer function from here
        # await self.send_order_data(data)


class OrdersGroupConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.channel_layer.group_add('orders', self.channel_name)

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard('orders', self.channel_name)

    async def send_order_data(self, event):
        # This method is called when data is sent to the 'orders' group
        data = event['data']
        print("\nIn send_order_data function\n")
        print(data)
        # Send a response back to the WebSocket
        response_data = {
            'message': 'Orders data received and processed.',
            'processed_data': data,  # Modify this to include the processed data
        }

        await self.send(text_data=json.dumps(response_data))
