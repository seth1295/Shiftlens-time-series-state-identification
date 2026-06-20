# ShiftLens

ShiftLens is a Python toolkit for state visibility in noisy time-series data.

The first release focuses on:

- toy and synthetic datasets
- basic rolling-window feature extraction
- deterministic candidate state assignment
- support diagnostics and explicit rejection records
- reproducible JSON and Markdown reporting

ShiftLens produces diagnostics and reproducible state evidence only. It does not provide decision, execution, operational, or control authority.

## Project Status

ShiftLens is an early release.

The current version is intended for experimentation, examples, and reproducible diagnostics on toy or synthetic time-series datasets. APIs, report schemas, and state-diagnostic behavior may change as the project matures.

ShiftLens is not production-ready and should not be used as an automated decision, execution, or operational control system.


## Install

```bash
pip install -e .
```

## Run the toy demo

```bash
shiftlens demo toy-state-shift --out reports/demo
```

This writes:

- `reports/demo/report.json`
- `reports/demo/report.md`

## License and Attribution

ShiftLens is licensed under the Apache License, Version 2.0.

This release contains original ShiftLens source code, documentation, examples, and toy/synthetic datasets.

Runtime and test dependencies are declared in `pyproject.toml`.

Any future copied, adapted, or substantially derived third-party source material will preserve applicable license notices and attribution and will be documented in `NOTICE` or `ATTRIBUTION.md` as appropriate.

## Scope

ShiftLens produces diagnostics and reproducible state evidence only. ShiftLens does not provide decision, execution, operational, or control authority.
