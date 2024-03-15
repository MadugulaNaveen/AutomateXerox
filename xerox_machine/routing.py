# # routing.py

from django.urls import re_path,path
from accounts import consumer

# application = get_asgi_application()
print("In routing.py baby.")
websocket_urlpatterns = [
    re_path(r'ws/orders/$', consumer.OrdersGroupConsumer.as_asgi()),
    re_path(r'ws/paymentSuccessful/$', consumer.OrderConsumer.as_asgi()),
]

channel_routing = {
    'websocket.receive': consumer.OrderConsumer.receive,
    'send.order_data': consumer.OrdersGroupConsumer.send_order_data,
}
