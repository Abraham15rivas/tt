__version__ = "3.5.0"

import asyncio
import importlib
import pkgutil
from apprise import Apprise, NotifyFormat
import time
import os
import sys
import socket

import ping3
from iamlistening import Listener
from tt.config import settings, logger


async def listener():
    """Launch Listener"""

    bot_listener = Listener()
    task = asyncio.create_task(bot_listener.run_forever())
    await send_notification(await init_message())
    message_processor = MessageProcessor()
    if settings.plugin_enabled:
        message_processor.load_plugins("tt.plugins")
        loop = asyncio.get_running_loop()
        loop.create_task(start_plugins(message_processor))

    while True:
        try:
            msg = await bot_listener.get_latest_message()
            if msg:
                await parse_message(msg)
                if settings.plugin_enabled:
                    await message_processor.process_message(msg)
        except Exception as error:
            logger.error("listener: %s", error)
    await task


async def start_plugins(message_processor):
    try:
        await message_processor.start_all_plugins()
    except Exception as error:
        logger.error("plugins start: %s", error)


async def send_notification(msg):
    """💬 MESSAGING """
    try:
        if not msg:
            return
        apobj = Apprise()
        if settings.discord_webhook_id:
            url = (f"discord://{str(settings.discord_webhook_id)}/"
                f"{str(settings.discord_webhook_token)}")
            format=NotifyFormat.MARKDOWN
            if isinstance(msg, str):
                msg = msg.replace("<code>", "`")
                msg = msg.replace("</code>", "`")
        elif settings.matrix_hostname:
            url = (f"matrixs://{settings.matrix_user}:{settings.matrix_pass}@"
                f"{settings.matrix_hostname[8:]}:443/"
                f"{str(settings.bot_channel_id)}")
            format=NotifyFormat.HTML
        else:
            url = (f"tgram://{str(settings.bot_token)}/"
                f"{str(settings.bot_channel_id)}")
            format=NotifyFormat.HTML

            apobj.add(url)
        try:
            await apobj.async_notify(body=str(msg), body_format=format)
        except Exception as e:
            logger.error("%s not sent: %s", msg, e)
    except Exception as e:
        logger.error("url: %s", e)


async def parse_message(msg):
    """main parser"""

    try:
        # Initialize FindMyOrder
        # fmo = FindMyOrder()

        # Check ignore
        if msg.startswith(settings.bot_ignore):
            return
        # Check bot command
        if msg.startswith(settings.bot_prefix):
            # message = None
            command = (msg.split(" ")[0])[1:]
            if command == settings.bot_command_help:
                await send_notification(f"{await init_message()}\n{settings.bot_msg_help}")
            # elif command == settings.bot_command_trading:
            #     message = await trading_switch_command()
            # elif command == settings.bot_command_quote:
            #     symbol = msg.split(" ")[1]
            #     message = await get_quote(symbol)
            # elif command == settings.bot_command_bal:
            #     await account_balance_command()
            # elif command == settings.bot_command_pos:
            #     message = await account_position_command()
            # elif command == settings.bot_command_restart:
            #     await restart_command()
            # if message is not None:
            #     message = await get_quote(symbol)
            #     await send_notification(message)

        # # Order found
        # if settings.trading_enabled and await fmo.search(msg):
        #     # Order parsing
        #     order = await fmo.get_order(msg)
        #     # Order execution
        #     order = await execute_order(order)
        #     if order:
        #         await send_notification(order)

    except Exception as e:
        logger.error(e)

def get_host_ip() -> str:
    """Returns host IP """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((settings.ping, 80))
        ip_address = s.getsockname()[0]
        s.close()
        return ip_address
    except Exception:
        pass

def get_ping(host: str = settings.ping) -> float:
    """Returns latency """
    response_time = ping3.ping(host, unit='ms')
    time.sleep(1)
    return round(response_time, 3)


# 🦾BOT ACTIONS
async def init_message():
    version = __version__
    # try:
    #     ip = get_host_ip()
    #     ping = get_ping()
    #     exchange_name = await get_name()
    #     account_info = await get_account(exchange)
    #     start_up = f"🗿 {version}\n🕸️ {ip}\n🏓 {ping}\n💱 {exchange_name}\n🪪 {account_info}"
    # except Exception:
    start_up = f"🗿 {version}\n"
    return start_up


async def trading_switch_command():
    settings.trading_enabled = not settings.trading_enabled
    return f"Trading is {'enabled' if settings.trading_enabled else 'disabled'}."


async def restart_command():
    # Restart bot
    os.execl(sys.executable, os.path.abspath(__file__), sys.argv[0])


class MessageProcessor:
    def __init__(self):
        self.plugins = []
        self.plugin_tasks = []

    def load_plugins(self, package_name):
        logger.info("Loading plugins from package: %s", package_name)
        package = importlib.import_module(package_name)
        logger.info("Package loaded: %s", package)

        for _, plugin_name, _ in pkgutil.iter_modules(package.__path__):
            try:
                module = importlib.import_module(f"{package_name}.{plugin_name}")
                logger.info("Module loaded: %s", module)

                for name, obj in module.__dict__.items():
                    if isinstance(obj, type) and issubclass(obj, BasePlugin) and obj is not BasePlugin:
                        plugin_instance = obj()
                        self.plugins.append(plugin_instance)
                        logger.info("Plugin loaded: %s", plugin_name)

            except Exception as e:
                logger.warning("Error loading plugin %s: %s", plugin_name, e)

    async def start_plugin(self, plugin_name):
        if plugin_name in self.plugins:
            plugin_instance = self.plugins[plugin_name]
            await plugin_instance.start()
        else:
            logger.warning("Plugin not found:  %s", plugin_name)

    async def start_all_plugins(self):
        try:
            for plugin in self.plugins:
                task = asyncio.create_task(plugin.start())
                self.plugin_tasks.append(task)
            await asyncio.gather(*self.plugin_tasks)
        except Exception as e:
            logger.warning("error starting all plugins %s", e)

    async def process_message(self, message):
        plugin_dict = {plugin.name: plugin for plugin in self.plugins}
        for plugin in plugin_dict.values():
            if plugin.should_handle(message):
                await plugin.handle_message(message)


class BasePlugin:
    async def start(self):
        pass

    async def stop(self):
        pass

    async def send_notification(self, message):
        pass

    def should_handle(self, message):
        pass

    async def handle_message(self, msg):
        pass

