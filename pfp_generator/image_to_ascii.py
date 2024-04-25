from enum import Enum
from typing import Optional

import cv2
import numpy as np
from PIL import Image, ImageEnhance

from pfp_generator.colors import RGB, colorize_text


class AsciiType(Enum):
    """Classifies the character sets used for the ASCII art.

    Attributes:
        SIMPLE (str): A simple character set.
        BARS (str): A character set with varying shades.
        COMPLEX (str): A complex character set.
    """

    SIMPLE = "@%#*+=-:. "
    BARS = "█"
    COMPLEX = (
        '$@B%8&WM#*zcvunxrjft/\\|()1{}[]?-_+~<>i!lI;;::,,,"""^^^'
        "`````'''''.......     "
    )


def get_sizes(image: np.ndarray, num_columns: int) -> tuple[int, ...]:
    """Get the sizes of the image and the cells.

    Args:
        image (np.ndarray): The image to be converted to ASCII art.
        num_columns (int): The number of columns in the ASCII art.

    Returns:
        tuple[int, ...]: The width, height, cell_width, cell_height, and
                        num_rows of the image.
    """
    height, width = image.shape
    cell_width = width / num_columns
    cell_height = 2 * cell_width
    num_rows = round(height / cell_height)
    return width, height, cell_width, cell_height, num_rows


def enhance_image(
    image: Image, brightness: Optional[int] = None, contrast: Optional[int] = None
) -> Image:
    """With a given image, enhance the brightness and contrast if provided.

    Args:
        image (Image): the image to be enhanced.
        brightness (Optional[int], optional): The brightness value. Defaults to None.
        contrast (Optional[int], optional): The contrast value. Defaults to None.

    Returns:
        Image: The enhanced image.
    """
    if contrast is not None:
        image = ImageEnhance.Contrast(image).enhance(contrast)
    if brightness is not None:
        image = ImageEnhance.Brightness(image).enhance(brightness)

    return image


def grayscale_image(image: Image) -> np.array:
    """Convert an image to grayscale.

    Args:
        image (Image): The image to be converted to grayscale.

    Returns:
        np.array: The grayscale image.
    """
    return cv2.cvtColor(np.array(image), cv2.COLOR_BGR2GRAY)


def get_start_and_end_indices(a: int, b: int, c: int) -> slice:
    """Get the start and end indices of a slice for a given cell.

    Args:
        a (int): The index of the cell.
        b (int): The width or height of the cell.
        c (int): The width or height of the image.

    Returns:
        slice: The start and end indices of the slice.
    """
    return slice(int(a * b), min(int((a + 1) * b), c))


def determine_ascii_character(
    grayscale_image: np.ndarray,
    colored_image: np.ndarray,
    row: int,
    column: int,
    cell_width: int,
    cell_height: int,
    width: int,
    height: int,
    num_chars: int,
) -> tuple[int, RGB]:
    """Determine the ASCII character for a given cell.

    Args:
        grayscaled_image (np.ndarray): The image grayscaled.
        colored_image (np.ndarray): The image colored.
        cell_width (int): The width of the cell.
        cell_height (int): The height of the cell.
        width (int): The width of the image.
        height (int): The height of the image.
        num_chars (int): The number of characters in the ASCII character set.

    Returns:
        int: The index of the ASCII character.
        RGB: The RGB color of the ASCII character.
    """
    row_slice = get_start_and_end_indices(row, cell_height, height)
    column_slice = get_start_and_end_indices(column, cell_width, width)
    index = min(
        int(np.mean(grayscale_image[row_slice, column_slice]) * num_chars / 255),
        num_chars - 1,
    )
    rgb_color = tuple(
        map(int, np.mean(colored_image[row_slice, column_slice], axis=(0, 1)))
    )

    return index, RGB(*rgb_color)


def image_to_ascii(
    image: Image,
    num_columns: int = 100,
    ascii_mode: AsciiType = AsciiType.BARS,
    brightness: Optional[float] = None,
    contrast: Optional[float] = None,
) -> str:
    """Convert an image to ASCII art.

    Args:
        image (Image): The image to be converted to ASCII art.
        num_columns (int, optional): The number of columns. Defaults to 100.
        ascii_mode (AsciiType, optional): The character set to use.
                                          Defaults to AsciiType.BARS.
        brightness (Optional[float], optional): Brightness value. Defaults to None.
        contrast (Optional[float], optional): Amount of contrast. Defaults to None.

    Returns:
        str: The ascii art.
    """
    num_chars = len(ascii_mode.value)

    image_as_array: np.ndarray = np.array(image)

    grayscaled_image: np.ndarray = grayscale_image(
        enhance_image(image, brightness, contrast)
    )

    width, height, cell_width, cell_height, num_rows = get_sizes(
        grayscaled_image, num_columns
    )

    output_str = ""
    for i in range(num_rows):
        for j in range(num_columns):
            index, color = determine_ascii_character(
                grayscaled_image,
                image_as_array,
                i,
                j,
                cell_width,
                cell_height,
                width,
                height,
                num_chars,
            )
            output_str += colorize_text(ascii_mode.value[index], color)
        if i < num_rows - 1:
            output_str += "\n"
    return output_str
