"""This handles color logic for the profile picture generator."""

import random
import re
from dataclasses import dataclass
from math import sqrt

from PIL import ImageColor

COLOR_THRESHOLD: float = 152.96


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
        return "#{:02x}{:02x}{:02x}".format(self.r, self.g, self.b)

    def __str__(self) -> str:
        return " | ".join([str(x) for x in (self.as_tuple(), self.as_hex())])


def generate_random_color(seed: str) -> RGB:
    """Generate a random color with a given seed.

    Args:
        seed (str): The seed for the random number generator.

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
        (((512 + r_mean) * r * r) >> 8) + 4 * g * g + (((767 - r_mean) * b * b) >> 8)
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


def str_to_rgb(color: str, fallback: str = "black") -> RGB:
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
        return RGB(*ImageColor.getrgb(fallback))


def hex_to_rgb(hex_color: str) -> RGB:
    """Convert a hex color to an RGB color.

    Args:
        hex_color (str): The hex color string.

    Returns:
        RGB: The RGB color.
    """
    hex_color = hex_color.lstrip("#")
    return RGB(*(int(hex_color[i : i + 2]) for i in range(0, len(hex_color), 2)))


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

    from answer @ https://stackoverflow.com/a/53330328
    ^            // start of line
    #            // literal pound sign, followed by
    (?:          // either:
      (?:          // a non-capturing group of:
        [\da-f]{3}   // exactly 3 of: a single digit or a letter 'a'-'f'
      ){1,2}       // repeated exactly 1 or 2 times
    |            // or:
      (?:          // a non-capturing group of:
        [\da-f]{4}   // exactly 4 of: a single digit or a letter 'a'-'f'
      ){1,2}       // repeated exactly 1 or 2 times
    )
    $            // end of line
    i            // ignore case (let 'A'-'F' match 'a'-'f')

    Args:
        color (str): The color string to check.

    Returns:
        bool: True if the string is a valid hex color, False otherwise.
    """
    return bool(
        re.match(
            r"/^#(?:(?:[\da-f]{3}){1,2}|(?:[\da-f]{4}){1,2})$/i", color, re.IGNORECASE
        )
    )
