import os
from tt.utils import BasePlugin, send_notification, __version__
from tt.config import logger, settings
import socket
import ping3

class HelperPlugin(BasePlugin):
    name = os.path.splitext(os.path.basename(__file__))[0]
    def __init__(self):
        try:
            self.enabled = settings.helper_enabled
            if self.enabled:
                self.version = f"🗿 {__version__}\n"
                self.latency = ping3.ping(settings.ping, unit='ms') 
                #round(response_time, 3)
                self.host_ip = self.get_host_ip()
                self.help_message = settings.bot_msg_help
        except Exception as error:
            logger.warning(error)

    async def start(self):
        """Starts the plugin"""
        try:           
            if self.enabled:
                pass
        except Exception as error:
            logger.warning(error)
    
    async def stop(self):
        """Stops the plugin"""
        try:           
            if self.enabled:
                pass
        except Exception as error:
            logger.warning(error)

    async def send_notification(self, message):
        """Sends a notification"""
        try:           
            if self.enabled:
                await send_notification(message)
        except Exception as error:
            logger.warning(error)

    def should_handle(self, message):
        """Returns True if the plugin should handle incoming message"""
        return self.enabled

    async def handle_message(self, msg):
        """Handles incoming messages"""
        try:           
            if self.enabled:
                if msg == f"{settings.bot_prefix}{settings.bot_command_help}":
                    await self.send_notification(
                        self.version+self.help_message)
        except Exception as error:
            logger.warning(error)

    def get_host_ip(self):
        """Returns host IP """
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect((settings.ping, 80))
            ip_address = s.getsockname()[0]
            s.close()
            return ip_address
        except Exception:
            pass
