from dataclasses import dataclass

@dataclass
class ConfigSettings:
    ntfy_topic = None
    high_temp = 100