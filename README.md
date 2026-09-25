# VayuAGI 6.1

<div align="center">

[![Version](https://img.shields.io/badge/version-6.1.0-0f766e?style=for-the-badge)](https://github.com/Dort-boll/VayuAGI-6.1)
[![Python](https://img.shields.io/badge/python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-16a34a?style=for-the-badge)](LICENSE)
[![CI](https://img.shields.io/github/actions/workflow/status/Dort-boll/VayuAGI-6.1/ci.yml?branch=main&style=for-the-badge&label=CI)](https://github.com/Dort-boll/VayuAGI-6.1/actions)

### Unified, Inspectable Cognitive Architecture

**Multi-path reasoning. Explicit uncertainty. Bounded adaptation. Persistent memory.**

[Quick Start](#quick-start) | [Architecture](#architecture) | [Integration](#python-api) | [Troubleshooting](#troubleshooting)

</div>

---

## Overview

VayuAGI is a local-first cognitive architecture for experimenting with multi-path reasoning, memory, uncertainty correction, and bounded adaptation. It is not a claim of general intelligence or machine consciousness. Every result is inspectable: confidence, evidence, warnings, and corrections are returned as structured data.

### What Makes VayuAGI Different?

| Conventional prototype | VayuAGI 6.1 |
|---|---|
| Ad hoc modules with overlapping responsibilities | Explicit subsystem boundaries and stable interfaces |
| Unchecked generated output | Confidence, evidence, warnings, and correction records |
| Hidden mutable global state | Validated configuration with bounded parameters |
| Memory mixed into reasoning code | Separate working, episodic, and semantic stores |
| Unsafe self-modification | Observable evolution limited to approved parameters |

> Intelligence should be evaluated through evidence, verification, memory, and feedback, not through architectural claims alone.

## Key Features

- **Unified cognitive engine** with synchronous and asynchronous APIs.
- **Multi-mode reasoning** across analytical, creative, intuitive, reflective, and transcendent paths.
- **Error correction** that marks weak results for review instead of inventing certainty.
- **Memory architecture** with bounded working memory, JSONL episodic storage, and contradiction-aware semantic facts.
- **Privacy boundaries** with input limits, normalization, and request-rate protection.
- **Bounded evolution** that can tune configuration only from observed performance signals.
- **Optional GUI** built on the same stable engine contract as the CLI.

## Requirements

The core runtime uses the Python standard library and requires Python 3.10 or newer. No GPU is required for the included local reasoning scaffold. A GPU, model adapter, or cloud service is not assumed by the current implementation.

## Quick Start

```bash
git clone https://github.com/Dort-boll/VayuAGI-6.1.git
cd VayuAGI-6.1
python -m venv .venv
source .venv/bin/activate
python -m pip install -e .
python -m vayu_agi.cli "Design a resilient feedback loop" --mode analytical
```

Launch the optional desktop interface:

```bash
python -m vayu_agi.gui.main
```

Run the complete test suite:

```bash
python -m pip install -e '.[dev]'
python -m pytest -q
```

## Architecture

Each subsystem has one responsibility and communicates through small Python interfaces:

```text
vayu_agi/
├── core/             coordinator, self-monitoring, experience records
├── reasoning/        multi-path insight generation and synthesis
├── memory/           working, episodic, and semantic stores
├── routing/          explicit thinking-mode selection
├── security/         input limits and rate limiting
├── evolution/        observable, bounded configuration changes
├── gui/              optional Tkinter interface
├── config.py         validated single source of truth
└── logger.py         shared logging facade
```

The cognitive engine coordinates these boundaries. Reasoning does not write memory, memory does not mutate configuration, and evolution cannot change executable code.

## Features

- Structured `CognitiveResult` records with confidence, evidence, warnings, and corrections.
- Input normalization, size limits, and request-rate protection.
- Natural, analytical, creative, intuitive, and transcendent routing modes.
- Working-memory context, JSONL episodic memory, and contradiction-aware semantic facts.
- Synchronous and asynchronous engine APIs with one result contract.
- Conservative self-improvement that raises a bounded parameter only when observed correction rates justify it.
- Optional GUI entrypoint that depends only on the stable engine API.
- Python 3.10+ and standard-library runtime dependencies.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e .
python -m vayu_agi.cli "Design a resilient feedback loop" --mode analytical
```

The GUI is optional:

```bash
python -m vayu_agi.gui.main
```

Run tests:

```bash
python -m pytest -q
```

## Python API

```python
from vayu_agi import CognitiveEngine

engine = CognitiveEngine()
result = engine.think("Design a resilient feedback loop")

print(result.synthesis)
print(f"confidence={result.confidence:.1%}")
for correction in result.corrections:
    print(correction.action)
```

For asynchronous applications:

```python
result = await engine.think_async("Review this workflow", mode="reflective")
```

## Error correction

VayuAGI does not invent content to increase confidence. A result is marked for reflection when it has weak evidence or falls below the configured confidence threshold. Invalid and oversized requests return a structured error result instead of escaping as an unhandled exception.

## Configuration

```python
from pathlib import Path
from vayu_agi import VayuConfig

config = VayuConfig(data_dir=Path("./.vayu-data"))
config.cognitive.update_param("analytical_depth", 0.9)
config.save()
```

All cognitive parameters are constrained to `[0, 1]`. Memory and logs are stored beneath `data_dir`.

## Troubleshooting

### The CLI reports low confidence

This is expected for short or underspecified requests. Inspect `result.corrections` and provide more context rather than treating the score as a fact claim.

### The GUI does not launch

The GUI requires a desktop session and Tkinter. On Debian or Ubuntu, install it with `sudo apt install python3-tk`. The CLI and core engine remain usable without a display.

### Tests cannot be found

Install the development extra and run the test module from the repository root:

```bash
python -m pip install -e '.[dev]'
python -m pytest -q
```

### Memory is not appearing

Set an explicit writable directory when constructing `VayuConfig`. Episodic memory is stored as `episodes.jsonl` beneath that configuration directory.

## Quality checks

The project includes unit and architecture tests plus GitHub Actions for Python 3.10, 3.11, and 3.12. Run `git diff --check` before submitting changes.

## License

MIT. See [LICENSE](LICENSE).
