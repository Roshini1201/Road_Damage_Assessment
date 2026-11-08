def calculate_severity(area):
    if area < 0.02:
        return "Low"
    elif area < 0.08:
        return "Medium"
    else:
        return "High"


def calculate_priority(severities):
    if not severities:
        return "No Damage Detected"

    if "High" in severities:
        return "High"
    elif "Medium" in severities:
        return "Medium"
    else:
        return "Low"