"""Command-line entry point for VayuAGI."""

import argparse
import json

from .core.cognitive_engine import CognitiveEngine


def main() -> None:
    parser = argparse.ArgumentParser(description="Inspect a VayuAGI cognitive result")
    parser.add_argument("signal", help="Text to analyze")
    parser.add_argument("--mode", default="natural", choices=("natural", "analytical", "creative", "reflective"))
    args = parser.parse_args()
    print(json.dumps(CognitiveEngine().think(args.signal, args.mode).as_dict(), indent=2))


if __name__ == "__main__":
    main()