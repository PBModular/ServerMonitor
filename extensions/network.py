# Bot stuff
from base.mod_ext import ModuleExtension
from base.module import command

# Pyrogram
from pyrogram import Client
from pyrogram.types import Message

# Libs
import platform
import cpuinfo
import psutil

AddressFamily = {
        2: "IPv4",
        10: "IPv6",
        28: "IPv6",
        17: "Link",
        18: "Link",
    }

class NetworkExtension(ModuleExtension):
    @command("netaddr")
    async def netaddr_cmd(self, bot: Client, message: Message):
        net_if_addrs = psutil.net_if_addrs()
        
        string = f"🌐  <b>{self.S['network']['network_info']}</b>\n"
        string += f"<b>{self.S['network']['address']}</b>:\n"
        for interf in net_if_addrs:
            interface = net_if_addrs[interf]
            string += f"<b>{interf}</b>\n"
            for addr in interface:
                attr = [
                    a
                    for a in dir(psutil.net_if_addrs()[interf][0])
                    if not a.startswith("__")
                    and not a.startswith("_")
                    and not callable(getattr(psutil.net_if_addrs()[interf][0], a))
                ]
                string += f"{AddressFamily[getattr(addr, 'family')]}\n"
                for item in attr[:-1]:
                    string += f"├── {item}: {getattr(addr, item)}\n"
                string += f"└── {attr[-1]}: {getattr(addr, attr[-1])}\n"
            string += "\n"

        await message.reply(
            string,
            quote=True
        )

    @command("netstats")
    async def netstats_cmd(self, bot: Client, message: Message):
        net_if_stats = psutil.net_if_stats()

        string = "🌐  <b>Network Info</b>\n" + "<b>Stats</b>:\n"
        for interf in net_if_stats:
            interface = net_if_stats[interf]
            string += f"<b>{interf}</b>\n"
            string += f"└── {interface}\n\n"

        
        await message.reply(
            string,
            quote=True
        )