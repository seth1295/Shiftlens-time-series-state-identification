from shiftlens.diagnostics.rejection import make_state_rejection_records


def test_rejection_records_include_required_fields() -> None:
    diagnostics = {
        "minimum_support_ratio": 0.4,
        "support_by_state": [
            {
                "state_id": 0,
                "support_count": 2,
                "support_ratio": 0.2,
                "meets_min_support_threshold": False,
            }
        ],
        "state_support_concentration_diagnostic": {
            "status": "ok",
            "dominant_support_ratio": 0.2,
            "reason": "placeholder",
        },
    }
    state_summaries = [{"state_id": 0, "label": "below_median_mean_below_median_variability"}]
    record = make_state_rejection_records(diagnostics, state_summaries)[0]
    assert record["state_id"] == 0
    assert record["status"] == "rejected"
    assert "reason" in record
    assert "evidence" in record
    assert "state support concentration diagnostic" in record["evidence"]
