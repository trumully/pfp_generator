# This test code was written by the `hypothesis.extra.ghostwriter` module
# and is provided under the Creative Commons Zero public domain dedication.

from hypothesis import given
from hypothesis import strategies as st

import pfp_generator.colors
from pfp_generator.colors import RGB

rgb_values = st.integers(min_value=0, max_value=255)


@given(r=rgb_values, g=rgb_values, b=rgb_values)
def test_fuzz_RGB(r: int, g: int, b: int) -> None:
    pfp_generator.colors.RGB(r=r, g=g, b=b)


@given(
    color_a=st.builds(RGB, b=rgb_values, g=rgb_values, r=rgb_values),
    color_b=st.builds(RGB, b=rgb_values, g=rgb_values, r=rgb_values),
)
def test_fuzz_color_distance(
    color_a: pfp_generator.colors.RGB, color_b: pfp_generator.colors.RGB
) -> None:
    pfp_generator.colors.color_distance(color_a=color_a, color_b=color_b)


@given(
    color_a=st.builds(RGB, b=rgb_values, g=rgb_values, r=rgb_values),
    color_b=st.builds(RGB, b=rgb_values, g=rgb_values, r=rgb_values),
)
def test_fuzz_colors_too_similar(
    color_a: pfp_generator.colors.RGB, color_b: pfp_generator.colors.RGB
) -> None:
    pfp_generator.colors.colors_too_similar(color_a=color_a, color_b=color_b)


@given(seed=st.text())
def test_fuzz_generate_random_color(seed: str) -> None:
    pfp_generator.colors.generate_random_color(seed=seed)


@given(hex_color=st.text())
def test_fuzz_hex_to_rgb(hex_color: str) -> None:
    pfp_generator.colors.hex_to_rgb(hex_color=hex_color)


@given(color=st.text())
def test_fuzz_is_valid_color_name(color: str) -> None:
    pfp_generator.colors.is_valid_color_name(color=color)


@given(color=st.text())
def test_fuzz_is_valid_hex(color: str) -> None:
    pfp_generator.colors.is_valid_hex(color=color)


@given(color=st.text())
def test_fuzz_str_to_rgb(color: str) -> None:
    pfp_generator.colors.str_to_rgb(color=color)
