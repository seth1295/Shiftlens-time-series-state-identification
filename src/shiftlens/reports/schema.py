from __future__ import annotations

from pathlib import Path


def build_report_payload(
    dataset: dict,
    feature_batch: dict,
    extractor_name: str,
    extraction: dict,
    diagnostics: dict,
    rejection_records: list[dict],
    output_dir: Path,
) -> dict:
    return {
        "artifact_identity": {
            "project": "ShiftLens",
            "artifact_type": "toy_state_report",
            "output_directory": str(output_dir),
            "data_notice": "Toy/synthetic datasets were used for this report.",
        },
        "dataset_summary": {
            "dataset_name": dataset["name"],
            "description": dataset["description"],
            "seed": dataset["seed"],
            "num_points": int(len(dataset["values"])),
            "known_state_labels": sorted(set(dataset["known_state_labels"].tolist())),
            "dataset_notice": dataset["dataset_notice"],
        },
        "feature_providers": [
            {
                "provider_name": feature_batch["provider_name"],
                "window": feature_batch["window"],
                "feature_names": feature_batch["feature_names"],
                "num_windows": int(len(feature_batch["window_indexes"])),
            }
        ],
        "state_extractor": {
            "name": extractor_name,
            "summary": extraction["summary"],
        },
        "states": extraction["state_summaries"],
        "diagnostics": diagnostics,
        "rejection_records": rejection_records,
        "source_trace": {
            "implementation_origin": "Original ShiftLens source code.",
            "dataset_notice": "Toy/synthetic datasets were used for this report.",
        },
    }
