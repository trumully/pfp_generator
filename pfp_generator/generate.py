"""Generate a profile picture pattern with a given color matrix."""

import hashlib
from dataclasses import dataclass, field
from typing import Optional

import numpy as np

from pfp_generator.colors import RGB


def sha512(seed: str) -> int:
    """Create a SHA-512 hash from a given seed.

    Args:
        text (str): The seed to hash.

    Returns:
        int: The hash value.
    """
    hash = int.from_bytes(seed + hashlib.sha512(seed).digest(), "big")
    return hash


def convert_seed(seed: str | bytes | bytearray) -> int:
    """Convert the seed to an integer if neeeded.

    Args:
        seed (str | bytes | bytearray): The seed to convert.

    Returns:
        int: The converted seed.
    """
    seed = seed.encode() if isinstance(seed, str) else seed
    return sha512(seed)


@dataclass(slots=True)
class ColorMatrix:
    """Create a pattern for a profile picture.

    Attributes:
        size (int): The size of the pattern.
        color (list[RGB]): A list of colors to choose from. [base, color1, color2, ...]
        color_weight (list[float]): A list of weights for each color.
        seed (str): The seed for the random number generator.

    Returns:
        np.ndarray: A pattern for a profile picture.
    """

    size: int
    color: list[RGB]
    color_weight: list[float]
    seed: str
    rng: Optional[np.random.Generator] = field(init=False, repr=False, default=None)

    def __post_init__(self) -> None:
        """Validate attributes

        Raises:
            ValueError: If the length of color and color_weight is not the same.
            ValueError: If the sum of color_weight is less than or equal to 0.
        """
        if len(self.color) != len(self.color_weight):
            raise ValueError("The length of color and color_weight must be the same")
        if sum(self.color_weight) <= 0:
            raise ValueError("The sum of color_weight must be greater than 0")

        seed = convert_seed(self.seed) if self.seed_is_byte_like() else int(self.seed)
        self.rng = np.random.default_rng(seed)

    @property
    def width(self) -> int:
        """The width of the pattern."""
        return self.size

    @property
    def height(self) -> int:
        """The height of the pattern."""
        return self.size * 2

    def seed_is_byte_like(self) -> bool:
        """Check if the seed is a byte-like object.

        Returns:
            bool: The result of the check.
        """
        return not isinstance(self.seed, int) and self.seed is not None

    def make_pattern(self) -> np.ndarray:
        """Make a pattern for a profile picture.

        Returns:
            np.ndarray: The pattern matrix.
        """
        return self.rng.choice(
            self.color, (self.height, self.width), p=self.color_weight
        )

    def reflect_pattern(self, pattern: np.ndarray) -> np.ndarray:
        """Reflect the pattern matrix to make a symmetric pattern.

        Args:
            pattern (np.ndarray): The pattern matrix.

        Returns:
            np.ndarray: The symmetric pattern matrix.
        """
        return np.hstack((pattern, np.fliplr(pattern)))

    def __call__(self) -> np.ndarray:
        """Create a pattern for a profile picture.

        Returns:
            np.ndarray: The created pattern matrix.
        """
        pattern = np.array(
            [[color.as_tuple() for color in row] for row in self.make_pattern()]
        )
        return self.reflect_pattern(pattern)


def generate_pfp(color_matrix: ColorMatrix) -> np.ndarray:
    """Generate a profile picture pattern with a given color matrix.

    Args:
        color_matrix (ColorMatrix): The color matrix to generate the pattern.

    Returns:
        np.ndarray: The generated pattern matrix.
    """
    return color_matrix()


def batch_generate_pfp(color_matrices: list[ColorMatrix]) -> list[np.ndarray]:
    """Generate a list of profile picture patterns with a given list of color matrices.

    Args:
        color_matrices (list[ColorMatrix]): A list of color matrices to generate the patterns.

    Returns:
        list[np.ndarray]: A list of generated pattern matrices.
    """
    return [generate_pfp(color_matrix) for color_matrix in color_matrices]
