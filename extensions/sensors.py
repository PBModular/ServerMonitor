# Bot stuff
from base.mod_ext import ModuleExtension
from base.module import command
from ..config import ConfigSettings

# Pyrogram
from pyrogram import Client
from pyrogram.types import Message

# Libs
import platform
import cpuinfo
import psutil
import requests

# Python Libs
import time
from threading import Thread


class SensorsExtension(ModuleExtension):
    def on_init(self):
        thread = Thread(target=self.temp_monitor)
        thread.daemon = True
        thread.start()

    def temp_monitor(self):
        while True:
            sensors_temperatures = psutil.sensors_temperatures()
            # sensor_name - amdgpu
            for sensor_name in sensors_temperatures:
                # get temp by sensor name
                sensor = sensors_temperatures[sensor_name]

                if sensor[0].high == None:
                    high = ConfigSettings.high_temp
                else:
                    high = sensor[0].high

                if(sensor[0].current > high and ConfigSettings.ntfy_topic):
                    requests.post(f"https://ntfy.sh/{ConfigSettings.ntfy_topic}",
                        data=f"📛 [{sensor_name}] {sensor[0].current} / {high}".encode(encoding='utf-8'))

                # print(f"[{sensor_name}] {sensor[0].current} / {high}")
            
            time.sleep(60)

    @command("temp")
    async def temp_cmd(self, bot: Client, message: Message):
        if hasattr(psutil, "sensors_temperatures"):
            sensors_temperatures = psutil.sensors_temperatures()

            string = f"🌡  <b>{self.S['sensors']['sensors_info']}</b>\n" + f"<b>{self.S['sensors']['temperature']}</b>:\n"
            string = "🌡  <b>Sensors Info</b>\n" + "<b>Temperature</b>:\n"
            string = f"🌡  <b>{self.S['sensors']['sensors_info']}</b>\n" + f"<b>{self.S['sensors']['temperature']}</b>:\n"
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
                f"❌ <b>{self.S['sensors']['no_fans']}</b>",
                quote=True
            )
        sensors_fans = psutil.sensors_fans()

        if sensors_fans == {}:
            return await message.reply(
                f"❌ <b>{self.S['sensors']['no_fans']}</b>",
                quote=True
            )

        string = f"<b>{self.S['sensors']['fans']}</b>:"
        string = "<b>Fans</b>:"
        string = f"<b>{self.S['sensors']['fans']}</b>:"
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