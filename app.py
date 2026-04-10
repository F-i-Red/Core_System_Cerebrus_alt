from flask import Flask, jsonify, send_from_directory
from core.engine import CerebrusEngine
from main import setup_engine  # reutilizamos o setup do main

app = Flask(__name__)
engine = setup_engine()

# --------------------------
# Endpoints
# --------------------------

@app.get("/")
def serve_index():
    return send_from_directory("static", "index.html")

@app.get("/request_house")
def request_house():
    result = engine.request_house("casa1", "fam1", "FIXA")
    return jsonify(result.__dict__)

@app.get("/request_transport")
def request_transport():
    result = engine.request_mobility("p1", "blocoA", "centro")
    return jsonify(result.__dict__)

@app.get("/send_residue")
def send_residue():
    result = engine.submit_logistics_request(
        req_id="req_web",
        person_id="p1",
        req_type="residuo",
        content="sangue e tecido",
        location="blocoA"
    )
    return jsonify(result.__dict__)

@app.get("/process_incident")
def process_incident():
    actions = engine.process_incident("incident_req_web")
    return jsonify([a.__dict__ for a in actions])

@app.get("/civic_intervention")
def civic_intervention():
    msg = engine.dispatch_civic_force("incident_req_web")
    return jsonify({"message": msg})

@app.get("/update_ecology")
def update_ecology():
    from modules.ecology import EcoBlock, ResourceFlow, update_flow, ecology_to_panel

    block = EcoBlock(
        id="blocoA",
        name="Bloco A",
        flows={
            "agua": ResourceFlow("agua"),
            "energia": ResourceFlow("energia"),
            "residuos": ResourceFlow("residuos"),
            "co2": ResourceFlow("co2")
        }
    )

    update_flow(block, "agua", consumed=20, regenerated=10)
    update_flow(block, "energia", consumed=15, regenerated=30)
    update_flow(block, "residuos", consumed=5, regenerated=5)
    update_flow(block, "co2", consumed=0, regenerated=0)

    panel_data = ecology_to_panel(block)
    engine.update_panel("blocoA", panel_data)

    return jsonify(panel_data)

@app.get("/vote")
def vote():
    from modules.education import Proposal, Vote
    proposal = Proposal(
        id="prop_web",
        title="Jardim Vertical",
        description="Criar jardim vertical",
        context="educacao"
    )
    votes = [
        Vote("prop_web", "p1", True),
        Vote("prop_web", "p2", False)
    ]
    result = engine.tally_proposal_votes(proposal, votes)
    return jsonify(result.__dict__)

@app.get("/logs")
def logs():
    logs = engine.ledger.get_public_logs()
    return jsonify([l.__dict__ for l in logs])


if __name__ == "__main__":
    app.run(debug=True)
