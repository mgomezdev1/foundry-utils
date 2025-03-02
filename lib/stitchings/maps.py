import json
from lib.foundry.objects import FoundryMapData, FoundryWall
from lib.json_utils import JsonUtils

def stitch_data(data_paths: list[str], output_path: str, direction="vertical", add_splitting_walls=True):
    maps: list[FoundryMapData] = []
    for path in data_paths:
        data = JsonUtils.from_camel_file(path)
        map_data = FoundryMapData.from_data(data)
        maps.append(map_data)

    if not maps:
        raise ValueError("No map data provided")

    base_map = maps[0]
    for map_data in maps[1:]:
        if add_splitting_walls:
            if direction == "vertical":
                y = map_data.height
                base_map.walls.append(FoundryWall.solid((0,y,map_data.width,y)))
            else:
                x = map_data.width
                base_map.walls.append(FoundryWall.solid((x,0,x,map_data.height)))
        base_map.combine(map_data, direction)

    with open(output_path, 'w') as out_file:
        json.dump(base_map.get_data(), out_file, indent=4)
        