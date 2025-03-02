import argparse
import json
from pydantic import BaseModel, ValidationError

from lib.stitchings.images import stitch_images
from lib.stitchings.maps import stitch_data
import os

class Source(BaseModel):
    src: str
    img_fmt: str = "jpg"

class Config(BaseModel):
    # Define your configuration fields here
    stitchings: list[Source]
    direction: str = "vertical"
    add_splitting_walls: bool = True
    output: str = "./out/output"
    out_fmt: str = "jpg"

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
    data = [f"{s.src}.json" for s in config.stitchings]

    output_dir = os.path.dirname(config.output)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    stitch_images(images, f"{config.output}.{config.out_fmt}", config.direction)
    stitch_data(data, f"{config.output}.json", config.direction, config.add_splitting_walls)

if __name__ == "__main__":
    main()