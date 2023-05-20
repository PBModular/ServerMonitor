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


def progressbar(iteration: int, length: int) -> str:
    percent = ("{0:." + str(1) + "f}").format(100 * (iteration / float(100)))
    filledLength = int(length * iteration // 100)
    return "█" * filledLength + "▒" * (length - filledLength)


def bytes2human(n):
    # http://code.activestate.com/recipes/578019
    # >>> bytes2human(10000)
    # '9.8K'
    # >>> bytes2human(100001221)
    # '95.4M'
    symbols = ("K", "M", "G", "T", "P", "E", "Z", "Y")
    prefix = {s: 1 << (i + 1) * 10 for i, s in enumerate(symbols)}
    for s in reversed(symbols):
        if n >= prefix[s]:
            value = float(n) / prefix[s]
            return "%.1f%s" % (value, s)
    return "%sB" % n

class MemoryExtension(ModuleExtension):
    @command("ram")
    async def ram_cmd(self, bot: Client, message: Message):
        string = "🗄  <b>Memory Info</b>\n"
        string += f"<b>RAM</b>:  |{progressbar(psutil.virtual_memory().percent, 10)} <code>({bytes2human(psutil.virtual_memory().used)}/{bytes2human(psutil.virtual_memory().total)})</code>|\n"
        string += f"<b>Swap</b>: |{progressbar(psutil.swap_memory().percent, 10)} <code>({bytes2human(psutil.swap_memory().used)}/{bytes2human(psutil.swap_memory().total)})</code>|\n"

        await message.reply(
                string,
                quote=True
            )

    @command("rom")
    async def rom_cmd(self, bot: Client, message: Message):
        string = "💽  <b>Disk Info</b>\n"
        for disk in psutil.disk_partitions():
            disk_usage = psutil.disk_usage(disk.mountpoint)

            string += f"<b>{disk.device}</b>\n"
            string += f"├── <b>Mount</b> {disk.mountpoint}\n"
            string += f"├── <b>FS</b> {disk.fstype}\n"
            string += f"├── <b>Disk Usage</b> {disk_usage.percent}% ({bytes2human(disk_usage.used)}/{bytes2human(disk_usage.total)})\n"
            string += f"│       └──{progressbar(disk_usage.percent, 10)}\n"
            string += f"└── <b>Options</b> {disk.opts}\n\n"

        await message.reply(
                string,
                quote=True
            )