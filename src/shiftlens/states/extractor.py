from __future__ import annotations

import numpy as np

from shiftlens.states.model import CandidateStateSummary


class SimpleStateExtractor:
    """Deterministic state assignment using quantile bins over mean and std."""

    name = "simple_quantile_state_extractor"

    def extract(self, features: np.ndarray, window_indexes: np.ndarray) -> dict:
        matrix = np.asarray(features, dtype=float)
        if matrix.ndim != 2 or matrix.shape[0] == 0:
            raise ValueError("features must be a non-empty 2D array")
        if matrix.shape[1] < 2:
            raise ValueError(
                "SimpleStateExtractor requires at least two feature columns for its v0 "
                "median-split demo: a primary feature and a variability feature."
            )
        if len(window_indexes) != matrix.shape[0]:
            raise ValueError("window_indexes length must match number of feature rows")

        mean_feature = matrix[:, 0]
        std_feature = matrix[:, 1]
        mean_cut = float(np.median(mean_feature))
        std_cut = float(np.median(std_feature))

        mean_bin = (mean_feature >= mean_cut).astype(int)
        std_bin = (std_feature >= std_cut).astype(int)
        assignments = mean_bin * 2 + std_bin

        state_summaries = []
        for state_id in sorted(np.unique(assignments)):
            mask = assignments == state_id
            label = _state_label(state_id)
            state_mean_feature = mean_feature[mask]
            state_summaries.append(
                CandidateStateSummary(
                    state_id=int(state_id),
                    label=label,
                    support_count=int(mask.sum()),
                    mean_feature_mean=float(state_mean_feature.mean()),
                    mean_feature_std=float(state_mean_feature.std()),
                )
            )

        transitions = int(np.count_nonzero(np.diff(assignments))) if len(assignments) > 1 else 0
        return {
            "assignments": assignments.astype(int),
            "window_indexes": np.asarray(window_indexes, dtype=int),
            "state_summaries": [
                {
                    "state_id": summary.state_id,
                    "label": summary.label,
                    "support_count": summary.support_count,
                    "mean_feature_mean": summary.mean_feature_mean,
                    "mean_feature_std": summary.mean_feature_std,
                }
                for summary in state_summaries
            ],
            "summary": {
                "num_candidate_states": len(state_summaries),
                "num_windows": int(len(assignments)),
                "transition_count": transitions,
                "assignment_rule": (
                    "median split over rolling mean and rolling standard deviation; "
                    "labels are relative to dataset medians"
                ),
            },
        }


def _state_label(state_id: int) -> str:
    mean_label = "above_median_mean" if state_id >= 2 else "below_median_mean"
    std_label = "above_median_variability" if state_id % 2 == 1 else "below_median_variability"
    return f"{mean_label}_{std_label}"
