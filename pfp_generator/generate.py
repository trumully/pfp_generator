"""Generate a profile picture pattern with a given color matrix."""

import hashlib
from dataclasses import dataclass

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


def convert_seed(seed: str | bytes | bytearray | int) -> int:
    """Convert the seed to an integer if neeeded.

    Args:
        seed (str | bytes | bytearray | int): The seed to convert.

    Returns:
        int: The converted seed.
    """
    if isinstance(seed, int):
        return seed
    seed = seed.encode() if isinstance(seed, str) else seed
    return sha512(seed)


@dataclass
class ColorMatrix:
    """Create a pattern for a profile picture.

    Attributes:
        size (int): The size of the pattern.
        color (list[RGB]): A list of colors to choose from.
                                        [base, color1, color2, ...]
        color_weight (list[float]): A list of weights for each color.
        seed (str): The seed for the random number generator.

    Raises:
        ValueError: If the length of color and color_weight is not the same.

    Returns:
        np.ndarray: A pattern for a profile picture.
    """

    size: int
    color: list[RGB]
    color_weight: list[float]
    seed: str

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
        self.seed = convert_seed(self.seed)
        self.rng = np.random.default_rng(seed=self.seed)

    def make_pattern(self) -> np.ndarray:
        """Make a pattern for a profile picture.

        Returns:
            np.ndarray: The pattern matrix.
        """
        pattern = self.rng.choice(
            self.color, (self.size * 2, self.size), p=self.color_weight
        )
        return pattern

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
        pattern = self.make_pattern()
        pattern = np.array([[color.as_tuple() for color in row] for row in pattern])
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
        color_matrices (list[ColorMatrix]): A list of color matrices to generate the
                                            patterns.

    Returns:
        list[np.ndarray]: A list of generated pattern matrices.
    """
    return [generate_pfp(color_matrix) for color_matrix in color_matrices]
