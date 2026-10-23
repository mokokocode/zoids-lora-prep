import os
from PIL import Image

# This tells the script where to look and where to save
INPUT_FOLDER = "raw_sprites"
OUTPUT_FOLDER = "ready_for_kohya"
BACKGROUND_COLOR = (255, 0, 255) # Pure Magenta
TARGET_SIZE = 512

def format_zoids_assets():
    # Make the output folder if it doesn't exist
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)
        
    if not os.path.exists(INPUT_FOLDER):
        print(f"Please create a folder named '{INPUT_FOLDER}' next to this script and put your PNGs inside!")
        return

    # Look at every file in the raw folder
    for filename in os.listdir(INPUT_FOLDER):
        if filename.endswith(".png"):
            # 1. Open the tiny GBA sprite
            image_path = os.path.join(INPUT_FOLDER, filename)
            sprite = Image.open(image_path).convert("RGBA")
            
            # 2. Figure out how much to scale it up without blurring
            w, h = sprite.size
            scale = min(TARGET_SIZE // w, TARGET_SIZE // h)
            if scale < 1: scale = 1
                
            new_w, new_h = (w * scale, h * scale)
            
            # 3. Upscale using Nearest Neighbor to keep crisp pixel edges
            sprite_scaled = sprite.resize((new_w, new_h), Image.Resampling.NEAREST)
            
            # 4. Create a 512x512 solid magenta square
            canvas = Image.new("RGBA", (TARGET_SIZE, TARGET_SIZE), BACKGROUND_COLOR + (255,))
            
            # 5. Paste the upscaled sprite perfectly in the middle of the magenta square
            offset_x = (TARGET_SIZE - new_w) // 2
            offset_y = (TARGET_SIZE - new_h) // 2
            canvas.paste(sprite_scaled, (offset_x, offset_y), sprite_scaled)
            
            # 6. Save the final image as an RGB file (no transparency allowed for SD 1.5)
            final_image = canvas.convert("RGB")
            clean_name = filename.replace(".png", "")
            final_image.save(os.path.join(OUTPUT_FOLDER, f"{clean_name}.png"))
            
            # 7. Create the matching .txt file for Kohya
            txt_path = os.path.join(OUTPUT_FOLDER, f"{clean_name}.txt")
            with open(txt_path, "w") as text_file:
                text_file.write("16-bit, pixel art, gba style, retro game sprite, mecha, zoid, solid magenta background")
                
            print(f"Successfully formatted: {filename}")

if __name__ == "__main__":
    format_zoids_assets()
    print("ALL DONE! You can close this now.")
