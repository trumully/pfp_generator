"""Display a profile picture pattern with a given color matrix."""

from tkinter.filedialog import asksaveasfilename

from PIL import Image

from pfp_generator.generate import ColorMatrix, generate_pfp


def display_pfp(
    color_matrix: ColorMatrix,
    *,
    size: int = 256,
    save: bool = False,
) -> None:
    """Display a profile picture pattern with a given color matrix.

    Args:
        color_matrix (ColorMatrix): The color matrix for the profile picture.
        size (int): The size of the profile picture. Defaults to 100.
        save (bool): A flag to save the profile picture. Defaults to False.
    """
    pattern = generate_pfp(color_matrix)
    name = color_matrix.seed or "pfp"
    image = (
        Image.fromarray(pattern.astype("uint8"))
        .convert("RGB")
        .resize((size, size), Image.NEAREST)
    )

    image.show()
    if save:
        save_file(image, name)


def save_file(image: Image.Image, name: str) -> None:
    """Save an image file.

    Args:
        image (Image.Image): The image to save.
        name (str): The name of the image.
    """
    filename = asksaveasfilename(
        filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg")],
        defaultextension=".png",
        initialfile=name,
    )
    if filename:
        image.save(filename)
