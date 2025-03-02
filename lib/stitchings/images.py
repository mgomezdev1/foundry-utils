from PIL import Image

def stitch_images(image_paths, output_path, direction="vertical"):
    images = [Image.open(path) for path in image_paths]
    print(f"Stitching {len(image_paths)} images with direction {direction}")

    if direction == "vertical":
        max_width = max(image.width for image in images)
        total_height = sum(image.height for image in images)
        stitched_image = Image.new('RGB', (max_width, total_height))
        
        y_offset = 0
        for image in images:
            if image.width < max_width:
                image = image.resize((max_width, int(image.height * (max_width / image.width))), Image.ANTIALIAS)
            stitched_image.paste(image, (0, y_offset))
            y_offset += image.height
    else:
        max_height = max(image.height for image in images)
        total_width = sum(image.width for image in images)
        stitched_image = Image.new('RGB', (total_width, max_height))
        
        x_offset = 0
        for image in images:
            if image.height < max_height:
                image = image.resize((int(image.width * (max_height / image.height)), max_height), Image.ANTIALIAS)
            stitched_image.paste(image, (x_offset, 0))
            x_offset += image.width
    
    print(f"Image ready, saving to {output_path}")
    stitched_image.save(output_path)
