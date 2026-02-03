# Grok API Image Generator

Generate unlimited images using the Grok API with automatic download functionality.

## Features

- ✅ Generate unlimited images with text prompts
- ✅ Automatic download to specified folder
- ✅ Customizable image settings (size, quality, style)
- ✅ Safe filename generation from prompts
- ✅ Interactive command-line interface
- ✅ Error handling and status updates

## Installation

1. Install Python 3.7 or higher
2. Install required dependencies:

```bash
pip install -r requirements.txt
```

Or install manually:
```bash
pip install requests
```

## Usage

### Basic Usage

Run the script:
```bash
python grok_image_generator.py
```

The script will:
1. Ask for your Grok API key
2. Ask for download folder name (default: `grok_images`)
3. Prompt you to enter image descriptions
4. Automatically generate and download images

### Image Settings

You can customize:
- **Size**: 256x256, 512x512, 1024x1024, 1792x1024, 1024x1792
- **Quality**: standard, hd
- **Style**: natural, vivid

### Example Session

```
Enter your Grok API key: xai-xxxxxxxxxxxxx
Enter download folder name: my_images

Enter image prompt: a beautiful sunset over mountains
[Image generated and downloaded]

Enter image prompt: a futuristic cityscape
[Image generated and downloaded]
```

## Programmatic Usage

You can also use the `GrokImageGenerator` class in your own scripts:

```python
from grok_image_generator import GrokImageGenerator

# Initialize
generator = GrokImageGenerator(
    api_key="your-api-key",
    download_folder="images"
)

# Generate and download
filepath = generator.generate_and_download(
    prompt="a serene lake at dawn",
    size="1024x1024",
    quality="hd",
    style="vivid"
)

print(f"Image saved to: {filepath}")
```

## File Organization

Generated images are saved with the format:
```
YYYYMMDD_HHMMSS_prompt_text.png
```

Example: `20260203_143052_beautiful_sunset.png`

## API Key

Get your Grok API key from [X.AI Console](https://console.x.ai/)

## Troubleshooting

- **Authentication Error**: Check your API key
- **Download Failed**: Check internet connection and folder permissions
- **Rate Limiting**: Add delays between requests if needed

## Notes

- Images are saved as PNG files
- The script includes a 1-second delay between requests to avoid rate limiting
- Prompts are truncated to 50 characters for filenames
- All images are automatically organized in your chosen folder

## License

Free to use and modify.
