# This test code was written by the `hypothesis.extra.ghostwriter` module
# and is provided under the Creative Commons Zero public domain dedication.

import pytest
from hypothesis import assume, given
from hypothesis import strategies as st

import pfp_generator.colors
import pfp_generator.generate

rgb_strategy = st.builds(
    pfp_generator.colors.RGB,
    st.tuples(
        st.integers(min_value=0, max_value=255),
        st.integers(min_value=0, max_value=255),
        st.integers(min_value=0, max_value=255),
    ),
)


@given(
    size=st.integers(),
    color=st.lists(rgb_strategy),
    color_weight=st.lists(st.floats(allow_nan=False, allow_infinity=False)),
    seed=st.text(),
)
def test_fuzz_ColorMatrix(
    size: int,
    color: list[pfp_generator.colors.RGB],
    color_weight: list[float],
    seed: str,
) -> None:
    assume(sum(color_weight) > 0)
    assume(size > 0)
    if len(color) != len(color_weight):
        with pytest.raises(ValueError):
            pfp_generator.generate.ColorMatrix(
                size=size, color=color, color_weight=color_weight, seed=seed
            )
    else:
        pfp_generator.generate.ColorMatrix(
            size=size, color=color, color_weight=color_weight, seed=seed
        )
