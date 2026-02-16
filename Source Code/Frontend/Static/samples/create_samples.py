#!/usr/bin/env python3
"""
Script to create placeholder sample images for Fruit Quality AI
Creates sample images for each fruit type and quality category
"""

import os
from PIL import Image, ImageDraw, ImageFont
import numpy as np

def create_placeholder_image(fruit_type, quality, filename):
    """Create a placeholder image with text"""
    # Image size
    width, height = 300, 200
    
    # Create new image
    img = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(img)
    
    # Try to use a nice font
    try:
        font = ImageFont.truetype("arial.ttf", 40)
    except:
        font = ImageFont.load_default()
    
    # Background colors based on quality
    bg_colors = {
        'good': (144, 238, 144),    # Light green
        'bad': (139, 69, 19),      # Dark red  
        'mixed': (255, 193, 7)     # Brown/orange
    }
    
    # Text colors
    text_colors = {
        'good': (0, 100, 0),       # Black
        'bad': (255, 255, 255),     # White
        'mixed': (0, 0, 0)          # Black
    }
    
    # Fruit icons/emojis
    fruit_icons = {
        'apple': '🍎',
        'banana': '🍌',
        'orange': '🍊',
        'guava': '🥝',
        'lemon': '🍋',
        'lime': '🍋',
        'pomegranate': '🍎'
    }
    
    # Quality labels
    quality_labels = {
        'good': 'Good Quality',
        'bad': 'Bad Quality', 
        'mixed': 'Mixed Quality'
    }
    
    # Fill background
    bg_color = bg_colors.get(quality, (200, 200, 200))
    img.paste(bg_color, (0, 0, width, height))
    
    # Add fruit icon
    icon = fruit_icons.get(fruit_type, '🍎')
    draw.text((10, 10), icon, font=font, fill=text_colors.get(quality, (0, 0, 0)))
    
    # Add quality label
    quality_text = quality_labels.get(quality, quality.title())
    draw.text((10, 50), quality_text, font=font, fill=text_colors.get(quality, (0, 0, 0)))
    
    # Add fruit name
    draw.text((10, 90), fruit_type.title(), font=font, fill=text_colors.get(quality, (0, 0, 0)))
    
    # Add description
    descriptions = {
        'apple_good': 'Fresh & Crisp',
        'apple_bad': 'Rotten & Soft',
        'apple_mixed': 'Partially Fresh',
        'banana_good': 'Ripe & Firm',
        'banana_bad': 'Overripe & Brown',
        'banana_mixed': 'Mixed Ripeness',
        'orange_good': 'Juicy & Bright',
        'orange_bad': 'Spoiled & Dark',
        'orange_mixed': 'Mixed Quality',
        'guava_good': 'Fresh & Green',
        'guava_bad': 'Rotten & Brown',
        'guava_mixed': 'Partially Fresh',
        'lemon_good': 'Fresh & Yellow',
        'lemon_bad': 'Spoiled & Brown',
        'lemon_mixed': 'Mixed Quality',
        'lime_good': 'Fresh & Green',
        'lime_bad': 'Rotten & Brown',
        'lime_mixed': 'Mixed Quality',
        'pomegranate_good': 'Fresh & Red',
        'pomegranate_bad': 'Rotten & Brown',
        'pomegranate_mixed': 'Mixed Quality'
    }
    
    description = descriptions.get(filename, f'{fruit_type.title()} {quality_labels.get(quality, "")}')
    draw.text((10, 130), description, font=font, fill=text_colors.get(quality, (0, 0, 0)))
    
    # Save image
    os.makedirs('static/samples', exist_ok=True)
    img.save(f'static/samples/{filename}')
    print(f"Created: {filename}")

def main():
    """Create all sample images"""
    fruits = ['apple', 'banana', 'orange', 'guava', 'lemon', 'lime', 'pomegranate']
    qualities = ['good', 'bad', 'mixed']
    
    for fruit in fruits:
        for quality in qualities:
            filename = f'{fruit}_{quality}.jpg'
            create_placeholder_image(fruit, quality, filename)
    
    print("All sample images created successfully!")

if __name__ == '__main__':
    main()


