import argparse
import json
from typing import Optional
from pydantic import BaseModel, ValidationError

from lib.stitchings.images import stitch_images
from lib.stitchings.maps import map_from_file, stitch_maps
import os

class Source(BaseModel):
    src: str
    merge_from: Optional[str] = None
    img_fmt: str = "jpg"

class Config(BaseModel):
    # Define your configuration fields here
    stitchings: list[Source]
    direction: str = "vertical"
    add_splitting_walls: bool = True
    output: str = "./out/output"
    out_fmt: str = "jpg"
    name: Optional[str] = None
    foundry_dir: Optional[str] = None

def main():
    parser = argparse.ArgumentParser(description="Stitch some maps together.")
    parser.add_argument(
        "--config", "-c", 
        type=str, 
        default='./config/config.json', 
        help="Path to the configuration file"
    )
    args = parser.parse_args()

    config_path = args.config
    with open(config_path, 'r') as config_file:
        config_data = json.load(config_file)
        try:
            config = Config(**config_data)
            print(f"Config: {config}")
        except ValidationError as e:
            print(f"Config validation error: {e}")

    images = [f"{s.src}.{s.img_fmt}" for s in config.stitchings]

    output_dir = os.path.dirname(config.output)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    img_output = f"{config.output}.{config.out_fmt}"
    stitch_images(images, img_output, config.direction)
    map_data = [map_from_file(f"{s.src}.json", s.merge_from) for s in config.stitchings]
    result = stitch_maps(map_data, config.direction, config.add_splitting_walls)
    if config.name:
        result.name = config.name
    if config.foundry_dir:
        foundry_path = os.path.join(config.foundry_dir, os.path.basename(img_output))
        result.background.src = foundry_path
    result.export(f"{config.output}.json")

if __name__ == "__main__":
    main()