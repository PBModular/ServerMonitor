# Bot stuff
from base.mod_ext import ModuleExtension
from base.module import command

# Pyrogram
from pyrogram import Client
from pyrogram.types import Message

# Python libs
from os.path import exists
import datetime
import subprocess

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
        string = f"""🐧  <b>{self.S['os']['linux_info']}</b>
        <b>{self.S['cpu']['name']}:</b> {get_distro()}
        <b>{self.S['os']['kernel']}:</b> {platform.release()}
        <b>{self.S['os']['hostname']}:</b> {platform.node()}
        <b>{self.S['os']['boot_time']}:</b> {datetime.datetime.fromtimestamp(psutil.boot_time()).strftime(
            "%Y-%m-%d %H:%M:%S"
        )}
        {f'<b>{self.S["os"]["glibc_ver"]}:</b> {platform.glibc()[1]}' if hasattr(platform, 'glibc') else ''}
        """

        await message.reply(
                string,
                quote=True
            )
    
    @command("osrelease")
    async def osrelease_cmd(self, bot: Client, message: Message):
        string = f"""📦  <b>{self.S["os"]["os_releases"]}:</b>
        <b>{self.S["os"]["pretty_name"]}:</b> {os_release["PRETTY_NAME"]}
        <b>{self.S["cpu"]["name"]}:</b> {os_release["NAME"]}
        <b>{self.S["os"]["version"]}:</b> {os_release.get("VERSION", self.S["os"]["not_available"])}
        <b>{self.S["os"]["documentation"]}:</b> {os_release.get("DOCUMENTATION_URL", self.S["os"]["not_available"])}
        <b>{self.S["os"]["support"]}:</b> {os_release.get("SUPPORT_URL", "Not available")}
        <b>{self.S["os"]["bug_report"]}:</b> {os_release["BUG_REPORT_URL"]}
            """

        await message.reply(
                string,
                quote=True
            )
    
    @command("neofetch")
    async def neofetch_cmd(self, _, message: Message):
        output = subprocess.getoutput("neofetch --stdout")
        await message.reply(f"<code>{output}</code>")
    