from PIL import Image, ImageDraw, ImageFont
import os
from pathlib import Path

def create_placeholder_image(text, filename, size=(400, 300), bg_color=(102, 126, 234), text_color=(255, 255, 255)):
    """Create a placeholder image with text"""
    # Create image
    img = Image.new('RGB', size, bg_color)
    draw = ImageDraw.Draw(img)
    
    # Try to use a default font, fallback to basic if not available
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 40)
    except:
        try:
            font = ImageFont.truetype("arial.ttf", 40)
        except:
            font = ImageFont.load_default()
    
    # Calculate text position to center it
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    x = (size[0] - text_width) // 2
    y = (size[1] - text_height) // 2
    
    # Draw text
    draw.text((x, y), text, fill=text_color, font=font)
    
    # Save image with explicit format
    img.save(filename, 'JPEG', quality=95)
    print(f"Created {filename}")

def main():
    # Create images directory if it doesn't exist
    images_dir = Path("static/images")
    images_dir.mkdir(parents=True, exist_ok=True)
    
    # Create placeholder images for animals
    animals = [
        ("Cat", "static/images/cat.jpg", (102, 126, 234)),
        ("Dog", "static/images/dog.jpg", (118, 75, 162)),
        ("Elephant", "static/images/elephant.jpg", (52, 152, 219))
    ]
    
    for animal_name, filepath, color in animals:
        create_placeholder_image(animal_name, filepath, bg_color=color)
    
    print("All placeholder images created successfully!")

if __name__ == "__main__":
    main()
