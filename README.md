# VayuAGI 6.1

VayuAGI is a local-first, inspectable cognitive architecture for experimenting with multi-path reasoning, memory, uncertainty correction, and bounded adaptation. It is not a claim of general intelligence or machine consciousness.

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

## Quality checks

The project includes unit and architecture tests plus GitHub Actions for Python 3.10, 3.11, and 3.12. Run `git diff --check` before submitting changes.

## License

MIT. See [LICENSE](LICENSE).
