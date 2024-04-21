"""This module contains the CLI for the profile picture generator."""

import argparse
import time

import pfp_generator.colors as colors
from pfp_generator.display import display_pfp
from pfp_generator.generate import ColorMatrix


def clean_color(color: str, seed: str) -> colors.RGB:
    """Sanitize the color string to a valid RGB color.

    Args:
        color (str): The color string to sanitize.

    Returns:
        colors.RGB: The sanitized RGB color.
    """
    if not color:
        return colors.generate_random_color(seed)
    if colors.is_valid_color_name(color):
        return colors.str_to_rgb(color)
    color = "#" + color if not color.startswith("#") else color
    if colors.is_valid_hex(color):
        return colors.hex_to_rgb(color)


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
        default="",
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

    seed = args.text or str(time.time()).replace(".", "")
    color_seed = seed[::-1]
    bg_weight = 1 - args.color_weight
    bg = clean_color(args.background, color_seed)
    c = clean_color(args.color, seed)

    if not args.background and not args.color:
        while colors.colors_too_similar(bg, c):
            color_seed += seed
            bg = clean_color(args.background, color_seed)
            c = clean_color(args.color, seed)

    color_matrix = ColorMatrix(
        size=args.size,
        color=[bg, c],
        color_weight=[bg_weight, args.color_weight],
        seed=seed,
    )

    print(f"Seed: {seed}\nBackground: {bg}\nPrimary: {c}")

    display_pfp(color_matrix, save=args.save)


if __name__ == "__main__":
    main()
