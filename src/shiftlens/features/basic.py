from __future__ import annotations

import numpy as np

from shiftlens.features.base import FeatureProvider


class BasicFeatureProvider(FeatureProvider):
    name = "basic_rolling_window"

    @property
    def feature_names(self) -> list[str]:
        return [
            "mean",
            "std",
            "min",
            "max",
            "range",
            "slope",
            "mean_absolute_difference",
        ]

    def transform(self, values: np.ndarray) -> dict:
        series = np.asarray(values, dtype=float)
        if series.ndim != 1:
            raise ValueError("values must be one-dimensional")
        if len(series) < self.window:
            raise ValueError("values length must be at least the window size")

        rows = []
        window_indexes = []
        x = np.arange(self.window, dtype=float)

        for end in range(self.window, len(series) + 1):
            window = series[end - self.window : end]
            mean = float(window.mean())
            std = float(window.std())
            min_value = float(window.min())
            max_value = float(window.max())
            value_range = max_value - min_value
            centered_x = x - x.mean()
            centered_y = window - window.mean()
            slope = float(np.dot(centered_x, centered_y) / np.dot(centered_x, centered_x))
            mean_abs_diff = float(np.mean(np.abs(np.diff(window))))
            rows.append([mean, std, min_value, max_value, value_range, slope, mean_abs_diff])
            window_indexes.append(end - 1)

        features = np.asarray(rows, dtype=float)
        return {
            "provider_name": self.name,
            "window": self.window,
            "feature_names": self.feature_names,
            "window_indexes": np.asarray(window_indexes, dtype=int),
            "features": features,
        }
