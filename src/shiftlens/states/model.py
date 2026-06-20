from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CandidateStateSummary:
    state_id: int
    label: str
    support_count: int
    mean_feature_mean: float
    mean_feature_std: float
