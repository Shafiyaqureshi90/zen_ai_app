from PIL import Image, ImageDraw, ImageFilter
import numpy as np
import random

def create_zen_background(width=1920, height=1080):
    """
    Create a Zen-inspired background image with bamboo and mist effects
    Returns a PNG image with light, desaturated colors suitable for text overlay
    """
    
    # Create blank canvas with light beige base color
    bg_color = (245, 240, 230)  # Light paper-like color
    img = Image.new("RGB", (width, height), bg_color)
    draw = ImageDraw.Draw(img)
    
    # Generate random bamboo stalks
    for _ in range(random.randint(8, 12)):
        # Bamboo stalk properties
        x = random.randint(50, width-50)
        width_bamboo = random.randint(15, 30)
        segments = random.randint(5, 8)
        
        # Bamboo segment colors (greenish-grey)
        bamboo_dark = (180, 195, 175)
        bamboo_light = (200, 210, 195)
        
        # Draw bamboo stalk
        segment_height = height // segments
        for seg in range(segments):
            y1 = seg * segment_height
            y2 = (seg + 1) * segment_height
            
            # Alternate slightly between colors for texture
            color = bamboo_dark if seg % 2 == 0 else bamboo_light
            draw.rounded_rectangle(
                [x, y1, x+width_bamboo, y2],
                radius=width_bamboo//2,
                fill=color
            )
            # Add bamboo joints
            if seg < segments - 1:
                joint_width = width_bamboo + 5
                draw.ellipse(
                    [x-3, y2-5, x+joint_width, y2+5],
                    fill=(150, 140, 130)
                )
    
    # Add mist effect
    mist = Image.new("RGBA", (width, height))
    mist_draw = ImageDraw.Draw(mist)
    
    for _ in range(20):
        x = random.randint(0, width)
        y = random.randint(0, height)
        radius = random.randint(150, 400)
        mist_draw.ellipse(
            [x-radius, y-radius, x+radius, y+radius],
            fill=(255, 255, 255, random.randint(10, 30))
        )
    
    # Composite mist onto background with blur
    mist = mist.filter(ImageFilter.GaussianBlur(radius=100))
    img.paste(mist, (0, 0), mist)
    
    # Add subtle paper texture overlay
    texture = Image.new("RGBA", (width, height))
    texture_px = texture.load()
    for i in range(width):
        for j in range(height):
            noise = random.randint(-5, 5)
            # Create very subtle texture effect
            texture_px[i,j] = (noise, noise, noise, 5)
    img.paste(texture, (0, 0), texture)
    
    # Optimize file size while preserving quality
    img.save("bg.png", format="PNG", optimize=True, quality=90)
    
    # Verify file size is under 400KB
    import os
    size_kb = os.path.getsize("bg.png") / 1024
    if size_kb > 400:
        # If too large, save as JPG with higher compression
        img.convert("RGB").save("bg.jpg", quality=85)
        print(f"Saved as JPG (size: {os.path.getsize('bg.jpg')/1024:.1f}KB)")
    else:
        print(f"Background image created (size: {size_kb:.1f}KB)")
    return img

if _name_ == "_main_":
    # Create HD (1920x1080) background by default
    bg_image = create_zen_background()
    bg_image.show()  # Optionally display the result