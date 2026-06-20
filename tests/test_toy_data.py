import numpy as np

from shiftlens.data.toy import make_toy_state_shift


def test_toy_data_is_deterministic() -> None:
    left = make_toy_state_shift(seed=11)
    right = make_toy_state_shift(seed=11)
    assert np.allclose(left["values"], right["values"])
    assert left["known_state_labels"].tolist() == right["known_state_labels"].tolist()


def test_toy_data_has_expected_segments() -> None:
    dataset = make_toy_state_shift(seed=7)
    assert len(dataset["values"]) == 180
    assert len(dataset["segment_boundaries"]) == 3
    assert dataset["dataset_notice"] == "Toy/synthetic datasets were used."
