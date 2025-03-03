from typing import Optional
from lib.foundry.maps import FoundryMapData, FoundryWall
from lib.json_utils import JsonUtils

def map_from_file(path: str, merge_from: Optional[str] = None):
    data = JsonUtils.from_camel_file(path)
    map = FoundryMapData.from_data(data)
    
    if (merge_from == None):
        return map
    else:
        data = JsonUtils.from_camel_file(merge_from)
        result = FoundryMapData.from_data(data)
        result.merge(map)
        
        return result
        
def stitch_maps(maps: list[FoundryMapData], direction="vertical", add_splitting_walls=True) -> FoundryMapData:
    base_map = maps[0]
    for map_data in maps[1:]:
        if add_splitting_walls:
            if direction == "vertical":
                y = base_map.height
                base_map.walls.append(FoundryWall.solid((0,y,map_data.width,y)))
            else:
                x = base_map.width
                base_map.walls.append(FoundryWall.solid((x,0,x,map_data.height)))
        base_map.combine(map_data, direction)

    return base_map
