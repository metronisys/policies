import yaml
import json

def load_policy(path):
    if path.endswith(".yml") or path.endswith(".yaml"):
        with open(path) as f:
            return yaml.safe_load(f)["policy"]
    if path.endswith(".json"):
        with open(path) as f:
            return json.load(f)["policy"]
    raise ValueError("Unsupported policy format")


def evaluate_condition(condition, context):
    for key, rule in condition.items():
        value = context.get(key)
        if isinstance(rule, dict):
            if "equals" in rule and value != rule["equals"]:
                return False
            if "less_than" in rule and value >= rule["less_than"]:
                return False
            if "greater_than" in rule and value <= rule["greater_than"]:
                return False
    return True


def evaluate_policy(policy, context):
    for key, condition in policy["conditions"].items():
        if key == "task":
            if not evaluate_condition(condition, context["task"]):
                return None
        else:
            if not evaluate_condition({key: condition}, context):
                return None

    return policy["decision"]


# Example usage
policy = load_policy("energy_guard.yml")
decision = evaluate_policy(policy, context)

if decision:
    print("Governance decision:", decision)
else:
    print("No governance action required")
