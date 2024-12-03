import streamlit as st
from streamlit_image_coordinates import streamlit_image_coordinates
from PIL import Image, ImageDraw

st.set_page_config(layout="wide")

IMAGE_WIDTH = 100
IMAGE_HEIGHT = 100
SPACING = 25  # Space between images

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

# Initialize session state for selected image and composite image
if "selected_image" not in st.session_state:
    st.session_state.selected_image = None
if "composite_image" not in st.session_state:
    st.session_state.composite_image = None

padding = ((len(images2) * (IMAGE_HEIGHT + SPACING)) - (len(images1) * (IMAGE_HEIGHT + SPACING))) // 2


def create_image(selected_image=None):
    # Determine the width and height for the canvas
    row1_count = len(images1)
    row2_count = len(images2)
    canvas_width = max(row1_count, row2_count) * (IMAGE_WIDTH + SPACING) - SPACING
    canvas_height = 2 * (IMAGE_HEIGHT + SPACING)  # Two rows

    dst = Image.new('RGB', (canvas_width, canvas_height), "white")
    draw = ImageDraw.Draw(dst)

    # Add images for the first row
    for i, img_path in enumerate(images1):
        img = Image.open(img_path).resize((IMAGE_WIDTH, IMAGE_HEIGHT))
        x, y = padding + i * (IMAGE_WIDTH + SPACING), 0
        dst.paste(img, (x, y))

        # Draw a green border if the image is selected
        if selected_image == img_path:
            draw.rectangle(
                [x, y, x + IMAGE_WIDTH, y + IMAGE_HEIGHT],
                outline="green",
                width=5,
            )

    # Add images for the second row
    for i, img_path in enumerate(images2):
        img = Image.open(img_path).resize((IMAGE_WIDTH, IMAGE_HEIGHT))
        x, y = i * (IMAGE_WIDTH + SPACING), IMAGE_HEIGHT + SPACING
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

    x, y = value["x"], value["y"]

    # Check if clicked on images1 (row 1)
    if y < IMAGE_HEIGHT:
        for i, img_path in enumerate(images1):
            img_x = padding + i * (IMAGE_WIDTH + SPACING)
            if img_x <= x <= img_x + IMAGE_WIDTH:
                return img_path

    # Check if clicked on images2 (row 2)
    if IMAGE_HEIGHT + SPACING <= y <= 2 * IMAGE_HEIGHT + SPACING:
        for i, img_path in enumerate(images2):
            img_x = i * (IMAGE_WIDTH + SPACING)
            if img_x <= x <= img_x + IMAGE_WIDTH:
                return img_path

    return None


# Render the interactive image
if st.session_state.composite_image is None:
    st.session_state.composite_image = create_image(st.session_state.selected_image)

placeholder = st.empty()
with placeholder.container():
    value = streamlit_image_coordinates(
        st.session_state.composite_image,
    )

# Determine which image was clicked
clicked_image = determine_clicked_image(value)

# Update the session state and immediately update the displayed image
if clicked_image and clicked_image != st.session_state.selected_image:
    st.session_state.selected_image = clicked_image
    st.session_state.composite_image = create_image(st.session_state.selected_image)

    with placeholder.container():
        value = streamlit_image_coordinates(
            st.session_state.composite_image,
        )
