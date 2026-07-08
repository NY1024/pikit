# Changelog

All notable changes to pikit will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [0.2.0] - 2026-07-08

### Added

- **Batch matrix evaluation** (`pikit.matrix`): `MatrixRunner` automates
  attacks × defenses × channels × agents combinatorial experiments with
  `ExperimentResult` persistence to JSON / CSV.
- **Automatic judge** (`pikit.judge`): `RuleJudge` (heuristic: sink-firing,
  keyword matching, refusal detection) and `LLMJudge` (model-based verdict)
  for automated success/failure verdicts on agent traces.
- **Detection defenses** (`pikit.defenses.detection`): `PatternDetector`,
  `LengthDetector`, `RepetitionDetector` with `DetectionHooks` for flagging
  suspicious input at three agent insertion points.
- **Experiment configuration** (`pikit.config`): `ExperimentConfig` dataclass
  with TOML loading for reproducible batch experiments.
- **CLI entry point** (`pikit.cli`): `pikit list`, `pikit show`, `pikit run`,
  `pikit matrix` subcommands available after `pip install`.
- **CI workflow** (`.github/workflows/ci.yml`): runs pytest on Python 3.9 /
  3.11 / 3.12 and verifies CLI entry point.
- **CONTRIBUTING.md**: guide for adding new attacks, defenses, channels,
  agents, and target backends.

### Changed

- Version bumped to `0.2.0`.
- `pikit/__init__.py` now exports `Judge`, `JudgeResult`, `RuleJudge`,
  `LLMJudge`, and `ExperimentConfig`.

### Fixed

- `.gitignore` now includes `site/` (MkDocs build output) to prevent
  accidental commits of generated documentation.

## [0.1.0] - 2026-07-02

### Added

- Core architecture: `Attack`, `Defense`, `Channel` base classes with
  decorator-based registry system.
- 9 attacks: naive, escape, context_ignoring, fake_completion, combined,
  payload_splitting, obfuscation, prompt_leaking, prefix_injection.
- 6 prevention defenses: delimiters, sandwich, instructional, spotlighting,
  random_sequence_enclosure, retokenization.
- 6 channels: webpage, document, markdown, code_comment, skills,
  unicode_hidden.
- 4 target backends: OpenAI-compatible, Anthropic, HuggingFace, Mock.
- 6 agents: chat, tool, email, rag, browser, coding.
- `craft()` unified entry point for direct and indirect injection.
- `Trace` / `TraceStep` for human-readable agent run inspection.
- `DefenseHooks` for defense insertion at system / tool_result / user.
- Demo runner (`demos/run.py`) with CLI, TOML config, and interactive modes.
- MkDocs Material documentation site deployed to GitHub Pages.