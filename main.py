from base.module import BaseModule, command
from pyrogram.types import Message
from base.mod_ext import ModuleExtension
from typing import Type

# Extensions
from .extensions.cpu import CPUExtension
from .extensions.memory import MemoryExtension
from .extensions.os import OSExtension
from .extensions.sensors import SensorsExtension
from .extensions.network import NetworkExtension

# Python Libs
import subprocess

class ServerMonitorModule(BaseModule):

    @property
    def module_extensions(self) -> list[Type[ModuleExtension]]:
        return [
            CPUExtension,
            MemoryExtension,
            OSExtension,
            SensorsExtension,
            NetworkExtension
        ]