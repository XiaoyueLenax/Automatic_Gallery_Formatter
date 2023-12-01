from PIL import Image, ImageDraw, ImageFont
import os
from datetime import datetime

def create_image_collage(folder_path, collage_path, resize_images=True, max_image_size=200):
    # Get a list of all image files in the folder
    image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]

    if not image_files:
        print("No image files found in the specified folder.")
        return

    # Set starting positions for images
    current_x, current_y = 0, 0

    # Determine the total width and height of all images for dynamic collage size
    total_width, max_height = 0, 600
    image_gap = 5  # Adjust the gap between images

    for image_file in image_files:
        # Open the image
        image_path = os.path.join(folder_path, image_file)
        img = Image.open(image_path)

        # Resize and crop the image if specified
        if resize_images:
            img = crop_and_resize_image(img, max_image_size)

        # Update the total width and height
        total_width += img.width
        max_height = max(max_height, img.height)

    # Calculate the dynamic collage width and height
    collage_width = min(total_width + (len(image_files) - 1) * image_gap, 2200)  # Set a maximum width for the collage
    collage_height = ((len(image_files) - 1) * image_gap) + max_height + 40  # Adjust the height to accommodate multiple rows and space for text
    collage = Image.new('RGB', (collage_width, collage_height), 'white')

    # Initialize drawing context
    draw = ImageDraw.Draw(collage)

    # Use a cute font
    font_path = "constan.ttf"  # Replace with the path to your cute font file
    base_font_size = 12

    for idx, image_file in enumerate(image_files, start=1):
        # Open the image
        image_path = os.path.join(folder_path, image_file)
        img = Image.open(image_path)

        # Resize and crop the image if specified
        if resize_images:
            img = crop_and_resize_image(img, max_image_size)

        # Get and format the creation date and time of the image
        creation_time = os.path.getctime(image_path)
        formatted_time = datetime.utcfromtimestamp(creation_time).strftime('%Y-%m-%d %H:%M:%S')

        # Adjust the font size relative to the image size
        font_size = int(base_font_size * (img.width / 100))
        font = ImageFont.truetype(font_path, font_size)

        # Calculate the position to place the text at the top center of the image
        text_width, text_height = draw.textsize(formatted_time, font)
        text_position = ((current_x + img.width // 2 - text_width // 2), current_y)

        # Paste the image onto the collage
        collage.paste(img, (current_x, current_y))

        # Draw the formatted time on the collage on the image with white outline
        border_size = 2  # Adjust the size of the white border
        for i in range(-border_size, border_size + 1):
            for j in range(-border_size, border_size + 1):
                draw.text((text_position[0] + i, text_position[1] + j), formatted_time, fill='white', font=font)
        draw.text(text_position, formatted_time, fill='black', font=font)

        # Draw the image number at the bottom right
        number_position = (current_x + img.width - 20, current_y + img.height - 20)
        draw.text(number_position, str(idx), fill='red', font=font)
        # Draw the image number at the bottom right with black text and white outline



        # Update the current position for the next image
        current_x += img.width + image_gap

        # Check if a new row is needed
        if current_x + img.width > collage_width:
            current_x = 0
            current_y += img.height + image_gap

    # Draw the total number of images at the bottom center
    total_images_position = (collage_width // 2, collage_height - 20)
    draw.text(total_images_position, f"Total Images: {len(image_files)}", fill='black', font=font)

    # Save the collage image
    collage.save(collage_path)
    print(f"Collage created successfully: {collage_path}")

def crop_and_resize_image(img, size):
    # Crop the image to a square
    min_dimension = min(img.width, img.height)
    left = (img.width - min_dimension) // 2
    top = (img.height - min_dimension) // 2
    right = (img.width + min_dimension) // 2
    bottom = (img.height + min_dimension) // 2
    img = img.crop((left, top, right, bottom))

    # Resize the image
    img.thumbnail((size, size))
    
    return img

# Example usage
folder_path = "C:/Users/coruf/OneDrive/Documents/001_Artsu"
collage_path = "C:/Users/coruf/OneDrive/Documents/Random_Projects/collage.jpg"
create_image_collage(folder_path, collage_path, resize_images=True, max_image_size=200)
