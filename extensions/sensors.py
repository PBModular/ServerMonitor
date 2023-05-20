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


class SensorsExtension(ModuleExtension):
    @command("temp")
    async def temp_cmd(self, bot: Client, message: Message):
        if hasattr(psutil, "sensors_temperatures"):
            sensors_temperatures = psutil.sensors_temperatures()

            string = "🌡  <b>Sensors Info</b>\n" + "<b>Temperature</b>:\n"
            for sensor_name in sensors_temperatures:
                sensor = sensors_temperatures[sensor_name]
                string += f"<b>{sensor_name}</b>\n"
                for sensor_info in sensor:
                    attr = [
                        a
                        for a in dir(sensor_info)
                        if not a.startswith("__")
                        and not a.startswith("_")
                        and not callable(getattr(sensor_info, a))
                    ]
                    for item in attr[:-1]:
                        string += f"├── {item}: {getattr(sensor_info, item)}\n"
                    string += f"└── {attr[-1]}: {getattr(sensor_info, attr[-1])}\n"
        
            await message.reply(
                string,
                quote=True
            )
        else:
            await message.reply(
                cpu_string(),
                quote=True
            )

    # TODO: Implement baterry
    @command("baterry")
    async def baterry_cmd(self, bot: Client, message: Message):
        pass
    
    @command("fan")
    async def fan_cmd(self, bot: Client, message: Message):
        if not hasattr(psutil, "sensors_fans"):
            return await message.reply(
                "❌ <b>Not support / No fans</b>",
                quote=True
            )
        sensors_fans = psutil.sensors_fans()

        if sensors_fans == {}:
            return await message.reply(
                "❌ <b>Not support / No fans</b>",
                quote=True
            )

        string = "<b>Fans</b>:"
        for sensor_name in sensors_fans:
            sensor = sensors_fans[sensor_name]
            string += f"<b>{sensor_name}</b>\n"
            for sensor_info in sensor:
                attr = [
                    a
                    for a in dir(sensor_info)
                    if not a.startswith("__")
                    and not a.startswith("_")
                    and not callable(getattr(sensor_info, a))
                ]
                for item in attr[:-1]:
                    string += f"├── {item}: {getattr(sensor_info, item)}\n"
                string += f"└── {attr[-1]}: {getattr(sensor_info, attr[-1])}\n"
        await message.reply(
            string,
            quote=True
        )