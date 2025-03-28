import os
import math
import numpy as np
from PIL import Image
from tqdm import tqdm

# --- CONFIGURATION ---
TILE_SIZE = 10  # Width and height of each tile
TILE_DIR = "/home/pi5/Photomosaic/dali"  # Folder containing tile images
INPUT_IMAGE = "/home/pi5/Photomosaic/input-photos/karan.jpg"  # Replace with your input image path
OUTPUT_IMAGE = "photomosaic.jpg"
# ----------------------

def average_color(image):
    np_image = np.array(image)
    w, h, d = np_image.shape
    return tuple(np_image.reshape((w * h, d)).mean(axis=0))

def load_tile_images(tile_dir):
    tile_images = []
    avg_colors = []
    print("Loading tiles...")
    for filename in os.listdir(tile_dir):
        try:
            img_path = os.path.join(tile_dir, filename)
            img = Image.open(img_path).convert("RGB").resize((TILE_SIZE, TILE_SIZE))
            tile_images.append(img)
            avg_colors.append(average_color(img))
        except:
            continue
    print(f"{len(tile_images)} tiles loaded.")
    return tile_images, np.array(avg_colors)

def closest_tile(avg_color, tile_avg_colors):
    diffs = np.linalg.norm(tile_avg_colors - avg_color, axis=1)
    return np.argmin(diffs)

def create_photomosaic(input_image_path, tile_images, tile_avg_colors):
    original = Image.open(input_image_path).convert("RGB")
    width, height = original.size

    grid_w = width // TILE_SIZE
    grid_h = height // TILE_SIZE
    new_width = grid_w * TILE_SIZE
    new_height = grid_h * TILE_SIZE
    original = original.resize((new_width, new_height))

    print(f"Creating mosaic: {grid_w} x {grid_h} tiles")

    mosaic = Image.new("RGB", (new_width, new_height))

    for y in tqdm(range(grid_h), desc="Building mosaic"):
        for x in range(grid_w):
            box = (x * TILE_SIZE, y * TILE_SIZE, (x + 1) * TILE_SIZE, (y + 1) * TILE_SIZE)
            region = original.crop(box)
            region_avg = average_color(region)
            tile_idx = closest_tile(region_avg, tile_avg_colors)
            mosaic.paste(tile_images[tile_idx], box)

    mosaic.save(OUTPUT_IMAGE)
    print(f"Mosaic saved as {OUTPUT_IMAGE}")

if __name__ == "__main__":
    tile_imgs, tile_colors = load_tile_images(TILE_DIR)
    create_photomosaic(INPUT_IMAGE, tile_imgs, tile_colors)
