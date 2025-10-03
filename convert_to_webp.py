#!/usr/bin/env python3
import os
from PIL import Image
import glob

# Configuration
IMAGES_DIR = 'images'
QUALITY = 85  # WebP quality (1-100)
DELETE_ORIGINALS = True

def convert_to_webp():
    # Get all JPG files
    jpg_files = glob.glob(os.path.join(IMAGES_DIR, '*.jpg'))

    if not jpg_files:
        print("No JPG files found in images directory")
        return

    print(f"Found {len(jpg_files)} images to convert\n")

    converted_count = 0
    failed_count = 0

    for jpg_path in jpg_files:
        try:
            # Open image
            img = Image.open(jpg_path)

            # Convert to RGB if necessary (WebP doesn't support all modes)
            if img.mode in ('RGBA', 'LA', 'P'):
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                img = background
            elif img.mode != 'RGB':
                img = img.convert('RGB')

            # Create WebP filename
            webp_path = jpg_path.replace('.jpg', '.webp')

            # Save as WebP with compression
            img.save(webp_path, 'WEBP', quality=QUALITY, method=6)

            # Get file sizes
            original_size = os.path.getsize(jpg_path)
            webp_size = os.path.getsize(webp_path)
            reduction = ((original_size - webp_size) / original_size) * 100

            print(f"[OK] Converted: {os.path.basename(jpg_path)}")
            print(f"  Original: {original_size / 1024:.1f} KB -> WebP: {webp_size / 1024:.1f} KB ({reduction:.1f}% reduction)")

            # Delete original if configured
            if DELETE_ORIGINALS:
                os.remove(jpg_path)
                print(f"  Removed original file")

            converted_count += 1
            print()

        except Exception as e:
            print(f"[FAIL] Failed to convert {os.path.basename(jpg_path)}: {str(e)}\n")
            failed_count += 1

    print(f"\n{'='*60}")
    print(f"Conversion Summary:")
    print(f"  Successfully converted: {converted_count}")
    print(f"  Failed: {failed_count}")
    print(f"  Total: {len(jpg_files)}")
    print(f"{'='*60}")

if __name__ == '__main__':
    print("JPG to WebP Converter")
    print(f"Quality: {QUALITY}")
    print(f"Delete originals: {DELETE_ORIGINALS}\n")

    convert_to_webp()
