# Defraglitch

**defraglitch** is a Python script that applies a glitchy fragmentation effect to an input image. The effect generates horizontal glitch rectangles around the main figure detected in the image, sampled with colors from the figure itself, and includes transparency options. This script uses OpenCV to create visually dynamic "glitch" effects suitable for creative projects, social media, or digital art.

## Features
- Applies glitch effects on both sides of a detected figure, with most glitches placed on the right.
- Glitch colors are sampled from the figure itself for an integrated look.
- Configurable opacity to create transparent or solid glitch effects.
- Outputs the modified image in the same directory as the input with a "_glitch" suffix.

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/DirtyBeastAfterTheToad/defraglitch.git
   cd defraglitch
2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt

## Usage
Run the script with an image file path as an argument:
  ```bash 
    python defraglitch.py <input_img_path>
  ```
- <input_img_path>: Path to the input image (e.g., images/sample.png).
- The output image will be saved in the same directory as the input image, with _glitch appended to the filename (e.g., sample_glitch.png).

## Example
  ```bash 
    python defraglitch.py 01.png
  ```
- This command will create a new file 01_glitch.png with the glitch effect applied.

## How it works
1. **Edge Detection and Mask Creation**: The script detects edges in the input image to isolate the main figure.
2. **Color Sampling**: Colors are sampled from within the figure to create glitch rectangles that blend seamlessly with the original image.
3. **Glitch Effect**: Randomly sized rectangles are placed around the figure, primarily on the right side, and an optional opacity effect is applied.
4. **Image Output**: The final image is saved with a "_glitch" suffix in the original file’s directory.
