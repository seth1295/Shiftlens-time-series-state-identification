import json

from shiftlens.reports.schema import build_report_payload
from shiftlens.reports.writer import write_report_bundle


def test_report_writer_creates_json_and_markdown(tmp_path) -> None:
    report = build_report_payload(
        dataset={
            "name": "toy_state_shift",
            "description": "desc",
            "seed": 7,
            "values": [1.0, 2.0, 3.0],
            "known_state_labels": __import__("numpy").array(["a", "b", "c"], dtype=object),
            "public_data_notice": "Public toy/synthetic data only. No private material used.",
        },
        feature_batch={
            "provider_name": "basic_rolling_window",
            "window": 3,
            "feature_names": ["mean"],
            "window_indexes": [2],
        },
        extractor_name="simple_quantile_state_extractor",
        extraction={
            "summary": {"num_candidate_states": 1, "num_windows": 1, "transition_count": 0},
            "state_summaries": [{"state_id": 0, "label": "x", "support_count": 1, "mean_feature_mean": 0.1, "mean_feature_std": 0.2}],
        },
        diagnostics={
            "minimum_support_ratio": 0.1,
            "support_by_state": [{"state_id": 0, "support_count": 1, "support_ratio": 1.0, "meets_min_support_threshold": True}],
            "state_support_concentration_diagnostic": {"status": "concentrated", "dominant_support_ratio": 1.0, "reason": "placeholder"},
        },
        rejection_records=[{"state_id": 0, "status": "accepted", "reason": "ok", "evidence": {}}],
        output_dir=tmp_path,
    )
    json_path, md_path = write_report_bundle(tmp_path, report)
    loaded = json.loads(json_path.read_text(encoding="utf-8"))
    assert loaded["artifact_identity"]["project"] == "ShiftLens"
    assert md_path.read_text(encoding="utf-8").startswith("# ShiftLens Toy State Report")
