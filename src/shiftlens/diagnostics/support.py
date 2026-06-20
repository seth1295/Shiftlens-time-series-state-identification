from __future__ import annotations

import math

import numpy as np


def validate_support_ratio(value: float) -> float:
    ratio = float(value)
    if not math.isfinite(ratio) or ratio < 0.0 or ratio > 1.0:
        raise ValueError("min_support_ratio must be a finite number between 0.0 and 1.0")
    return ratio


def compute_state_support_diagnostics(assignments: np.ndarray, min_support_ratio: float) -> dict:
    validated_min_support_ratio = validate_support_ratio(min_support_ratio)
    labels = np.asarray(assignments, dtype=int)
    total = int(len(labels))
    if total == 0:
        raise ValueError("assignments must not be empty")

    state_ids, counts = np.unique(labels, return_counts=True)
    support = []
    ratios = counts / total
    dominant_ratio = float(ratios.max())
    concentration_status = "ok" if dominant_ratio <= 0.75 else "concentrated"

    for state_id, count, ratio in zip(state_ids, counts, ratios):
        support.append(
            {
                "state_id": int(state_id),
                "support_count": int(count),
                "support_ratio": float(ratio),
                "meets_min_support_threshold": bool(ratio >= validated_min_support_ratio),
            }
        )

    return {
        "minimum_support_ratio": validated_min_support_ratio,
        "support_by_state": support,
        "state_support_concentration_diagnostic": {
            "status": concentration_status,
            "dominant_support_ratio": dominant_ratio,
            "reason": "Simple placeholder diagnostic based on the largest support ratio.",
        },
    }
