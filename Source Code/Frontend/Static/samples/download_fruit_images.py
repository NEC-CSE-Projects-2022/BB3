#!/usr/bin/env python3
"""
Script to create beautiful fruit images with professional design
"""

import os
from PIL import Image, ImageDraw, ImageFont
import numpy as np

def create_beautiful_fruit_image(fruit_type, quality, filename):
    """Create a beautiful fruit image with professional design"""
    # Image size
    width, height = 400, 300
    
    # Create new image with gradient background
    img = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(img)
    
    # Beautiful gradient backgrounds based on quality
    gradients = {
        'good': {
            'start': (144, 238, 144),    # Light green
            'end': (34, 139, 34),       # Forest green
            'text': (0, 100, 0)          # Dark green
        },
        'bad': {
            'start': (255, 182, 193),    # Light pink
            'end': (139, 69, 19),        # Brown
            'text': (139, 0, 0)          # Dark red
        },
        'mixed': {
            'start': (255, 218, 185),    # Peach
            'end': (255, 140, 0),       # Dark orange
            'text': (139, 69, 19)        # Brown
        }
    }
    
    # Create gradient background
    gradient = gradients.get(quality, gradients['good'])
    for y in range(height):
        ratio = y / height
        r = int(gradient['start'][0] * (1 - ratio) + gradient['end'][0] * ratio)
        g = int(gradient['start'][1] * (1 - ratio) + gradient['end'][1] * ratio)
        b = int(gradient['start'][2] * (1 - ratio) + gradient['end'][2] * ratio)
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    
    # Add decorative circle
    circle_color = (255, 255, 255, 128)  # Semi-transparent white
    draw.ellipse([width//2 - 80, height//2 - 80, width//2 + 80, height//2 + 80], 
                fill=(255, 255, 255, 50), outline=(255, 255, 255, 200), width=3)
    
    # Try to use a nice font
    try:
        title_font = ImageFont.truetype("arial.ttf", 48)
        subtitle_font = ImageFont.truetype("arial.ttf", 24)
        desc_font = ImageFont.truetype("arial.ttf", 18)
    except:
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()
        desc_font = ImageFont.load_default()
    
    # Fruit emojis and names
    fruit_data = {
        'apple': {'emoji': '🍎', 'name': 'Apple', 'icon': '🍏'},
        'banana': {'emoji': '🍌', 'name': 'Banana', 'icon': '🍌'},
        'orange': {'emoji': '🍊', 'name': 'Orange', 'icon': '🍊'},
        'guava': {'emoji': '🥝', 'name': 'Guava', 'icon': '🍏'},
        'lemon': {'emoji': '🍋', 'name': 'Lemon', 'icon': '🍋'},
        'lime': {'emoji': '🍋', 'name': 'Lime', 'icon': '🍋'},
        'pomegranate': {'emoji': '🍎', 'name': 'Pomegranate', 'icon': '🍎'}
    }
    
    # Quality labels and descriptions
    quality_data = {
        'good': {
            'label': 'Good Quality',
            'desc': 'Fresh & Perfect',
            'color': (0, 128, 0)
        },
        'bad': {
            'label': 'Bad Quality',
            'desc': 'Rotten & Spoiled',
            'color': (139, 0, 0)
        },
        'mixed': {
            'label': 'Mixed Quality',
            'desc': 'Partially Fresh',
            'color': (255, 140, 0)
        }
    }
    
    fruit_info = fruit_data.get(fruit_type, fruit_data['apple'])
    quality_info = quality_data.get(quality, quality_data['good'])
    
    # Draw large fruit emoji
    draw.text((width//2 - 40, height//2 - 60), fruit_info['emoji'], 
              font=title_font, fill=gradient['text'])
    
    # Draw quality label
    label_text = quality_info['label']
    label_bbox = draw.textbbox((0, 0), label_text, font=subtitle_font)
    label_width = label_bbox[2] - label_bbox[0]
    draw.text(((width - label_width) // 2, height//2 + 20), label_text, 
              font=subtitle_font, fill=quality_info['color'])
    
    # Draw description
    desc_text = quality_info['desc']
    desc_bbox = draw.textbbox((0, 0), desc_text, font=desc_font)
    desc_width = desc_bbox[2] - desc_bbox[0]
    draw.text(((width - desc_width) // 2, height//2 + 50), desc_text, 
              font=desc_font, fill=gradient['text'])
    
    # Draw fruit name at bottom
    name_text = fruit_info['name']
    name_bbox = draw.textbbox((0, 0), name_text, font=subtitle_font)
    name_width = name_bbox[2] - name_bbox[0]
    draw.text(((width - name_width) // 2, height - 40), name_text, 
              font=subtitle_font, fill=gradient['text'])
    
    # Add decorative elements
    draw.rectangle([10, 10, width-10, height-10], outline=gradient['text'], width=2)
    draw.rectangle([20, 20, width-20, height-20], outline=gradient['text'], width=1)
    
    # Save image
    os.makedirs('static/samples', exist_ok=True)
    img.save(f'static/samples/{filename}', 'JPEG', quality=95)
    print(f"Created: {filename}")

def main():
    """Create all beautiful fruit images"""
    fruits = ['apple', 'banana', 'orange', 'guava', 'lemon', 'lime', 'pomegranate']
    qualities = ['good', 'bad', 'mixed']
    
    for fruit in fruits:
        for quality in qualities:
            filename = f'{fruit}_{quality}.jpg'
            create_beautiful_fruit_image(fruit, quality, filename)
    
    print("All beautiful fruit images created successfully!")

if __name__ == '__main__':
    main()
