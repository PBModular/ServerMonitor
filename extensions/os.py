# Bot stuff
from base.mod_ext import ModuleExtension
from base.module import command

# Pyrogram
from pyrogram import Client
from pyrogram.types import Message

# Python libs
from os.path import exists
import datetime

# Libs
import platform
import cpuinfo
import psutil

backslash = "\n"
returnslash = "\r"

def get_os_release():
        if not exists("/etc/os-release"):
            return False

        list_ = []
        with open("/etc/os-release") as f:
            list_.extend(item.split("=") for item in f.readlines())
        return {item[0]: item[1].replace(backslash, "").replace('"', "") for item in list_}
    
# https://stackoverflow.com/questions/2756737/check-linux-distribution-name
def get_distro():
    """
    Name of your Linux distro
    """
    if not exists("/etc/issue"):
        return False

    with open("/etc/issue") as f:
        return f.read().split()[0]

os_release = get_os_release()

class OSExtension(ModuleExtension):

    @command("distro")
    async def distro_cmd(self, bot: Client, message: Message):
        string = f"""🐧  <b>Linux Info</b>
        <b>Name:</b> {get_distro()}
        <b>Kernel:</b> {platform.release()}
        <b>Hostname:</b> {platform.node()}
        <b>Boot time:</b> {datetime.datetime.fromtimestamp(psutil.boot_time()).strftime(
            "%Y-%m-%d %H:%M:%S"
        )}
        {f'<b>glibc ver:</b> {platform.glibc()[1]}' if hasattr(platform, 'glibc') else ''}
        """

        await message.reply(
                string,
                quote=True
            )
    
    @command("osrelease")
    async def osrelease_cmd(self, bot: Client, message: Message):
        string = f"""📦  <b>/etc/os-releases Info:</b>
        <b>Pretty Name:</b> {os_release["PRETTY_NAME"]}
        <b>Name:</b> {os_release["NAME"]}
        <b>Version:</b> {os_release.get("VERSION", "Not available")}
        <b>Documentation:</b> {os_release.get("DOCUMENTATION_URL", "Not available")}
        <b>Support:</b> {os_release.get("SUPPORT_URL", "Not available")}
        <b>Bug Report:</b> {os_release["BUG_REPORT_URL"]}
            """

        await message.reply(
                string,
                quote=True
            )
    
    @command("neofetch")
    async def neofetch_cmd(self, _, message: Message):
        output = subprocess.getoutput("neofetch --stdout")
        await message.reply(f"<code>{output}</code>")
    