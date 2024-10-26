import cv2
import numpy as np
import os
import random
import sys

class ImageDefragmentation:
    def __init__(self, image_path):
        self.image_path = image_path
        self.output_path = self._generate_output_path(image_path)

        self.original_image = cv2.imread(self.image_path)
        self.glitch_image = None
        self.mask = None

    def _generate_output_path(self, image_path):
        # Generate output path by appending "_glitch" before the file extension
        dir_name, file_name = os.path.split(image_path)
        file_root, file_ext = os.path.splitext(file_name)
        return os.path.join(dir_name, f"{file_root}_glitch{file_ext}")

    def load_image(self):
        if self.original_image is None:
            print(f"Error loading image from {self.image_path}.")
            return False
        print("Image loaded successfully.")
        return True

    def create_mask(self):
        # Direct edge detection without grayscale conversion
        edges = cv2.Canny(self.original_image, 50, 150)
        dilated = cv2.dilate(edges, np.ones((5, 5), np.uint8), iterations=1)
        contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        mask = np.zeros(self.original_image.shape[:2], dtype=np.uint8)
        if contours:
            largest_contour = max(contours, key=cv2.contourArea)
            cv2.drawContours(mask, [largest_contour], -1, (255), thickness=cv2.FILLED)
        self.mask = mask
        return mask

    def sample_color_from_figure(self, x_start, x_end, y):
        sample_x = random.randint(x_start, x_end)
        sample_y = random.randint(max(0, y - 5), min(self.original_image.shape[0] - 1, y + 5))
        sample_area = self.original_image[sample_y:sample_y+5, sample_x:sample_x+5]
        mean_color = sample_area.mean(axis=(0, 1))
        return tuple(int(c) for c in mean_color)

    def create_glitch_effect(self, opacity=0.5):
        self.glitch_image = self.original_image.copy()
        overlay = self.glitch_image.copy()  # Transparent overlay
        height, width = self.mask.shape

        # Glitch effect parameters
        num_glitches = 444  
        min_length, max_length = 20, 100  
        glitch_height = 2  
        right_side_probability = 0.75  

        for _ in range(num_glitches):
            y = random.randint(0, height - 1)
            if np.any(self.mask[y, :] > 0): 
                row_indices = np.where(self.mask[y, :] > 0)[0]
                if len(row_indices) > 0:
                    x_start = row_indices[0]
                    x_end = row_indices[-1]
                    sampled_color = self.sample_color_from_figure(x_start, x_end, y)

                    if random.random() < right_side_probability:
                        max_possible_length = width - x_end
                        line_length = random.randint(min_length, min(max_length, max_possible_length))
                        x_position = random.randint(x_end, min(width - line_length, x_end + line_length))
                    else:
                        max_possible_length = x_start
                        line_length = random.randint(min_length, min(max_length, max_possible_length))
                        x_position = random.randint(max(0, x_start - line_length - 10), x_start - line_length)

                    # Draw glitch rectangle with transparency
                    cv2.rectangle(overlay, (x_position, y), (x_position + line_length, y + glitch_height), 
                                  sampled_color, -1)

        # Blend the overlay with the original image based on opacity
        cv2.addWeighted(overlay, opacity, self.glitch_image, 1 - opacity, 0, self.glitch_image)

        return self.glitch_image

    def save_processed_image(self):
        if self.glitch_image is not None:
            cv2.imwrite(self.output_path, self.glitch_image)
            print(f"Processed glitch image saved to {self.output_path}")
        else:
            print("No glitch image to save.")

# Command-line interface
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python defraglitch.py <input_img_path>")
        sys.exit(1)

    input_image_path = sys.argv[1]
    defragger = ImageDefragmentation(input_image_path)
    if defragger.load_image():
        defragger.create_mask()
        defragger.create_glitch_effect()
        defragger.save_processed_image()
