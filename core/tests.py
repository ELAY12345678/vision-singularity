from django.test import TransactionTestCase
from channels.testing import WebsocketCommunicator
from channels.db import database_sync_to_async
from visionsingularity.asgi import application
from core.models import Restaurant, Table, ServiceCall
from rest_framework.test import APIClient
from django.test import TransactionTestCase
from io import BytesIO
from PIL import Image

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

class TestCVEndpoint(TransactionTestCase):
    def test_frame_upload_stub(self):
        # create a 1×1 dummy JPEG in-memory
        img_bytes = BytesIO()
        Image.new("RGB", (1,1)).save(img_bytes, format="JPEG")
        img_bytes.seek(0)

        client = APIClient()
        resp = client.post("/frames/",
                           {"frame": img_bytes},
                           format="multipart")
        self.assertEqual(resp.status_code, 202)
        self.assertEqual(resp.data["status"], "frame received")


