# app.py

from flask import Flask, jsonify, request, render_template
from core.engine import CerebrusEngine

app = Flask(__name__)

# Single global engine instance
engine = CerebrusEngine()


# ---------------------------------------------------------
# UI Root
# ---------------------------------------------------------

@app.route("/")
def index():
    """
    Main UI entrypoint.
    Assumes you have a templates/index.html file.
    """
    return render_template("index.html")


# ---------------------------------------------------------
# Housing
# ---------------------------------------------------------

@app.route("/housing/request", methods=["POST"])
def housing_request():
    """
    Demo: assign demo house to demo family.
    """
    result = engine.request_house()

    return jsonify({
        "success": result.success,
        "house_id": result.house_id,
        "family_id": result.family_id,
        "message": result.message,
        "details": result.details
    })


# ---------------------------------------------------------
# Mobility
# ---------------------------------------------------------

@app.route("/mobility/request", methods=["POST"])
def mobility_request():
    """
    Demo: assign a vehicle to a demo transport request.
    """
    result = engine.request_transport()

    return jsonify({
        "success": result.success,
        "vehicle_id": result.vehicle_id,
        "request_id": result.request_id,
        "message": result.message,
        "details": result.details
    })


# ---------------------------------------------------------
# Logistics
# ---------------------------------------------------------

@app.route("/logistics/residue", methods=["POST"])
def logistics_residue():
    """
    Process a residue request.
    Body JSON:
        { "content": "text describing residue" }
    """
    data = request.get_json(silent=True) or {}
    content = data.get("content", "mixed residue")

    scan = engine.send_residue(content=content)

    return jsonify({
        "fraction": scan.fraction,
        "purity": scan.purity,
        "destination": scan.destination,
        "alert": scan.alert
    })


# ---------------------------------------------------------
# Justice
# ---------------------------------------------------------

@app.route("/justice/process/<incident_id>", methods=["POST"])
def justice_process(incident_id):
    """
    Process an incident through the justice pipeline.
    """
    result = engine.process_incident(incident_id=incident_id)

    # If error, return as-is
    if isinstance(result, dict) and "error" in result:
        return jsonify(result), 404

    return jsonify({
        "incident_id": result.incident_id,
        "risk_level": result.risk_level,
        "victim_protection": result.victim_protection,
        "aggressor_restrictions": result.aggressor_restrictions,
        "restorative_process": result.restorative_process,
        "containment": result.containment
    })


# ---------------------------------------------------------
# Civic Force
# ---------------------------------------------------------

@app.route("/civic/intervention", methods=["POST"])
def civic_intervention():
    """
    Create an urgent civic force intervention.
    Body JSON (optional):
        { "description": "...", "location": "Block A" }
    """
    data = request.get_json(silent=True) or {}
    description = data.get("description", "urgent situation")
    location = data.get("location", "Block A")

    result = engine.civic_intervention(description=description, location=location)

    return jsonify({
        "task_id": result["task"].id,
        "assignment_results": result["assignment_results"]
    })


# ---------------------------------------------------------
# Ecology
# ---------------------------------------------------------

@app.route("/ecology/update", methods=["POST"])
def ecology_update():
    """
    Demo: update ecology flows and return panel data.
    """
    panel = engine.update_ecology()
    return jsonify(panel)


# ---------------------------------------------------------
# Sustainability
# ---------------------------------------------------------

@app.route("/sustainability/panel", methods=["GET"])
def sustainability_panel():
    """
    Returns sustainability indicators, score, and alerts.
    """
    result = engine.sustainability_panel()
    return jsonify(result)


@app.route("/sustainability/actions", methods=["GET"])
def sustainability_actions():
    """
    Returns recommended actions for all sustainability alerts.
    """
    result = engine.sustainability_actions()
    return jsonify(result)


@app.route("/sustainability/create_tasks", methods=["POST"])
def sustainability_create_tasks():
    """
    Converts sustainability alerts into Civic Force tasks.
    """
    result = engine.sustainability_to_civic_tasks()
    return jsonify(result)


@app.route("/sustainability/update/<indicator>/<value>", methods=["POST"])
def sustainability_update_indicator(indicator, value):
    """
    Updates a sustainability indicator manually.
    Example:
        POST /sustainability/update/renewable_energy_ratio/0.75
    """
    try:
        value_f = float(value)
    except ValueError:
        return jsonify({"error": "Value must be a float between 0 and 1"}), 400

    engine.sustainability.update_indicator(indicator, value_f)

    return jsonify({
        "status": "updated",
        "indicator": indicator,
        "value": value_f
    })


# ---------------------------------------------------------
# Logs
# ---------------------------------------------------------

@app.route("/logs", methods=["GET"])
def logs():
    """
    Returns all public ledger entries.
    """
    entries = engine.get_logs()
    return jsonify(entries)


# ---------------------------------------------------------
# Main
# ---------------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True)
