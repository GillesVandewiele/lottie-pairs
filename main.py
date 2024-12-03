import streamlit as st
from streamlit_image_coordinates import streamlit_image_coordinates
from PIL import Image, ImageDraw

st.set_page_config(layout="wide")

IMAGE_WIDTH = 50
IMAGE_HEIGHT = 50
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
    canvas_height = 10 + max(row1_count, row2_count) * (IMAGE_WIDTH + SPACING) - SPACING
    canvas_width = 2 * (IMAGE_HEIGHT + SPACING) + 10

    dst = Image.new("RGB", (canvas_width, canvas_height), "white")

    # Add images for the first row
    for i, img_path in enumerate(images1):
        img = Image.open(img_path).resize((IMAGE_WIDTH, IMAGE_HEIGHT))
        y, x = padding + i * (IMAGE_WIDTH + SPACING) + 10, 10
        dst.paste(img, (x, y))

    # Add images for the second row
    for i, img_path in enumerate(images2):
        img = Image.open(img_path).resize((IMAGE_WIDTH, IMAGE_HEIGHT))
        y, x = 10 + i * (IMAGE_WIDTH + SPACING), IMAGE_HEIGHT + SPACING + 10
        dst.paste(img, (x, y))

    return dst


def highlight_selection(base_image, selected_image1, selected_image2, connected_pairs, drawn_lines):
    """
    Draw highlight rectangles and a line between the centers of the selected images.
    """
    overlay = base_image.copy()  # Work on a copy to avoid modifying the cached base image
    draw = ImageDraw.Draw(overlay)
    WIDTH = 5

    # Draw white boxes (reset)
    for i, img_path in enumerate(images1):
        y, x = 10 + padding + i * (IMAGE_WIDTH + SPACING), 10
        draw.rectangle(
            [x - WIDTH, y - WIDTH, x + IMAGE_WIDTH + WIDTH, y + IMAGE_HEIGHT + WIDTH],
            outline="white",
            width=WIDTH
        )

    for i, img_path in enumerate(images2):
        y, x = 10 + i * (IMAGE_WIDTH + SPACING), IMAGE_HEIGHT + SPACING + 10
        draw.rectangle(
            [x - WIDTH, y - WIDTH, x + IMAGE_WIDTH + WIDTH, y + IMAGE_HEIGHT + WIDTH],
            outline="white",
            width=WIDTH
        )

    # Highlight the selected image in row 1
    for i, img_path in enumerate(images1):
        y, x = 10 + padding + i * (IMAGE_WIDTH + SPACING), 10
        if img_path == selected_image1:
            draw.rectangle(
                [x - WIDTH, y - WIDTH, x + IMAGE_WIDTH + WIDTH, y + IMAGE_HEIGHT + WIDTH],
                outline="green",
                width=WIDTH
            )

    # Highlight the selected image in row 2
    for i, img_path in enumerate(images2):
        y, x = 10 + i * (IMAGE_WIDTH + SPACING), IMAGE_HEIGHT + SPACING + 10
        if img_path == selected_image2:
            draw.rectangle(
                [x - WIDTH, y - WIDTH, x + IMAGE_WIDTH + WIDTH, y + IMAGE_HEIGHT + WIDTH],
                outline="green",
                width=WIDTH
            )

    # Draw a line between the centers of the selected images
    if selected_image1 and selected_image2:
        idx1 = images1.index(selected_image1) if selected_image1 in images1 else None
        idx2 = images2.index(selected_image2) if selected_image2 in images2 else None

        if idx1 is not None and idx2 is not None:
            center1 = (10 + IMAGE_HEIGHT // 2,
                       padding + idx1 * (IMAGE_WIDTH + SPACING) + IMAGE_WIDTH // 2)
            center2 = (10 + IMAGE_HEIGHT + SPACING + IMAGE_HEIGHT // 2,
                       idx2 * (IMAGE_WIDTH + SPACING) + IMAGE_WIDTH // 2,)

            draw.line([center1, center2], fill="blue", width=2)

            # Store the connected pair
            connected_pairs.append((selected_image1, selected_image2))

            # Store the drawn line
            drawn_lines.append([center1, center2])

    # Redraw all previous lines
    for line in drawn_lines:
        draw.line(line, fill="blue", width=2)

    return overlay, connected_pairs, drawn_lines


# Determine which image was clicked and which row it belongs to
def determine_clicked_image(value):
    if value is None:
        return None, None

    y, x = value["x"], value["y"]

    # Check if clicked on images1 (row 1)
    if y < IMAGE_HEIGHT:
        for i, img_path in enumerate(images1):
            img_x = padding + i * (IMAGE_WIDTH + SPACING)
            if img_x <= x <= img_x + IMAGE_WIDTH:
                return img_path, 1  # Row 1

    # Check if clicked on images2 (row 2)
    if IMAGE_HEIGHT + SPACING <= y <= 2 * IMAGE_HEIGHT + SPACING:
        for i, img_path in enumerate(images2):
            img_x = i * (IMAGE_WIDTH + SPACING)
            if img_x <= x <= img_x + IMAGE_WIDTH:
                return img_path, 2  # Row 2

    return None, None

if "selected_image1" not in st.session_state:
    st.session_state.selected_image1 = None

if "selected_image2" not in st.session_state:
    st.session_state.selected_image2 = None

if "connected_pairs" not in st.session_state:
    st.session_state.connected_pairs = []

if "drawn_lines" not in st.session_state:
    st.session_state.drawn_lines = []

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
clicked_image, row = determine_clicked_image(value)

try:
    if clicked_image:
        if row == 1 and clicked_image != st.session_state.selected_image1:
            st.session_state.selected_image1 = clicked_image  # Update selected image for row 1
        elif row == 2 and clicked_image != st.session_state.selected_image2:
            st.session_state.selected_image2 = clicked_image  # Update selected image for row 2

        # Update the base image and add connection logic
        st.session_state.base_image, st.session_state.connected_pairs, st.session_state.drawn_lines = highlight_selection(
            st.session_state.base_image, 
            st.session_state.selected_image1, 
            st.session_state.selected_image2, 
            st.session_state.connected_pairs,
            st.session_state.drawn_lines
        )

        if st.session_state.selected_image1 and st.session_state.selected_image2:
            # Clear the selections
            st.session_state.selected_image1 = None
            st.session_state.selected_image2 = None

        # Enable submit button when all pairs are connected
        row_with_fewer_images = images1 if len(images1) <= len(images2) else images2
        total_required_connections = len(row_with_fewer_images)

        if len(st.session_state.connected_pairs) == total_required_connections:
            submit_button_enabled = True
        else:
            submit_button_enabled = False

        # Render the submit button
        submit_button = st.button("Submit", disabled=not submit_button_enabled)
        with placeholder.container():
            value = streamlit_image_coordinates(st.session_state.base_image)  # No unique key, single component for both rows
except:
    pass
