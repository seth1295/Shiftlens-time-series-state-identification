import numpy as np

from shiftlens.features.basic import BasicFeatureProvider


def test_basic_feature_provider_output_shape_and_names() -> None:
    values = np.linspace(0.0, 1.0, 20)
    provider = BasicFeatureProvider(window=5)
    batch = provider.transform(values)
    assert batch["features"].shape == (16, 7)
    assert batch["feature_names"] == [
        "mean",
        "std",
        "min",
        "max",
        "range",
        "slope",
        "mean_absolute_difference",
    ]
    assert batch["window_indexes"][0] == 4


def test_basic_feature_provider_values_are_finite() -> None:
    provider = BasicFeatureProvider(window=6)
    batch = provider.transform(np.sin(np.arange(30)))
    assert np.isfinite(batch["features"]).all()
