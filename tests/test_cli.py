import argparse

import pytest

from shiftlens.cli import TOY_STATE_SHIFT_NUM_POINTS, build_parser, valid_ratio, valid_window


@pytest.mark.parametrize("value", ["nan", "inf", "-inf", "-0.1", "1.5"])
def test_valid_ratio_rejects_invalid_values(value: str) -> None:
    with pytest.raises(argparse.ArgumentTypeError, match="finite number between 0.0 and 1.0"):
        valid_ratio(value)


@pytest.mark.parametrize("value, expected", [("0.0", 0.0), ("1.0", 1.0)])
def test_valid_ratio_accepts_boundary_values(value: str, expected: float) -> None:
    assert valid_ratio(value) == expected


@pytest.mark.parametrize("value", ["nan", "inf", "-inf", "-0.1", "1.5"])
def test_build_parser_exits_cleanly_for_invalid_ratio(value: str) -> None:
    parser = build_parser()
    with pytest.raises(SystemExit) as exc:
        parser.parse_args(
            ["demo", "toy-state-shift", "--out", "reports/bad", "--min-support-ratio", value]
        )
    assert exc.value.code == 2


@pytest.mark.parametrize("value", ["1", "181"])
def test_valid_window_rejects_out_of_range_values(value: str) -> None:
    with pytest.raises(
        argparse.ArgumentTypeError,
        match=f"integer between 2 and {TOY_STATE_SHIFT_NUM_POINTS}",
    ):
        valid_window(value)


@pytest.mark.parametrize("value, expected", [("2", 2), ("180", 180)])
def test_valid_window_accepts_boundary_values(value: str, expected: int) -> None:
    assert valid_window(value) == expected


@pytest.mark.parametrize("value", ["1", "181"])
def test_build_parser_exits_cleanly_for_invalid_window(value: str) -> None:
    parser = build_parser()
    with pytest.raises(SystemExit) as exc:
        parser.parse_args(["demo", "toy-state-shift", "--out", "reports/bad", "--window", value])
    assert exc.value.code == 2
