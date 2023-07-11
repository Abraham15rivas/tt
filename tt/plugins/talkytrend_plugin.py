import os
from tt.utils import BasePlugin, send_notification
from tt.config import settings
from talkytrend import TalkyTrend

class TalkyTrendPlugin(BasePlugin):
    name = os.path.splitext(os.path.basename(__file__))[0]
    def __init__(self):
        self.enabled = settings.talkytrend_enabled
        if self.enabled:
            self.trend = TalkyTrend()

    async def start(self):
        """Starts the TalkyTrend plugin"""        
        if self.enabled:
            while True:
                async for message in self.trend.scanner():
                    await self.send_notification(message)

    async def stop(self):
        """Stops the TalkyTrend plugin"""

    async def send_notification(self, message):
        """Sends a notification"""
        if self.enabled:
            await send_notification(message)

    def should_handle(self, message):
        """Returns plugin status"""
        return self.enabled

    async def handle_message(self, msg):
        """Handles incoming messages"""
        if not self.enabled:
            return
        if msg.startswith(settings.bot_ignore):
            return
        if msg.startswith(settings.bot_prefix):
            command = (msg.split(" ")[0])[1:]
            if command == settings.bot_command_news:
                if self.trend.live_tv:
                    await self.send_notification(f"📺: {self.trend.live_tv}")
            elif command == settings.bot_command_help:
                await self.send_notification(
                    await self.exchange.get_info())
