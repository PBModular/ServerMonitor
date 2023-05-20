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


class CPUExtension(ModuleExtension):
    @command("cpu")
    async def cpu_cmd(self, bot: Client, message: Message):
        string = "🧠  <b>CPU Info</b>\n"
        string += f"⦁ <b>Name</b>: {cpuinfo.get_cpu_info().get('brand_raw', 'Undetermined.')} ({cpuinfo.get_cpu_info()['arch_string_raw']})\n"
        string += f"⦁ <b>Count</b>: {psutil.cpu_count(logical=False)} ({psutil.cpu_count()})\n"
        # string += (f"⦁ <b>Freq</b>: {psutil.cpu_freq[0]} (max: {psutil.cpu_freq[2]} / min: {psutil.cpu_freq[1]})\n")
        string += f"⦁ <b>Flags</b>: {' '.join(cpuinfo.get_cpu_info().get('flags', 'No flags'))}\n"
        string += (
            f"⦁ <b>Load avg</b>: {psutil.loadavg[0]} {psutil.loadavg[1]} {psutil.loadavg[2]}\n"
            if hasattr(psutil, "loadavg")
            else ""
        )
        
        await message.reply(
                string,
                quote=True
            )