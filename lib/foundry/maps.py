import json
from typing import Optional
from pydantic import BaseModel

from lib.foundry.lights import FoundryLight
from lib.foundry.walls import FoundryWall
from lib.strings import process_keys_recursive, snake_to_camel

class FoundryMapData(BaseModel):
    name: str = "UnnamedMap"
    width: int = 0
    height: int = 0
    shift_x: int = 0
    shift_y: int = 0
    grid_distance: float = 150
    grid_units: str = "ft"
    padding: float = 0
    grid_color: str = "#000000"
    grid_alpha: float = 0
    global_light: bool = True
    darkness: float = 0
    lights: "list[FoundryLight]" = []
    walls: "list[FoundryWall]" = []
    img: Optional[str] = None
    foreground: Optional[str] = None
    extra: dict = {}

    def shift(self, dx=0, dy=0):
        for l in self.lights:
            l.shift(dx, dy)
        for w in self.walls:
            w.shift(dx, dy)

    def combine(self, other: "FoundryMapData", direction="vertical"):
        if direction == "vertical":
            other.shift(0, self.height)
            self.height += other.height
        elif direction == "horizontal":
            other.shift(self.width, 0)
            self.width += other.width
        else:
            raise ValueError("Direction must be either 'vertical' or 'horizontal'")

        self.lights.extend(other.lights)
        self.walls.extend(other.walls)

    @classmethod
    def from_data(cls, data: dict):
        copy = {**data}
        copy["lights"] = [FoundryLight.from_data(l) for l in copy.pop("lights", [])]
        copy["walls"] = [FoundryWall.from_data(w) for w in copy.pop("walls", [])]

        extra = {}
        attributes = cls.model_fields
        for k in list(copy.keys()):
            if k not in attributes:
                extra[k] = copy.pop(k)
        copy["extra"] = extra
        print(extra)

        return cls(**copy)

    def get_data(self):
        data = dict(self.model_dump(mode="json", exclude={"lights", "walls", "extra"}))
        data["lights"] = [light.get_data() for light in self.lights]
        data["walls"] = [wall.get_data() for wall in self.walls]
        for k, v in self.extra.items():
            data[k] = v
        return data
    
    def merge(self, other: "FoundryMapData"):
        # for now, merge does nothing
        return self

    def export(self, output_path: str):
        data = process_keys_recursive(self.get_data(), snake_to_camel)
        # print(f"Exporting {data}")
        with open(output_path, 'w') as out_file:
            json.dump(data, out_file, indent=4)
