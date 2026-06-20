import numpy as np
import pytest

from shiftlens.states.extractor import SimpleStateExtractor


def test_state_extractor_returns_expected_structure() -> None:
    features = np.array(
        [
            [0.0, 0.1],
            [0.2, 0.1],
            [2.0, 0.2],
            [2.2, 1.5],
        ],
        dtype=float,
    )
    indexes = np.arange(len(features))
    result = SimpleStateExtractor().extract(features, indexes)
    assert result["assignments"].shape == (4,)
    assert isinstance(result["state_summaries"], list)
    assert result["summary"]["num_windows"] == 4
    assert result["summary"]["num_candidate_states"] >= 1
    assert "relative to dataset medians" in result["summary"]["assignment_rule"]


def test_state_extractor_mean_feature_std_uses_mean_feature_dispersion() -> None:
    features = np.array(
        [
            [0.0, 0.1],
            [1.0, 0.2],
            [10.0, 5.0],
            [11.0, 6.0],
        ],
        dtype=float,
    )
    indexes = np.arange(len(features))
    result = SimpleStateExtractor().extract(features, indexes)

    summaries = {entry["state_id"]: entry for entry in result["state_summaries"]}
    assert summaries[0]["support_count"] == 2
    assert summaries[0]["mean_feature_mean"] == 0.5
    assert summaries[0]["mean_feature_std"] == 0.5


def test_state_extractor_rejects_one_column_feature_matrix() -> None:
    features = np.array([[0.0], [1.0], [2.0]], dtype=float)
    indexes = np.arange(len(features))

    try:
        SimpleStateExtractor().extract(features, indexes)
    except ValueError as exc:
        assert (
            str(exc)
            == "SimpleStateExtractor requires at least two feature columns for its v0 "
            "median-split demo: a primary feature and a variability feature."
        )
    else:
        raise AssertionError("Expected a ValueError for a one-column feature matrix.")


def test_state_extractor_rejects_mismatched_window_indexes() -> None:
    features = np.array(
        [
            [0.0, 0.1],
            [1.0, 0.2],
            [2.0, 0.3],
        ],
        dtype=float,
    )
    indexes = np.array([0, 1])

    with pytest.raises(ValueError, match="window_indexes length must match number of feature rows"):
        SimpleStateExtractor().extract(features, indexes)


def test_state_extractor_labels_use_relative_median_wording() -> None:
    features = np.array(
        [
            [-5.0, 1.0],
            [-4.0, 2.0],
            [-1.0, 1.0],
            [0.0, 2.0],
        ],
        dtype=float,
    )
    indexes = np.arange(len(features))
    result = SimpleStateExtractor().extract(features, indexes)

    labels = {entry["label"] for entry in result["state_summaries"]}
    assert "below_median_mean_below_median_variability" in labels
    assert "above_median_mean_above_median_variability" in labels
    assert all("high_mean" not in label and "low_mean" not in label for label in labels)
