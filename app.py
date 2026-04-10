from flask import Flask, jsonify, send_from_directory
from core.engine import CerebrusEngine
from main import setup_engine

app = Flask(__name__)
engine = setup_engine()

# ---------------------------------------------------------
# Serve the Web Interface
# ---------------------------------------------------------

@app.get("/")
def serve_index():
    return send_from_directory("static", "index.html")


# ---------------------------------------------------------
# Housing
# ---------------------------------------------------------

@app.get("/request_house")
def request_house():
    """
    Assign a house to a family (demo request).
    """
    result = engine.request_house("casa1", "fam1", "FIXED")
    return jsonify(result.__dict__)


# ---------------------------------------------------------
# Mobility
# ---------------------------------------------------------

@app.get("/request_transport")
def request_transport():
    """
    Request a transport vehicle for a person.
    """
    result = engine.request_mobility("p1", "blockA", "center")
    return jsonify(result.__dict__)


# ---------------------------------------------------------
# Logistics (Residue / Delivery)
# ---------------------------------------------------------

@app.get("/send_residue")
def send_residue():
    """
    Send a residue request (may trigger an incident).
    """
    result = engine.submit_logistics_request(
        req_id="req_web",
        person_id="p1",
        req_type="residue",
        content="blood and tissue",
        location="blockA"
    )
    return jsonify(result.__dict__)


# ---------------------------------------------------------
# Justice
# ---------------------------------------------------------

@app.get("/process_incident")
def process_incident():
    """
    Process an existing incident created by residue anomaly.
    """
    incident_id = "incident_req_web"
    actions = engine.process_incident(incident_id)
    return jsonify([a.__dict__ for a in actions])


# ---------------------------------------------------------
# Civic Force
# ---------------------------------------------------------

@app.get("/civic_intervention")
def civic_intervention():
    """
    Trigger a Civic Force intervention for the incident.
    """
    incident_id = "incident_req_web"
    msg = engine.dispatch_civic_force(incident_id)
    return jsonify({"message": msg})


# ---------------------------------------------------------
# Ecology
# ---------------------------------------------------------

@app.get("/update_ecology")
def update_ecology():
    """
    Update ecological data for block A and refresh the public panel.
    """
    from modules.ecology import EcoBlock, ResourceFlow, update_flow, ecology_to_panel

    block = EcoBlock(
        id="blockA",
        name="Block A",
        flows={
            "water": ResourceFlow("water"),
            "energy": ResourceFlow("energy"),
            "waste": ResourceFlow("waste"),
            "co2": ResourceFlow("co2")
        }
    )

    update_flow(block, "water", consumed=20, regenerated=10)
    update_flow(block, "energy", consumed=15, regenerated=30)
    update_flow(block, "waste", consumed=5, regenerated=5)
    update_flow(block, "co2", consumed=0, regenerated=0)

    panel_data = ecology_to_panel(block)
    engine.update_panel("blockA", panel_data)

    return jsonify(panel_data)


# ---------------------------------------------------------
# Education (Voting)
# ---------------------------------------------------------

@app.get("/vote")
def vote():
    """
    Perform a weighted vote on a proposal.
    """
    from modules.education import Proposal, Vote

    proposal = Proposal(
        id="prop_web",
        title="Vertical Garden",
        description="Create a vertical garden in Block A",
        context="education"
    )

    votes = [
        Vote("prop_web", "p1", True),
        Vote("prop_web", "p2", False)
    ]

    result = engine.tally_proposal_votes(proposal, votes)
    return jsonify(result.__dict__)


# ---------------------------------------------------------
# Public Logs
# ---------------------------------------------------------

@app.get("/logs")
def logs():
    """
    Return all public ledger logs.
    """
    logs = engine.ledger.get_public_logs()
    return jsonify([l.__dict__ for l in logs])


# ---------------------------------------------------------
# Run Server
# ---------------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True)
