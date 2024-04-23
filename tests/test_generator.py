# This test code was written by the `hypothesis.extra.ghostwriter` module
# and is provided under the Creative Commons Zero public domain dedication.

from hypothesis import assume, given
from hypothesis import strategies as st

import pfp_generator.generate


@given(
    size=st.integers(),
    color_weight_dict=st.dictionaries(
        st.text(),
        st.floats(min_value=0, exclude_min=True, allow_infinity=False, allow_nan=False),
        min_size=1,
    ),
    seed=st.text(),
)
def test_fuzz_ColorMatrix(
    size: int,
    color_weight_dict: dict[str, float],
    seed: str,
) -> None:
    color, color_weight = zip(*color_weight_dict.items())
    assume(sum(color_weight) > 0)
    assume(size > 0)
    pfp_generator.generate.ColorMatrix(
        size=size, color=color, color_weight=color_weight, seed=seed
    )
