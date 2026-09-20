# [PROJECT NAME] — analysis / data

[One sentence: the question this repo exists to answer.]

## Tech stack

- Python [3.12], pandas [2.2], [scikit-learn] / [polars]
- Notebooks: Jupyter, but production code lives in `src/`
- Env: [uv] / [conda]
- Tests: pytest

## Commands

```bash
uv sync
uv run jupyter lab
uv run python -m src.pipeline.run --config configs/[NAME].yaml
uv run pytest -q
uv run ruff check .
```

## Architecture

- `data/raw/`        — immutable source data. NEVER write here.
- `data/interim/`    — intermediate artefacts, safe to delete and regenerate
- `data/processed/`  — model-ready outputs
- `notebooks/`       — exploration only. Prefixed `NN-initials-topic.ipynb`.
- `src/`             — every function a notebook needs. Notebooks import, not define.
- `configs/`         — YAML config per experiment
- `reports/`         — generated figures and write-ups

## Conventions

- Notebooks explore; `src/` is the source of truth. Once a cell works, move it into `src/`.
- Every transformation is a pure function taking a DataFrame and returning a new one.
- No hardcoded paths — read them from the config.
- Set and record a random seed for anything stochastic.
- State units and time zones in column names or docstrings.
- Print row counts before and after any join or filter. Silent row loss is the number one bug.

## Boundaries

- Never modify anything in `data/raw/`.
- Never commit data files or `.ipynb` outputs — check the gitignore before adding files.
- Do not delete `reports/` artefacts; they are referenced externally.
- Do not silently drop rows to make a merge work. Surface the mismatch.

## Build rules

1. Before analysis, profile the data: dtypes, nulls, duplicates, ranges. Report what you find.
2. State assumptions explicitly in the output, not just in your head.
3. Any number that goes in a report must be reproducible from a committed script.
4. Show the sanity checks you ran, not just the conclusion.
