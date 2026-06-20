from __future__ import annotations

from abc import ABC, abstractmethod

import numpy as np


class FeatureProvider(ABC):
    """Base abstraction for rolling-window feature providers."""

    name = "feature_provider"

    def __init__(self, window: int) -> None:
        if window < 2:
            raise ValueError("window must be at least 2")
        self.window = window

    @property
    @abstractmethod
    def feature_names(self) -> list[str]:
        raise NotImplementedError

    @abstractmethod
    def transform(self, values: np.ndarray) -> dict:
        raise NotImplementedError
