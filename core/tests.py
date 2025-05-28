from django.test import TransactionTestCase
from channels.testing import WebsocketCommunicator
from channels.db import database_sync_to_async
from visionsingularity.asgi import application
from core.models import Restaurant, Table, ServiceCall

class TestWebSocketEvents(TransactionTestCase):
    async_capable = True          # Channels async tests

    def setUp(self):
        self.restaurant = Restaurant.objects.create(
            name="Test Resto", address="123 Test St", phone="123-456"
        )
        self.table = Table.objects.create(
            restaurant=self.restaurant, number=1, camera_id="cam-001"
        )

    @database_sync_to_async
    def create_call(self):
        return ServiceCall.objects.create(table=self.table, event_type="wave")

    async def test_service_call_event_broadcast(self):
        # 1. connect
        comm = WebsocketCommunicator(application, "/ws/events/")
        connected, _ = await comm.connect()
        self.assertTrue(connected)

        # 2. consume & discard the first “hello” message
        first = await comm.receive_json_from(timeout=5)
        if first.get("content"):        # rare case no greeting sent
            content_msg = first
        else:
            # 3. create model instance -> trigger signal & group_send
            await self.create_call()
            content_msg = await comm.receive_json_from(timeout=5)

        # 4. assertions on the real event payload
        content = content_msg.get("content")
        self.assertIsNotNone(content, "ServiceCall payload missing")

        self.assertEqual(content["table"], 1)
        self.assertEqual(content["event_type"], "wave")
        self.assertEqual(content["status"], "pending")

        await comm.disconnect()

