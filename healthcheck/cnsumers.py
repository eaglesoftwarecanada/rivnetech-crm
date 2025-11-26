from channels.generic.websocket import AsyncJsonWebsocketConsumer
from urllib.parse import parse_qs


class HealthCheckConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        query = parse_qs(self.scope["query_string"].decode())
        self.alias = None
        self.group_name = "healthcheck"

        if "alias" in query and query["alias"]:
            self.alias = query["alias"][0]
            self.group_name = f"healthcheck_{self.alias}"

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def healthcheck_message(self, event):
        # event["data"] is already serializer.data
        await self.send_json(event["data"])
