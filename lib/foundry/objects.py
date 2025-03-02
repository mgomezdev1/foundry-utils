from typing import Optional
from pydantic import BaseModel

class FoundryObject(BaseModel):
    def shift(self, dx: float, dy: float):
        pass

class FoundryMapData(BaseModel):
    name: str = "UnnamedMap"
    width: int = 0
    height: int = 0
    grid: int = 0
    shift_x: int = 0
    shift_y: int = 0
    grid_distance: float
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
        copy["lights"] = [FoundryLight.from_data(l) for l in copy.get("lights", [])]
        copy["walls"]  = [FoundryWall.from_data(w) for w in copy.get("walls", [])]
        return cls(**copy)

    def get_data(self):
        return {
            "name": self.name,
            "width": self.width,
            "height": self.height,
            "grid": self.grid,
            "shift_x": self.shift_x,
            "shift_y": self.shift_y,
            "grid_distance": self.grid_distance,
            "grid_units": self.grid_units,
            "padding": self.padding,
            "grid_color": self.grid_color,
            "grid_alpha": self.grid_alpha,
            "global_light": self.global_light,
            "darkness": self.darkness,
            "lights": [light.get_data() for light in self.lights],
            "walls": [wall.get_data() for wall in self.walls],
            "img": self.img,
            "foreground": self.foreground
        }

class FoundryLight(FoundryObject):
    x: float = 0
    y: float = 0
    dim: float = 0
    bright: float = 0
    tint_color: str = "#000000"
    tint_alpha: float = 0

    def get_data(self):
        return self.model_dump(mode='json')
    
    @classmethod
    def from_data(cls, data: dict):
        return cls(**data)
    
    def shift(self, dx: float, dy: float):
        self.x += dx
        self.y += dy

class FoundryWall(FoundryObject):
    start_x: float = 0
    start_y: float = 0
    end_x: float = 0
    end_y: float = 0
    move: bool = False
    sense: bool = False
    sound: bool = False
    door: bool = False

    def get_data(self):
        return {
            "c": [self.start_x, self.start_y, self.end_x, self.end_y],
            "move": 1 if self.move else 0,
            "sense": 1 if self.sense else 0,
            "sound": 1 if self.sound else 0,
            "door": 1 if self.door else 0
        }
    
    @classmethod
    def build(cls, coords: tuple[float, float, float, float], move=False, sense=False, sound=False, door=False):
        return cls(
            start_x=coords[0],
            start_y=coords[1],
            end_x=coords[2],
            end_y=coords[3],
            move=move,
            sense=sense,
            sound=sound,
            door=door
    )

    @classmethod
    def solid(cls, coords: tuple[float, float, float, float]):
        return cls.build(coords, True, True, True, False)

    @classmethod
    def from_data(cls, data: dict):
        coords = data.get("c", [0, 0, 0, 0])
        return cls.build(
            coords=coords,
            move=bool(data.get("move", 0)),
            sense=bool(data.get("sense", 0)),
            sound=bool(data.get("sound", 0)),
            door=bool(data.get("door", 0))
        )
    
    def shift(self, dx: float, dy: float):
        self.start_x += dx
        self.start_y += dy
        self.end_x += dx
        self.end_y += dy
