"""Display a profile picture pattern with a given color matrix."""

from tkinter.filedialog import asksaveasfilename

from PIL import Image

from pfp_generator.generate import ColorMatrix, batch_generate_pfp, generate_pfp

PER_ROW: int = 5


def display_pfp(
    matrices: list[ColorMatrix],
    *,
    size: int = 256,
    save: bool = False,
) -> None:
    """Display a profile picture pattern with a given color matrix.

    Args:
        matrices (list[ColorMatrix]): The color matrices for the profile pictures.
        size (int): The size of the profile picture. Defaults to 256.
        save (bool): A flag to save the profile picture. Defaults to False.
    """
    pattern = [generate_pfp(matrices[0])]
    name = "pfps" if len(matrices) > 1 else matrices[0].seed

    pattern.extend(batch_generate_pfp(matrices[1:]))

    num_images = len(pattern)
    num_rows = (num_images + PER_ROW - 1) // PER_ROW
    num_cols = min(num_images, PER_ROW)

    collage_width, collage_height = size * num_cols, size * num_rows

    collage = Image.new("RGB", (collage_width, collage_height))

    for i, p in enumerate(pattern):
        image = (
            Image.fromarray(p.astype("uint8"))
            .convert("RGB")
            .resize((size, size), Image.NEAREST)
        )
        row, col = divmod(i, PER_ROW)
        collage.paste(image, (col * size, row * size))

    collage.show()
    if save:
        save_file(collage, name)


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
