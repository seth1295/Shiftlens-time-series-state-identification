from __future__ import annotations

import json
from pathlib import Path


def write_report_bundle(output_dir: Path, report: dict) -> tuple[Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "report.json"
    md_path = output_dir / "report.md"

    json_path.write_text(
        json.dumps(report, indent=2, sort_keys=False, allow_nan=False) + "\n",
        encoding="utf-8",
    )
    md_path.write_text(_render_markdown_report(report), encoding="utf-8")
    return json_path, md_path


def _render_markdown_report(report: dict) -> str:
    artifact_identity = report["artifact_identity"]
    dataset_summary = report["dataset_summary"]
    provider = report["feature_providers"][0]
    diagnostics = report["diagnostics"]

    lines = [
        "# ShiftLens Toy State Report",
        "",
        str(dataset_summary["dataset_notice"]),
        "",
        "## Artifact Identity",
        f"- Project: {artifact_identity['project']}",
        f"- Artifact type: {artifact_identity['artifact_type']}",
        f"- Output directory: {artifact_identity['output_directory']}",
        "",
        "## Dataset Summary",
        f"- Dataset: {dataset_summary['dataset_name']}",
        f"- Description: {dataset_summary['description']}",
        f"- Seed: {dataset_summary['seed']}",
        f"- Number of points: {dataset_summary['num_points']}",
        "",
        "## Feature Providers",
        f"- Provider: {provider['provider_name']}",
        f"- Window: {provider['window']}",
        f"- Features: {', '.join(provider['feature_names'])}",
        "",
        "## Extracted Candidate States",
    ]

    for state in report["states"]:
        lines.append(
            f"- State {state['state_id']} ({state['label']}): support_count={state['support_count']}, "
            f"mean_feature_mean={state['mean_feature_mean']:.4f}, mean_feature_std={state['mean_feature_std']:.4f}"
        )

    lines.extend(
        [
            "",
            "## State Support Diagnostics",
            f"- Minimum support ratio: {diagnostics['minimum_support_ratio']:.3f}",
            f"- State support concentration diagnostic: {diagnostics['state_support_concentration_diagnostic']['status']}",
        ]
    )

    for support in diagnostics["support_by_state"]:
        lines.append(
            f"- State {support['state_id']}: count={support['support_count']}, "
            f"ratio={support['support_ratio']:.3f}, "
            f"meets_min_support_threshold={support['meets_min_support_threshold']}"
        )

    lines.extend(["", "## State Rejection Records"])
    for record in report["rejection_records"]:
        lines.append(
            f"- State {record['state_id']}: status={record['status']}, reason={record['reason']}"
        )

    lines.extend(
        [
            "",
            "## Provenance",
            f"- {report['provenance']['implementation_origin']}",
            f"- {report['provenance']['source_material_notice']}",
            "",
        ]
    )
    return "\n".join(lines)
