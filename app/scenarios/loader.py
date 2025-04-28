import os
import yaml

SCENARIO_DIR = os.path.join(os.path.dirname(__file__), "definitions")

def load_scenarios():
    scenarios = []
    for fname in sorted(os.listdir(SCENARIO_DIR)):
        if fname.endswith(".yaml"):
            with open(os.path.join(SCENARIO_DIR, fname), "r", encoding="utf-8") as f:
                scenario = yaml.safe_load(f)
                scenarios.append(scenario)
    return scenarios

def get_scenario_by_id(scenario_id):
    for scenario in load_scenarios():
        if scenario["id"] == scenario_id:
            return scenario
    return None

def get_all_scenarios():
    """Alias for load_scenarios, for compatibility with existing code."""
    return load_scenarios()
