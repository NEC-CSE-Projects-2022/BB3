#!/usr/bin/env python3
"""
Script to create realistic fruit images based on real fruit appearance
"""

import os
from PIL import Image, ImageDraw, ImageFont
import numpy as np

def create_realistic_fruit_image(fruit_type, filename):
    """Create realistic fruit images with proper colors and shapes"""
    # Image size
    width, height = 400, 300
    
    # Create new image with appropriate background
    img = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(img)
    
    # Realistic fruit colors and backgrounds
    fruit_data = {
        'apple': {
            'bg_start': (255, 245, 245),  # Light pink background
            'bg_end': (255, 200, 200),    # Pink background
            'fruit_color': (220, 20, 60), # Deep red apple
            'highlight': (255, 182, 193), # Light pink highlight
            'name': 'Apple'
        },
        'banana': {
            'bg_start': (255, 253, 230),  # Light yellow background
            'bg_end': (255, 235, 180),    # Yellow background
            'fruit_color': (255, 215, 0), # Gold banana
            'highlight': (255, 255, 200), # Light yellow highlight
            'name': 'Banana'
        },
        'orange': {
            'bg_start': (255, 250, 230),  # Light orange background
            'bg_end': (255, 220, 150),    # Orange background
            'fruit_color': (255, 140, 0), # Dark orange
            'highlight': (255, 200, 100), # Light orange highlight
            'name': 'Orange'
        },
        'guava': {
            'bg_start': (240, 255, 240),  # Light green background
            'bg_end': (200, 255, 200),    # Green background
            'fruit_color': (50, 205, 50), # Lime green
            'highlight': (144, 238, 144), # Light green highlight
            'name': 'Guava'
        },
        'lemon': {
            'bg_start': (255, 255, 230),  # Light yellow background
            'bg_end': (255, 250, 150),    # Yellow background
            'fruit_color': (255, 255, 0), # Bright yellow
            'highlight': (255, 255, 200), # Light yellow highlight
            'name': 'Lemon'
        },
        'pomegranate': {
            'bg_start': (255, 240, 245),  # Light red background
            'bg_end': (255, 200, 220),    # Red background
            'fruit_color': (139, 0, 0),   # Dark red
            'highlight': (255, 182, 193), # Light red highlight
            'name': 'Pomegranate'
        }
    }
    
    fruit_info = fruit_data.get(fruit_type, fruit_data['apple'])
    
    # Create gradient background
    for y in range(height):
        ratio = y / height
        r = int(fruit_info['bg_start'][0] * (1 - ratio) + fruit_info['bg_end'][0] * ratio)
        g = int(fruit_info['bg_start'][1] * (1 - ratio) + fruit_info['bg_end'][1] * ratio)
        b = int(fruit_info['bg_start'][2] * (1 - ratio) + fruit_info['bg_end'][2] * ratio)
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    
    # Draw realistic fruit shape
    if fruit_type == 'apple':
        # Apple shape - round with slight indent at top
        draw.ellipse([width//2 - 80, height//2 - 60, width//2 + 80, height//2 + 60], 
                    fill=fruit_info['fruit_color'], outline=(0,0,0), width=2)
        # Apple stem
        draw.rectangle([width//2 - 3, height//2 - 80, width//2 + 3, height//2 - 60], 
                      fill=(139, 69, 19))
        # Apple leaf
        draw.ellipse([width//2 + 5, height//2 - 75, width//2 + 25, height//2 - 65], 
                    fill=(34, 139, 34))
        
    elif fruit_type == 'banana':
        # Banana shape - curved
        points = [
            (width//2 - 100, height//2 + 20),
            (width//2 - 80, height//2 - 30),
            (width//2 - 40, height//2 - 50),
            (width//2 + 20, height//2 - 40),
            (width//2 + 80, height//2 + 10),
            (width//2 + 100, height//2 + 40)
        ]
        draw.polygon(points, fill=fruit_info['fruit_color'], outline=(0,0,0), width=2)
        
    elif fruit_type == 'orange':
        # Orange shape - round with texture
        draw.ellipse([width//2 - 70, height//2 - 70, width//2 + 70, height//2 + 70], 
                    fill=fruit_info['fruit_color'], outline=(0,0,0), width=2)
        # Orange texture dots
        for i in range(20):
            x = width//2 + np.random.randint(-60, 60)
            y = height//2 + np.random.randint(-60, 60)
            draw.ellipse([x-2, y-2, x+2, y+2], fill=(255, 140, 0))
            
    elif fruit_type == 'guava':
        # Guava shape - round with slight pear shape
        draw.ellipse([width//2 - 60, height//2 - 80, width//2 + 60, height//2 + 60], 
                    fill=fruit_info['fruit_color'], outline=(0,0,0), width=2)
        # Guava texture
        for i in range(15):
            x = width//2 + np.random.randint(-50, 50)
            y = height//2 + np.random.randint(-70, 50)
            draw.ellipse([x-1, y-1, x+1, y+1], fill=(144, 238, 144))
            
    elif fruit_type == 'lemon':
        # Lemon shape - oval with pointed ends
        draw.ellipse([width//2 - 40, height//2 - 70, width//2 + 40, height//2 + 70], 
                    fill=fruit_info['fruit_color'], outline=(0,0,0), width=2)
        # Lemon texture
        for i in range(10):
            x = width//2 + np.random.randint(-30, 30)
            y = height//2 + np.random.randint(-60, 60)
            draw.ellipse([x-1, y-1, x+1, y+1], fill=(255, 255, 200))
            
    elif fruit_type == 'pomegranate':
        # Pomegranate shape - round with crown
        draw.ellipse([width//2 - 70, height//2 - 60, width//2 + 70, height//2 + 60], 
                    fill=fruit_info['fruit_color'], outline=(0,0,0), width=2)
        # Crown at top
        points = [
            (width//2 - 20, height//2 - 60),
            (width//2 - 10, height//2 - 80),
            (width//2, height//2 - 70),
            (width//2 + 10, height//2 - 80),
            (width//2 + 20, height//2 - 60)
        ]
        draw.polygon(points, fill=(139, 69, 19))
    
    # Add highlight to make it look 3D
    draw.ellipse([width//2 - 60, height//2 - 50, width//2 - 20, height//2 - 20], 
                fill=fruit_info['highlight'])
    
    # Add fruit name
    try:
        font = ImageFont.truetype("arial.ttf", 32)
    except:
        font = ImageFont.load_default()
    
    text = fruit_info['name']
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    draw.text(((width - text_width) // 2, height - 40), text, 
              font=font, fill=(0, 0, 0))
    
    # Add decorative border
    draw.rectangle([10, 10, width-10, height-10], outline=fruit_info['fruit_color'], width=3)
    draw.rectangle([20, 20, width-20, height-20], outline=fruit_info['highlight'], width=1)
    
    # Save image
    os.makedirs('static/samples', exist_ok=True)
    img.save(f'static/samples/{filename}', 'JPEG', quality=95)
    print(f"Created realistic: {filename}")

def main():
    """Create all realistic fruit images"""
    fruits = ['apple', 'banana', 'orange', 'guava', 'lemon', 'pomegranate']
    
    for fruit in fruits:
        filename = f'{fruit}_real.jpg'
        create_realistic_fruit_image(fruit, filename)
    
    print("All realistic fruit images created successfully!")

if __name__ == '__main__':
    main()

