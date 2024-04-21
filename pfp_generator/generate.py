"""Generate a profile picture pattern with a given color matrix."""

import random
from dataclasses import dataclass
from typing import Any

from pfp_generator.colors import RGB

Matrix = list[list[Any]]


@dataclass(frozen=True)
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
        Matrix: A pattern for a profile picture.
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
        random.seed(self.seed)

    def make_pattern(self) -> Matrix:
        """Make a pattern for a profile picture.

        Returns:
            Matrix: The pattern matrix.
        """
        return [
            [
                random.choices(self.color, self.color_weight, k=1)[0]
                for _ in range(self.size)
            ]
            for _ in range(self.size * 2)
        ]

    def reflect_pattern(self, pattern: Matrix) -> Matrix:
        """Reflect the pattern matrix to make a symmetric pattern.

        Args:
            pattern (Matrix): The pattern matrix.

        Returns:
            Matrix: The symmetric pattern matrix.
        """
        return [row + row[::-1] for row in pattern]

    def __call__(self) -> Matrix:
        """Create a pattern for a profile picture.

        Returns:
            Matrix: The created pattern matrix.
        """
        pattern = self.make_pattern()
        return self.reflect_pattern(pattern)


def generate_pfp(color_matrix: ColorMatrix) -> Matrix:
    """Generate a profile picture pattern with a given color matrix.

    Args:
        color_matrix (ColorMatrix): The color matrix to generate the pattern.

    Returns:
        Matrix: The generated pattern matrix.
    """
    return color_matrix()
