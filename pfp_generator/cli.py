"""This module contains the CLI for the profile picture generator."""

import argparse
import random

from PIL import ImageColor

from pfp_generator.display import display_pfp
from pfp_generator.generate import ColorMatrix


def get_random_color(bg_color: str) -> str:
    """Get a random color that is not the background color.

    Args:
        bg_color (str): The background color.

    Returns:
        str: A random color that is not the background color.
    """
    colors = [c for c in list(ImageColor.colormap) if c != bg_color]
    return random.choice(colors)


def main() -> None:
    """The main function for the CLI."""
    parser = argparse.ArgumentParser(
        prog="pfp-generator", description="Generate profile pictures."
    )

    parser.add_argument(
        "text",
        type=str,
        nargs="?",
        default=None,
        help="Text to generate the profile picture from. If left blank, generate a "
        "random profile picture.",
    )

    parser.add_argument(
        "-s",
        "--size",
        type=int,
        default=5,
        help="The size of the base pattern. Defaults to 5.",
    )
    parser.add_argument(
        "-bg",
        "--background",
        type=str,
        default="white",
        help="The color of the background.",
    )
    parser.add_argument(
        "-c",
        "--color",
        type=str,
        default="",
        help="The color of the profile picture.",
    )
    parser.add_argument(
        "-w",
        "--color-weight",
        type=float,
        default=0.35,
        help="The weight of the profile picture color.",
    )
    parser.add_argument(
        "--save",
        action="store_true",
        help="Ask to save the profile picture.",
    )
    args = parser.parse_args()

    if args.text is not None:
        random.seed(args.text)

    args.color = args.color or get_random_color(args.background)

    bg_weight = 1 - args.color_weight
    color_matrix = ColorMatrix(
        size=args.size,
        color=[ImageColor.getrgb(args.background), ImageColor.getrgb(args.color)],
        color_weight=[bg_weight, args.color_weight],
        seed=args.text,
    )
    display_pfp(color_matrix, save=args.save)


if __name__ == "__main__":
    main()
