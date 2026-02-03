#!/usr/bin/env python3
"""
Grok API Image Generator
Generates unlimited images using Grok API and automatically downloads them
"""

import os
import requests
import json
from datetime import datetime
from pathlib import Path
import time

class GrokImageGenerator:
    def __init__(self, api_key, download_folder="grok_images"):
        """
        Initialize the Grok Image Generator
        
        Args:
            api_key (str): Your Grok API key
            download_folder (str): Folder where images will be saved
        """
        self.api_key = api_key
        self.download_folder = download_folder
        self.base_url = "https://x.com/i/grok"
        
        # Create download folder if it doesn't exist
        Path(self.download_folder).mkdir(parents=True, exist_ok=True)
        print(f"✓ Download folder created/verified: {self.download_folder}")
    
    def generate_image(self, prompt, model="grok-2-vision-1212", size="1024x1024", 
                       quality="medium", style="natural"):
        """
        Generate an image using Grok API
        
        Args:
            prompt (str): Text description of the image to generate
            model (str): Model to use (default: grok-2-vision-1212)
            size (str): Image size (options: 256x256, 512x512, 1024x1024, 1792x1024, 1024x1792)
            quality (str): Image quality (low, medium, or high)
            style (natural or vivid)
        
        Returns:
            dict: API response containing image URL
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": model,
            "prompt": prompt,
            "n": 1,  # Number of images to generate
            "size": size,
            "quality": quality,
            "style": style
        }
        
        try:
            print(f"\n🎨 Generating image with prompt: '{prompt}'")
            response = requests.post(self.base_url, headers=headers, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"❌ Error generating image: {e}")
            if hasattr(e.response, 'text'):
                print(f"Response: {e.response.text}")
            return None
    
    def download_image(self, image_url, prompt):
        """
        Download image from URL and save to folder
        
        Args:
            image_url (str): URL of the generated image
            prompt (str): Original prompt (used for filename)
        
        Returns:
            str: Path to downloaded file
        """
        try:
            # Create safe filename from prompt and timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_prompt = "".join(c for c in prompt[:50] if c.isalnum() or c in (' ', '-', '_')).strip()
            safe_prompt = safe_prompt.replace(' ', '_')
            filename = f"{timestamp}_{safe_prompt}.png"
            filepath = os.path.join(self.download_folder, filename)
            
            # Download image
            print(f"⬇️  Downloading image...")
            img_response = requests.get(image_url)
            img_response.raise_for_status()
            
            # Save to file
            with open(filepath, 'wb') as f:
                f.write(img_response.content)
            
            print(f"✓ Image saved: {filepath}")
            return filepath
        except Exception as e:
            print(f"❌ Error downloading image: {e}")
            return None
    
    def generate_and_download(self, prompt, **kwargs):
        """
        Generate image and automatically download it
        
        Args:
            prompt (str): Text description of the image
            **kwargs: Additional parameters for generate_image()
        
        Returns:
            str: Path to downloaded file or None
        """
        result = self.generate_image(prompt, **kwargs)
        
        if result and 'data' in result and len(result['data']) > 0:
            image_url = result['data'][0]['url']
            return self.download_image(image_url, prompt)
        else:
            print("❌ No image URL found in response")
            return None


def main():
    """Main function to run the image generator"""
    
    print("=" * 60)
    print("  GROK API IMAGE GENERATOR")
    print("=" * 60)
    
    # Get API key
    api_key = input("\n🔑 Enter your Grok API key: ").strip()
    
    if not api_key:
        print("❌ API key is required!")
        return
    
    # Get download folder (optional)
    download_folder = input("📁 Enter download folder name (default: 'grok_images'): ").strip()
    if not download_folder:
        download_folder = "grok_images"
    
    # Initialize generator
    generator = GrokImageGenerator(api_key, download_folder)
    
    print("\n" + "=" * 60)
    print("Ready to generate images! Type 'quit' or 'exit' to stop.")
    print("=" * 60)
    
    # Options
    print("\n⚙️  Options (press Enter to use defaults):")
    print("  - Size: 1024x1024 (or: 256x256, 512x512, 1792x1024, 1024x1792)")
    print("  - Quality: medium (or: low, high)")
    print("  - Style: natural (or: vivid)")
    
    image_count = 0
    
    while True:
        print("\n" + "-" * 60)
        prompt = input("\n💭 Enter image prompt (or 'quit' to exit): ").strip()
        
        if prompt.lower() in ['quit', 'exit', 'q']:
            print(f"\n✓ Generated {image_count} images. Goodbye!")
            break
        
        if not prompt:
            print("⚠️  Prompt cannot be empty!")
            continue
        
        # Optional: ask for custom settings
        custom = input("Use custom settings? (y/n, default: n): ").strip().lower()
        
        kwargs = {}
        if custom == 'y':
            size = input("Size (default: 1024x1024): ").strip()
            if size:
                kwargs['size'] = size
            
            quality = input("Quality (default: medium): ").strip()
            if quality:
                kwargs['quality'] = quality
            
            style = input("Style (default: natural): ").strip()
            if style:
                kwargs['style'] = style
        
        # Generate and download
        filepath = generator.generate_and_download(prompt, **kwargs)
        
        if filepath:
            image_count += 1
            print(f"\n✅ Success! Total images generated: {image_count}")
        else:
            print("\n⚠️  Failed to generate/download image. Please try again.")
        
        # Optional delay to avoid rate limiting
        time.sleep(1)


if __name__ == "__main__":
    main()
