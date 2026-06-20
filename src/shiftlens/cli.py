from __future__ import annotations

import argparse
from pathlib import Path

from shiftlens.data.toy import make_toy_state_shift
from shiftlens.diagnostics.rejection import make_state_rejection_records
from shiftlens.diagnostics.support import compute_state_support_diagnostics, validate_support_ratio
from shiftlens.features.basic import BasicFeatureProvider
from shiftlens.reports.schema import build_report_payload
from shiftlens.reports.writer import write_report_bundle
from shiftlens.states.extractor import SimpleStateExtractor

TOY_STATE_SHIFT_NUM_POINTS = len(make_toy_state_shift(seed=0)["values"])


def valid_ratio(value: str) -> float:
    try:
        return validate_support_ratio(float(value))
    except ValueError as exc:
        raise argparse.ArgumentTypeError(
            "min-support-ratio must be a finite number between 0.0 and 1.0"
        ) from exc


def valid_window(value: str) -> int:
    try:
        window = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(
            f"window must be an integer between 2 and {TOY_STATE_SHIFT_NUM_POINTS} "
            "for the toy-state-shift demo"
        ) from exc
    if window < 2 or window > TOY_STATE_SHIFT_NUM_POINTS:
        raise argparse.ArgumentTypeError(
            f"window must be an integer between 2 and {TOY_STATE_SHIFT_NUM_POINTS} "
            "for the toy-state-shift demo"
        )
    return window


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="shiftlens")
    subparsers = parser.add_subparsers(dest="command", required=True)

    demo_parser = subparsers.add_parser("demo", help="Run the toy demo.")
    demo_subparsers = demo_parser.add_subparsers(dest="demo_name", required=True)

    toy_parser = demo_subparsers.add_parser(
        "toy-state-shift",
        help="Generate toy state-shift data and write reproducible reports.",
    )
    toy_parser.add_argument("--out", required=True, help="Output directory for reports.")
    toy_parser.add_argument("--seed", type=int, default=7, help="Deterministic random seed.")
    toy_parser.add_argument(
        "--window",
        type=valid_window,
        default=12,
        help="Rolling window size for basic feature extraction.",
    )
    toy_parser.add_argument(
        "--min-support-ratio",
        type=valid_ratio,
        default=0.15,
        help="Minimum support ratio used for rejection checks.",
    )
    return parser


def run_toy_state_shift_demo(out_dir: str | Path, seed: int, window: int, min_support_ratio: float) -> dict:
    dataset = make_toy_state_shift(seed=seed)
    provider = BasicFeatureProvider(window=window)
    feature_batch = provider.transform(dataset["values"])

    extractor = SimpleStateExtractor()
    extraction = extractor.extract(feature_batch["features"], feature_batch["window_indexes"])

    diagnostics = compute_state_support_diagnostics(
        assignments=extraction["assignments"],
        min_support_ratio=min_support_ratio,
    )
    rejection_records = make_state_rejection_records(
        diagnostics=diagnostics,
        state_summaries=extraction["state_summaries"],
    )

    report = build_report_payload(
        dataset=dataset,
        feature_batch=feature_batch,
        extractor_name=extractor.name,
        extraction=extraction,
        diagnostics=diagnostics,
        rejection_records=rejection_records,
        output_dir=Path(out_dir),
    )
    write_report_bundle(Path(out_dir), report)
    return report


def main() -> None:
    args = build_parser().parse_args()
    if args.command == "demo" and args.demo_name == "toy-state-shift":
        run_toy_state_shift_demo(
            out_dir=args.out,
            seed=args.seed,
            window=args.window,
            min_support_ratio=args.min_support_ratio,
        )
        return
    raise SystemExit("Unsupported command.")


if __name__ == "__main__":
    main()
