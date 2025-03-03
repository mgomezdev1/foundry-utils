
from pydantic import BaseModel

class FoundryObject(BaseModel):
    def shift(self, dx: float, dy: float):
        pass
