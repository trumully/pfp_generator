"""This module contains the CLI for the profile picture generator."""

import argparse
import time

import pfp_generator.colors as colors
from pfp_generator.display import display_pfp
from pfp_generator.generate import ColorMatrix

MAX_PATTERN_SIZE: int = 100


def clean_color(color: str, seed: str | int) -> colors.RGB:
    """Sanitize the color string to a valid RGB color.

    Args:
        color (str): The color string to sanitize.
        seed (str | int): The seed for the random number generator.

    Returns:
        colors.RGB: The sanitized RGB color.
    """
    if colors.is_valid_color_name(color):
        return colors.str_to_rgb(color)
    color = "#" + color if not color.startswith("#") else color
    if colors.is_valid_hex(color):
        return colors.hex_to_rgb(color)
    return colors.generate_random_color(seed)


def clean_seed(seed: str) -> str | int:
    """Clean the seed to a valid seed.

    Args:
        seed (str): The seed to clean.

    Returns:
        str | int: The cleaned seed.
    """
    return int(seed) if seed.isnumeric() else str(seed)


def make_colors(
    bg: str, c: str, seeds: list[str | int]
) -> tuple[colors.RGB, colors.RGB]:
    """Make the background and color for the profile picture.

    Args:
        bg (str): The background color.
        c (str): The color.
        seeds (list[str | int]): The seeds for the random number generator.

    Returns:
        tuple[colors.RGB, colors.RGB]: The background and color for the profile picture.
    """
    c_to_rgb = clean_color(c, seeds[0])
    bg_to_rgb = clean_color(bg, seeds[1])

    if (not bg and not c) and colors.colors_too_similar(c_to_rgb, bg_to_rgb):
        c_to_rgb = clean_color(c, seeds[0])
        bg_to_rgb = colors.flip_color(bg_to_rgb)

    return bg_to_rgb, c_to_rgb


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
        help="Text to generate from. Random text is used if not provided.",
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
        metavar="<weight>",
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
    parser.add_argument(
        "--ascii",
        action="store_true",
        help="Display the ASCII representation of the profile picture.",
    )
    args = parser.parse_args()

    if args.size >= MAX_PATTERN_SIZE:
        return print(f"Pattern size must be less than {MAX_PATTERN_SIZE}!")

    default_seed = clean_seed(str(time.time()).replace(".", ""))
    seed = clean_seed(args.text) if args.text else default_seed
    color_seed = clean_seed(str(seed)[::-1])

    if color_seed == seed:
        color_seed = seed + 1 if isinstance(seed, int) else seed + "1"

    seed_to_print = seed

    matrices = []
    for i in range(args.batches):
        bg, c = make_colors(args.background, args.color, [color_seed, seed])
        matrices.append(build_matrix(seed, args.size, args.color_weight, bg, c))
        if i < args.batches - 1:
            seed = clean_seed(str(seed) + str(i + 1))
            color_seed = clean_seed(str(seed)[::-1])

    display_pfp(matrices, save=args.save, ascii=args.ascii)
    print(f"Seed: {seed_to_print}")


if __name__ == "__main__":
    main()
