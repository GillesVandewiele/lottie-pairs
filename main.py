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

padding = ((len(images2) * (IMAGE_HEIGHT + SPACING)) - (len(images1) * (IMAGE_HEIGHT + SPACING))) // 2



@st.cache_data
def create_base_image():
    """
    Create the composite image once and cache it.
    """
    row1_count = len(images1)
    row2_count = len(images2)
    canvas_width = max(row1_count, row2_count) * (IMAGE_WIDTH + SPACING) - SPACING
    canvas_height = 10 + 2 * (IMAGE_HEIGHT + SPACING)

    dst = Image.new("RGB", (canvas_width, canvas_height), "white")

    # Add images for the first row
    for i, img_path in enumerate(images1):
        img = Image.open(img_path).resize((IMAGE_WIDTH, IMAGE_HEIGHT))
        x, y = padding + i * (IMAGE_WIDTH + SPACING), 10
        dst.paste(img, (x, y))

    # Add images for the second row
    for i, img_path in enumerate(images2):
        img = Image.open(img_path).resize((IMAGE_WIDTH, IMAGE_HEIGHT))
        x, y = i * (IMAGE_WIDTH + SPACING), 10 + IMAGE_HEIGHT + SPACING
        dst.paste(img, (x, y))

    return dst


def highlight_selection(base_image, selected_image):
    """
    Draw a highlight rectangle on top of the base image.
    """
    overlay = base_image.copy()  # Work on a copy to avoid modifying the cached base image
    draw = ImageDraw.Draw(overlay)
    WIDTH = 5

    for i, img_path in enumerate(images1):
        x, y = padding + i * (IMAGE_WIDTH + SPACING), 10
        draw.rectangle(
            [x - WIDTH, y - WIDTH, x + IMAGE_WIDTH + WIDTH, y + IMAGE_HEIGHT + WIDTH],
            outline="white",
            width=WIDTH
        )

    for i, img_path in enumerate(images2):
        x, y = i * (IMAGE_WIDTH + SPACING), 10 + IMAGE_HEIGHT + SPACING
        draw.rectangle(
            [x - WIDTH, y - WIDTH, x + IMAGE_WIDTH + WIDTH, y + IMAGE_HEIGHT + WIDTH],
            outline="white",
            width=WIDTH
        )

    # Highlight in the first row
    for i, img_path in enumerate(images1):
        x, y = padding + i * (IMAGE_WIDTH + SPACING), 10
        if img_path == selected_image:
            draw.rectangle(
                [x - WIDTH, y - WIDTH, x + IMAGE_WIDTH + WIDTH, y + IMAGE_HEIGHT + WIDTH],
                outline="green",
                width=WIDTH
            )

    # Highlight in the second row
    for i, img_path in enumerate(images2):
        x, y = i * (IMAGE_WIDTH + SPACING), 10 + IMAGE_HEIGHT + SPACING
        if img_path == selected_image:
            draw.rectangle(
                [x - WIDTH, y - WIDTH, x + IMAGE_WIDTH + WIDTH, y + IMAGE_HEIGHT + WIDTH],
                outline="green",
                width=WIDTH
            )

    return overlay



# Determine which image was clicked
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

if "selected_image" not in st.session_state:
    st.session_state.selected_image = None

# Cache the base image
if "base_image" not in st.session_state:
    st.session_state.base_image = create_base_image()

# Render the composite image and detect clicks
placeholder = st.empty()
with placeholder.container():
    value = streamlit_image_coordinates(
        st.session_state.base_image,  # Using cached base image
    )

# Update session state for selected image
clicked_image = determine_clicked_image(value)

if clicked_image and clicked_image != st.session_state.selected_image:
    st.session_state.selected_image = clicked_image  # Update selected image only if it's new
    st.session_state.base_image = highlight_selection(st.session_state.base_image, st.session_state.selected_image)
    with placeholder.container():
        value = streamlit_image_coordinates(st.session_state.base_image)
