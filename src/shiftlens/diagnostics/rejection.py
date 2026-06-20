from __future__ import annotations


def make_state_rejection_records(diagnostics: dict, state_summaries: list[dict]) -> list[dict]:
    summary_by_id = {entry["state_id"]: entry for entry in state_summaries}
    concentration = diagnostics["state_support_concentration_diagnostic"]
    records = []

    for support in diagnostics["support_by_state"]:
        state_id = support["state_id"]
        meets_support = support["meets_min_support_threshold"]
        if meets_support:
            status = "accepted"
            reason = "State meets the minimum support threshold."
        else:
            status = "rejected"
            reason = "State support is below the minimum support threshold."

        evidence = {
            "support_count": support["support_count"],
            "support_ratio": support["support_ratio"],
            "minimum_support_ratio": diagnostics["minimum_support_ratio"],
            "state support concentration diagnostic": concentration,
            "state_label": summary_by_id.get(state_id, {}).get("label", "unknown"),
        }
        records.append(
            {
                "state_id": state_id,
                "status": status,
                "reason": reason,
                "evidence": evidence,
            }
        )
    return records
