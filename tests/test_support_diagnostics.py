import numpy as np
import pytest

from shiftlens.diagnostics.support import compute_state_support_diagnostics, validate_support_ratio


def test_support_diagnostics_counts_and_ratios() -> None:
    diagnostics = compute_state_support_diagnostics(np.array([0, 0, 1, 1, 1]), 0.3)
    support = {entry["state_id"]: entry for entry in diagnostics["support_by_state"]}
    assert support[0]["support_count"] == 2
    assert support[1]["support_count"] == 3
    assert support[1]["meets_min_support_threshold"] is True
    assert diagnostics["state_support_concentration_diagnostic"]["status"] == "ok"


@pytest.mark.parametrize("value", [float("nan"), float("inf"), float("-inf"), -0.1, 1.5])
def test_support_ratio_validation_rejects_invalid_values(value: float) -> None:
    with pytest.raises(ValueError, match="finite number between 0.0 and 1.0"):
        validate_support_ratio(value)


@pytest.mark.parametrize("value", [0.0, 1.0])
def test_support_ratio_validation_accepts_boundaries(value: float) -> None:
    assert validate_support_ratio(value) == value


@pytest.mark.parametrize("value", [float("nan"), float("inf"), float("-inf"), -0.1, 1.5])
def test_support_diagnostics_reject_invalid_min_support_ratio(value: float) -> None:
    with pytest.raises(ValueError, match="finite number between 0.0 and 1.0"):
        compute_state_support_diagnostics(np.array([0, 1]), value)
