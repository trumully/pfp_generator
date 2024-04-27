"""This handles color logic for the profile picture generator."""

import random
import re
from dataclasses import dataclass
from math import sqrt

from PIL import ImageColor

COLOR_THRESHOLD: float = 306  # 765 * 0.4
FALLBACK_COLOR = "black"


@dataclass(frozen=True, slots=True)
class RGB:
    """A class to represent an RGB color.

    Attributes:
        r (int): The red value.
        g (int): The green value.
        b (int): The blue value.
    """

    r: int
    g: int
    b: int

    def as_tuple(self) -> tuple[int, int, int]:
        """Convert the RGB values to a tuple.

        Returns:
            tuple[int, int, int]: The RGB values as a tuple.
        """
        return (self.r, self.g, self.b)

    def as_hex(self) -> str:
        """Convert the RGB values to a hex string.

        Returns:
            str: The RGB values as a hex string.
        """
        return f"#{self.r:02x}{self.g:02x}{self.b:02x}"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, RGB):
            return False
        return self.as_tuple() == other.as_tuple()

    def __str__(self) -> str:
        return " | ".join([str(x) for x in (self.as_tuple(), self.as_hex())])


def generate_random_color(seed: str | int) -> RGB:
    """Generate a random color with a given seed.

    Args:
        seed (str | int): The seed for the random number generator.

    Returns:
        RGB: The generated random color.
    """
    random.seed(seed)
    return RGB(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))


def color_distance(color_a: RGB, color_b: RGB) -> float:
    """Get the distance between two colors.

    Uses the algorithm shown in the article by Thiadmer Riemersma over at CompuPhase:
    https://www.compuphase.com/cmetric.htm

    Args:
        color_a (RGB): The first color.
        color_b (RGB): The second color.

    Returns:
        float: The distance between the two colors.
    """
    r_mean: int = (color_a.r + color_b.r) // 2
    r: int = color_a.r - color_b.r
    g: int = color_a.g - color_b.g
    b: int = color_a.b - color_b.b

    return sqrt(
        (2 + (r_mean / 256)) * r**2 + 4 * g**2 + (2 + (255 - r_mean) / 256) * b**2
    )


def colors_too_similar(color_a: RGB, color_b: RGB) -> bool:
    """Check if two colors are too similar.

    Args:
        color_a (RGB): The first color.
        color_b (RGB): The second color.

    Returns:
        bool: True if the colors are too similar, False otherwise.
    """
    return color_distance(color_a, color_b) < COLOR_THRESHOLD


def flip_color(color: RGB) -> RGB:
    """Flip the color by subtracting the RGB values from 255.

    Args:
        color (RGB): The color to flip.

    Returns:
        RGB: The flipped color.
    """
    return RGB(255 - color.r, 255 - color.g, 255 - color.b)


def str_to_rgb(color: str) -> RGB:
    """Parse a color name to a valid RGB color.

    Args:
        color (str): The color string to parse.
        fallback (str): The fallback color string. Defaults to "black".

    Returns:
        RGB: The RGB color.
    """
    try:
        return RGB(*ImageColor.getrgb(color))
    except ValueError:
        return RGB(*ImageColor.getrgb(FALLBACK_COLOR))


def hex_to_rgb(hex_color: str) -> RGB:
    """Convert a hex color to an RGB color.

    Args:
        hex_color (str): The hex color string.

    Returns:
        RGB: The RGB color.
    """
    hex_color = hex_color.lstrip("#")
    try:
        colors = (int(hex_color[i : i + 2], 16) for i in range(0, len(hex_color), 2))
        return RGB(*colors)
    except (ValueError, TypeError):
        return RGB(*ImageColor.getrgb(FALLBACK_COLOR))


def is_valid_color_name(color: str) -> bool:
    """Check if a string is a valid color name.

    Args:
        color (str): The color string to check.

    Returns:
        bool: True if the string is a valid color name, False otherwise.
    """
    return color in ImageColor.colormap


def is_valid_hex(color: str) -> bool:
    """Check if a string is a valid hex color.

    Uses regex to check if the string is a valid hex color.
    Solution from https://stackoverflow.com/a/19282773

    Args:
        color (str): The color string to check.

    Returns:
        bool: True if the string is a valid hex color, False otherwise.
    """
    return bool(re.match(r"^#?(?:(?:[0-9a-fA-F]{2}){3}|(?:[0-9a-fA-F]){3})$", color))


def colorize_text(text: str, color: RGB) -> str:
    """Colorize the text with the given color.

    Args:
        text (str): The text to colorize.
        color (RGB): The color to colorize the text with.

    Returns:
        str: The colorized text.
    """
    return f"\u001b[38;2;{color.r};{color.g};{color.b}m{text}\u001b[0m"
