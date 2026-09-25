# VayuAGI 6.1

VayuAGI is a local-first, inspectable cognitive architecture. This repository is a reliable foundation for experimentation, not a claim of general intelligence. It provides one coherent engine contract, structured results, deterministic correction checks, and bounded self-improvement.

## What is implemented

- Typed configuration with validation and input limits.
- Synchronous and asynchronous cognitive APIs with the same result schema.
- Analytical, creative, and reflective insight passes.
- Error correction that flags low confidence, missing insights, and unsafe inputs.
- Thread-safe metrics and a conservative evolution engine.
- A dependency-free CLI suitable for local automation.

The correction layer is deliberately transparent: it does not invent facts to raise a confidence score. It returns a warning and marks the result for review when the evidence is weak.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e .
python -m vayu_agi.cli "How should a system recover from an error?" --mode analytical
```

Run the tests with:

```bash
python -m pytest
```

## Python API

```python
from vayu_agi import CognitiveEngine

engine = CognitiveEngine()
result = engine.think("Design a resilient feedback loop")

print(result.synthesis)
print(result.confidence)
print(result.corrections)
```

## Engineering direction

The next safe extensions are model adapters, persistent memory, and a GUI built against `CognitiveResult`. Those layers should remain optional and must preserve the core guarantees: bounded inputs, explicit uncertainty, observable corrections, and no unreviewed self-modification.

## License

MIT. See [LICENSE](LICENSE).
