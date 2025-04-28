from models import db, Scenario
from scenarios.loader import load_scenarios

def sync_scenarios_to_db():
    scenarios = load_scenarios()
    for scenario_data in scenarios:
        scenario_id = scenario_data["id"]
        scenario = Scenario.query.get(scenario_id)
        if scenario:
            # Update existing scenario
            scenario.name = scenario_data.get("name", scenario.name)
            scenario.description = scenario_data.get("description", scenario.description)
            scenario.status = scenario_data.get("status", scenario.status)
            scenario.html_snippet = scenario_data.get("html_snippet", scenario.html_snippet)
            scenario.js_snippet = scenario_data.get("js_snippet", scenario.js_snippet)
        else:
            # Create new scenario with explicit id
            scenario = Scenario(
                id=scenario_id,
                name=scenario_data.get("name"),
                description=scenario_data.get("description"),
                status=scenario_data.get("status", "pending"),
                html_snippet=scenario_data.get("html_snippet"),
                js_snippet=scenario_data.get("js_snippet"),
            )
            db.session.add(scenario)
    db.session.commit()