import os
import sys

def create_placeholder(filename, text, size=(800, 600), color=(76, 175, 80)):
    """
    Creates a simple PNG placeholder image using Pillow.
    If Pillow is not installed, it attempts to install it or write a tiny raw PNG.
    """
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        print("PIL/Pillow is not installed. Attempting to install...")
        import subprocess
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow"])
            from PIL import Image, ImageDraw, ImageFont
        except Exception as e:
            print(f"Failed to install Pillow: {e}")
            print("Writing minimal valid PNG byte representation instead...")
            # Tiny valid 1x1 green PNG
            tiny_png = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\x0cIDATx\x9cc` \x06\x00\x00\x0e\x00\x07\xbc\xb5\xc4\xb2\x00\x00\x00\x00IEND\xaeB`\x82'
            with open(filename, 'wb') as f:
                f.write(tiny_png)
            print(f"Created tiny fallback PNG: {filename}")
            return

    # Create image
    img = Image.new('RGB', size, color=color)
    draw = ImageDraw.Draw(img)
    
    # Draw simple text
    draw.text((50, 250), text, fill=(255, 255, 255))
    draw.text((50, 300), f"File: {os.path.basename(filename)}", fill=(255, 255, 255))
    draw.text((50, 350), f"Resolution: {size[0]}x{size[1]}", fill=(255, 255, 255))
    
    # Save image
    img.save(filename)
    print(f"Successfully generated placeholder: {filename}")

if __name__ == "__main__":
    assets_dir = "/Applications/XAMPP/xamppfiles/htdocs/11_Biology_Microbiology/microbioexam/agri_book/assets"
    os.makedirs(assets_dir, exist_ok=True)
    
    placeholders = [
        ("ch01_winogradsky_column.png", "Chapter 1: Winogradsky Column"),
        ("ch02_nitrogen_cycle.png", "Chapter 2: Soil Nitrogen Cycle"),
        ("ch03_root_nodules.png", "Chapter 3: Root Nodules Cross-Section"),
        ("ch04_fungal_infection.png", "Chapter 4: Fungal Infection Haustorium"),
        ("ch05_bt_mechanism.png", "Chapter 5: Bt delta-endotoxin Pore Formation"),
        ("ch06_biofertilizer_fermentation.png", "Chapter 6: Biofertilizer Fermentation Bioreactor"),
        ("ch07_rumen_microbes.png", "Chapter 7: Rumen Microbial Ecosystem"),
        ("ch08_composting_microbes.png", "Chapter 8: Composting Microbial Succession"),
        ("ch09_metagenomics_ai.png", "Chapter 9: Soil DNA Metagenomics & AI Smart Farming"),
    ]
    
    for filename, label in placeholders:
        filepath = os.path.join(assets_dir, filename)
        # Only create if it doesn't already exist
        if not os.path.exists(filepath):
            create_placeholder(filepath, label)
        else:
            print(f"File already exists, skipping: {filepath}")
