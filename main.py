import streamlit as st
from streamlit_image_coordinates import streamlit_image_coordinates
from PIL import Image, ImageDraw

IMAGE_WIDTH = 100
IMAGE_HEIGHT = 100

N_IMAGES = 8

images1 = [
    "verkleed/image1.jpg",
    "verkleed/image2.jpg",
    "verkleed/image3.jpg",
    "verkleed/image4.jpg"
]

images2 = [
    "normaal/image1.jpg",
    "normaal/image2.jpg",
    "normaal/image3.jpg",
    "normaal/image4.jpg",
    "normaal/image5.jpg",
    "normaal/image6.jpg",
    "normaal/image7.jpg",
    "normaal/image8.jpg"
]

# Initialize session state for selected image if not already done
if "selected_image" not in st.session_state:
    st.session_state.selected_image = None


def create_image(selected_image=None):
    dst = Image.new('RGB', (IMAGE_WIDTH * 3, N_IMAGES * (IMAGE_HEIGHT + 25)), "white")
    draw = ImageDraw.Draw(dst)
    padding = ((N_IMAGES * (IMAGE_HEIGHT + 25)) - (len(images1) * (IMAGE_HEIGHT + 25))) // 2
    for i, img_path in enumerate(images1):
        img = Image.open(img_path)
        img = img.resize((IMAGE_WIDTH, IMAGE_HEIGHT))
        x, y = 0, padding + i * (IMAGE_HEIGHT + 25)
        dst.paste(img, (x, y))

        # Draw a green border if the image is selected
        if selected_image == img_path:
            draw.rectangle(
                [x, y, x + IMAGE_WIDTH, y + IMAGE_HEIGHT],
                outline="green",
                width=5,
            )

    for i, img_path in enumerate(images2):
        img = Image.open(img_path)
        img = img.resize((IMAGE_WIDTH, IMAGE_HEIGHT))
        x, y = IMAGE_WIDTH * 2, i * (IMAGE_HEIGHT + 25)
        dst.paste(img, (x, y))

        # Draw a green border if the image is selected
        if selected_image == img_path:
            draw.rectangle(
                [x, y, x + IMAGE_WIDTH, y + IMAGE_HEIGHT],
                outline="green",
                width=5,
            )

    return dst


def determine_clicked_image(value):
    if value is None:
        return None

    padding = ((N_IMAGES * (IMAGE_HEIGHT + 25)) - (len(images1) * (IMAGE_HEIGHT + 25))) // 2

    x, y = value["x"], value["y"]

    # Check if clicked on images1
    if x < IMAGE_WIDTH:
        for i, img_path in enumerate(images1):
            img_y = padding + i * (IMAGE_HEIGHT + 25)
            if img_y <= y <= img_y + IMAGE_HEIGHT:
                return img_path

    # Check if clicked on images2
    if IMAGE_WIDTH * 2 <= x <= IMAGE_WIDTH * 3:
        for i, img_path in enumerate(images2):
            img_y = i * (IMAGE_HEIGHT + 25)
            if img_y <= y <= img_y + IMAGE_HEIGHT:
                return img_path

    return None


# Render the interactive image
placeholder = st.empty()
with placeholder.container():
    value = streamlit_image_coordinates(
        create_image(st.session_state.selected_image),
    )

# Determine which image was clicked
clicked_image = determine_clicked_image(value)

# Update the session state and immediately re-render the image if needed
if clicked_image and clicked_image != st.session_state.selected_image:
    st.session_state.selected_image = clicked_image
    with placeholder.container():
        value = streamlit_image_coordinates(
            create_image(st.session_state.selected_image),
        )

# # Display debug information
# st.write("Selected image:", st.session_state.selected_image)
