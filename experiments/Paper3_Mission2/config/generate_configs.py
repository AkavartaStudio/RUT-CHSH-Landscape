#!/usr/bin/env python3
"""
Generate individual experiment configs by merging base with overrides.
"""
import json
import copy
from pathlib import Path

def deep_merge(base: dict, override: dict) -> dict:
    """Recursively merge override into base."""
    result = copy.deepcopy(base)
    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = copy.deepcopy(value)
    return result

def main():
    config_dir = Path(__file__).parent

    # Load base and overrides
    with open(config_dir / "base_M2_E3xx.json") as f:
        base = json.load(f)

    with open(config_dir / "overrides_M2_E3xx.json") as f:
        overrides = json.load(f)

    # Generate individual configs
    for exp_id, exp_overrides in overrides.items():
        config = deep_merge(base, exp_overrides)
        config["experiment_id"] = exp_id

        # Update base_seed to match experiment number
        exp_num = int(exp_id[1:])  # E301 -> 301
        if "initial_conditions" not in config:
            config["initial_conditions"] = {}
        config["initial_conditions"]["base_seed"] = exp_num

        # Write individual config
        output_path = config_dir / f"{exp_id}.json"
        with open(output_path, "w") as f:
            json.dump(config, f, indent=2)
        print(f"Generated: {output_path.name}")

if __name__ == "__main__":
    main()
