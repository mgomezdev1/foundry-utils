
from lib.foundry.objects import FoundryObject

class FoundryWall(FoundryObject):
    start_x: float = 0
    start_y: float = 0
    end_x: float = 0
    end_y: float = 0
    move: int = 0
    sight: int = 0
    light: int = 0
    sound: int = 0
    door: int = 0
    dir: int = 0
    extra: dict

    def get_data(self):
        return {
            "c": [self.start_x, self.start_y, self.end_x, self.end_y],
            "move": self.move,
            "sight": self.sight,
            "light": self.light,
            "sound": self.sound,
            "door": self.door,
            "dir": self.dir,
            **self.extra
        }
    
    @classmethod
    def build(cls, coords: tuple[float, float, float, float], move=0, sight=0, light=0, sound=0, door=0, dir=0, **extra):
        return cls(
            start_x=coords[0],
            start_y=coords[1],
            end_x=coords[2],
            end_y=coords[3],
            move=20 if move == 1 else move,
            sight=20 if sight == 1 else sight,
            light=20 if light == 1 else light,
            sound=20 if sound == 1 else sound,
            door=door,
            dir=dir,
            extra=extra
        )

    @classmethod
    def solid(cls, coords: tuple[float, float, float, float]):
        return cls.build(coords, move=1, sound=1, sight=1, light=1, door=0, dir=0)

    @classmethod
    def from_data(cls, data: dict):
        coords = data.pop("c", [0, 0, 0, 0])
        move = data.pop("move", 0)
        sound = data.pop("sound", 0)
        door = data.pop("door", 0)
        dir = data.pop("dir", 0)
        
        sense = data.pop("sense", 0)
        sight = data.pop("sight", sense)
        light = data.pop("light", sense)
        return cls.build(
            coords=coords,
            move=move,
            sight=sight,
            light=light,
            sound=sound,
            door=door,
            dir=dir,
            **data
        )
    
    def shift(self, dx: float, dy: float):
        self.start_x += dx
        self.start_y += dy
        self.end_x += dx
        self.end_y += dy
