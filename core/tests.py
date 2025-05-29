from django.test import TransactionTestCase
from channels.testing import WebsocketCommunicator
from channels.db import database_sync_to_async
from visionsingularity.asgi import application
from core.models import Restaurant, Table, ServiceCall
from rest_framework.test import APIClient
from django.test import TransactionTestCase
from io import BytesIO
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
from unittest.mock import patch

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
        """
        This verifies that the /frames/ endpoint:
        1. accepts multipart data,
        2. does NOT require authentication,
        3. returns HTTP 202 when no gesture is detected.
        """
        # -- create a dummy 8×8 black JPEG entirely in-memory ------------
        from io import BytesIO
        from PIL import Image
        buf = BytesIO()
        Image.new("RGB", (8, 8), (0, 0, 0)).save(buf, format="JPEG")
        buf.seek(0)

        # -- POST to the endpoint ---------------------------------------
        client = APIClient()
        response = client.post(
            "/frames/",
            {
                "frame": SimpleUploadedFile("blank.jpg", buf.read(), "image/jpeg"),
                "table_id": "999",         # any fake id (view ignores for stub test)
            },
            format="multipart",
        )

        # -- EXPECT: accepted but no gesture ----------------------------
        self.assertEqual(response.status_code, 202)
        self.assertIn(response.data["status"], ["no gesture", "frame received"])


class TestGestureDetection(TransactionTestCase):
    def setUp(self):
        self.restaurant = Restaurant.objects.create(name="Cam Resto")
        self.table = Table.objects.create(restaurant=self.restaurant, number=1, camera_id="cam")

    def _dummy_frame(self):
        # put a bright pixel near top-centre to mimic “raised hand”
        img = Image.new("RGB", (64, 64), (0,0,0))
        img.putpixel((32, 4), (255,255,255))
        buf = BytesIO()
        img.save(buf, format="JPEG")
        buf.seek(0)
        return buf

    @patch("core.views.detect_gesture", return_value="raise")
    def test_raise_detected(self, _mock_detect_gesture):
        client = APIClient()
        resp = client.post(
            "/frames/",
            {"frame": SimpleUploadedFile("f.jpg", self._dummy_frame().read(), "image/jpeg"),
             "table_id": str(self.table.id)},
            format="multipart",
        )
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(resp.data["gesture"], "raise")
        self.assertEqual(ServiceCall.objects.count(), 1)

