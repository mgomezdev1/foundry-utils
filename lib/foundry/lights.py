from pydantic import BaseModel
from lib.foundry.objects import FoundryObject

class LightConfig(BaseModel):
    dim: float = 0
    bright: float = 0
    color: str = "#000000"
    alpha: float = 0
    negative: bool = False
    priority: float = 0
    angle: float = 360
    extra: dict

    def get_data(self) -> dict:
        data = self.model_dump(mode="json", exclude={"extra"})
        for k, v in self.extra.items():
            data[k] = v
        return data
    
    @classmethod
    def from_data(cls, data: dict) -> "LightConfig":
        copy = {**data}

        extra = {}
        attributes = cls.model_fields
        for k in list(copy.keys()):
            if k not in attributes:
                extra[k] = copy.pop(k)
        copy["extra"] = extra
        
        return cls(**copy)

class FoundryLight(FoundryObject):
    x: float = 0
    y: float = 0
    config: LightConfig
    extra: dict

    def get_data(self) -> dict:
        data = self.model_dump(mode="json", exclude={"config", "extra"})
        data["config"] = self.config.get_data()
        for k, v in self.extra.items():
            data[k] = v
        return data
    
    @classmethod
    def from_data(cls, data: dict):
        copy = {**data}
        config = LightConfig.from_data(copy.pop("config", {}))
        if "dim" in copy: config.dim = copy.pop("dim")
        if "bright" in copy: config.bright = copy.pop("bright")
        if "tint_color" in copy: config.color = copy.pop("tint_color")
        if "tint_alpha" in copy: config.alpha = copy.pop("tint_alpha")

        extra = {}
        attributes = cls.model_fields
        for k in list(copy.keys()):
            if k not in attributes:
                extra[k] = copy.pop(k)
        copy["extra"] = extra
        copy["config"] = config

        return cls(**copy)
    
    def shift(self, dx: float, dy: float):
        self.x += dx
        self.y += dy