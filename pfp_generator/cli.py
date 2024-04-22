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


def colorize_text(text: str, color: colors.RGB) -> str:
    """Colorize the text with the given color.

    Args:
        text (str): The text to colorize.
        color (colors.RGB): The color to colorize the text with.

    Returns:
        str: The colorized text.
    """
    return f"\u001b[38;2;{color.r};{color.g};{color.b}m{text}\u001b[0m"


def make_colors(
    bg: colors.RGB, c: colors.RGB, seeds: list[str | int]
) -> tuple[colors.RGB, colors.RGB]:
    """Make the background and color for the profile picture.

    Args:
        bg (colors.RGB): The background color.
        c (colors.RGB): The color.
        seeds (list[str  |  int]): The seeds for the random number generator.

    Returns:
        tuple[colors.RGB, colors.RGB]: The background and color for the profile picture.
    """
    bg = clean_color(bg, seeds[1])
    c = clean_color(c, seeds[0])

    if (not bg and not c) and colors.colors_too_similar(bg, c):
        bg = colors.flip_color(bg)
        c = clean_color(c, seeds[0])

    return bg, c


def build_matrix(
    seed: str | int, size: int, weight: float, bg: colors.RGB, c: colors.RGB
) -> ColorMatrix:
    return ColorMatrix(
        size=size,
        color=[bg, c],
        color_weight=[1 - weight, weight],
        seed=seed,
    )


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
        metavar="<size>",
        help="The size of the base pattern. Defaults to 5.",
    )
    parser.add_argument(
        "-bg",
        "--background",
        type=str,
        default="",
        metavar="<color>",
        help="The color of the background.",
    )
    parser.add_argument(
        "-c",
        "--color",
        type=str,
        default="",
        metavar="<color>",
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
        "-b",
        "--batches",
        type=int,
        default=1,
        metavar="<amount>",
        help="The number of profile pictures to generate.",
    )
    parser.add_argument(
        "--save",
        action="store_true",
        help="Ask to save the file.",
    )
    args = parser.parse_args()

    default_seed = int(str(time.time()).replace(".", ""))
    seed = args.text or default_seed
    color_seed = int(str(seed)[::-1]) if seed == default_seed else seed[::-1]

    matrices = []
    for i in range(args.batches):
        bg, c = make_colors(args.background, args.color, [color_seed, seed])
        matrices.append(build_matrix(seed, args.size, args.color_weight, bg, c))
        seed += str(i + 1) if isinstance(seed, str) else int(i + 1)
        color_seed = seed[::-1] if isinstance(seed, str) else int(str(seed)[::-1])

    display_pfp(matrices, save=args.save)


if __name__ == "__main__":
    main()
