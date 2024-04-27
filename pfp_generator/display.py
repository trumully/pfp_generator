"""Display a profile picture pattern with a given color matrix."""

from pathlib import Path

from PIL import Image

from pfp_generator.generate import ColorMatrix, batch_generate_pfp, generate_pfp
from pfp_generator.image_to_ascii import image_to_ascii

IMAGES_PER_ROW: int = 5
SAVE_PATH: Path = Path(Path("~").expanduser(), ".cache", "pfp-generator")
CACHE_LIMIT: int = 5  # in MB


def display_pfp(
    matrices: list[ColorMatrix],
    *,
    size: int = 256,
    save: bool = False,
    ascii: bool = False,
) -> None:
    """Display a profile picture pattern with a given color matrix.

    Args:
        matrices (list[ColorMatrix]): The color matrices for the profile pictures.
        size (int): The size of the profile picture. Defaults to 256.
        save (bool): A flag to save the profile picture. Defaults to False.
        ascii (bool): A flag to display the ASCII representation of the profile picture.
    """
    pattern = [generate_pfp(matrices[0])]
    name = str(matrices[0].seed)

    pattern.extend(batch_generate_pfp(matrices[1:]))

    num_images = len(pattern)
    num_rows = (num_images + IMAGES_PER_ROW - 1) // IMAGES_PER_ROW
    num_cols = min(num_images, IMAGES_PER_ROW)

    collage_width, collage_height = size * num_cols, size * num_rows

    collage = Image.new("RGB", (collage_width, collage_height))

    images = []

    for i, p in enumerate(pattern):
        image = (
            Image.fromarray(p.astype("uint8"))
            .convert("RGB")
            .resize((size, size), Image.Resampling.NEAREST)
        )
        images.append(image)
        row, col = divmod(i, IMAGES_PER_ROW)
        collage.paste(image, (col * size, row * size))

    collage.show()

    if cache_exceeded():
        print(
            f"Cache limit reached! If you want to save more images, please clear the "
            f"cache @ {SAVE_PATH}"
        )
    elif save:
        save_file(images, name)

    if ascii:
        print(image_to_ascii(images[0], num_columns=50, contrast=1.5))


def cache_exceeded() -> bool:
    """Check if the cache exceeds the cache limit.

    Returns:
        bool: True if the cache exceeds the cache limit, False otherwise.
    """
    return get_dir_size(SAVE_PATH) >= CACHE_LIMIT


def get_dir_size(directory: Path) -> float:
    """Get the size of a directory and its subdirectories in MB.

    Args:
        directory (Path): The directory to get the size of.

    Returns:
        float: The size of the directory in MB.
    """
    size_bytes = sum(f.stat().st_size for f in directory.glob("**/*") if f.is_file())
    return size_bytes / 1024 / 1024


def save_file(images: list[Image.Image], name: str) -> None:
    """Save an image file.

    Args:
        images (list[Image.Image]): The images to save.
        name (str): The name of the image.
    """
    if not Path.exists((save_dir := Path(SAVE_PATH, name))):
        Path.mkdir(save_dir, parents=True)

    for i, image in enumerate(images, start=1):
        if cache_exceeded():
            return print(
                f"Cache limit reached! If you want to save more images, please clear "
                f"the cache @ {SAVE_PATH}"
            )

        if not Path.exists((filename := Path(save_dir, f"{name}_{i}.png"))):
            image.save(filename)

    print(f"Profile pictures saved to {Path(SAVE_PATH, name)}")
