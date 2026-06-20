from __future__ import annotations

import numpy as np


def make_toy_state_shift(seed: int = 7) -> dict:
    """Create deterministic synthetic segments with known labels.

    Returns a dictionary with:
    - name: dataset identifier string.
    - description: summary string.
    - seed: RNG seed integer.
    - values: 1D NumPy array of synthetic time-series values.
    - known_state_labels: 1D NumPy object array of labels.
    - segment_boundaries: list of dictionaries describing segments.
    - dataset_notice: toy/synthetic data notice string.
    """
    rng = np.random.default_rng(seed)
    segments = [
        {"label": "low_mean_low_noise", "length": 60, "mean": 0.0, "std": 0.25},
        {"label": "high_mean_low_noise", "length": 60, "mean": 2.5, "std": 0.25},
        {"label": "low_mean_high_noise", "length": 60, "mean": 0.25, "std": 0.9},
    ]

    values = []
    known_labels = []
    boundaries = []
    start = 0
    for segment in segments:
        segment_values = rng.normal(segment["mean"], segment["std"], segment["length"])
        values.append(segment_values)
        known_labels.extend([segment["label"]] * segment["length"])
        end = start + segment["length"]
        boundaries.append(
            {
                "label": segment["label"],
                "start_index": start,
                "end_index": end,
                "mean": segment["mean"],
                "std": segment["std"],
            }
        )
        start = end

    series = np.concatenate(values)
    return {
        "name": "toy_state_shift",
        "description": "Synthetic series with known state segments for evaluation.",
        "seed": seed,
        "values": series,
        "known_state_labels": np.asarray(known_labels, dtype=object),
        "segment_boundaries": boundaries,
        "dataset_notice": "Toy/synthetic datasets were used.",
    }
