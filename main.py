# main.py

from core.engine import CerebrusEngine
from core.types import Family, House
from modules import education, ecology, justice


def setup_engine():
    engine = CerebrusEngine()

    # --------------------------
    # Famílias
    # --------------------------
    engine.families["fam1"] = Family(
        id="fam1",
        members=["p1"],
        joule_credits=120,
        social_relevance_tags=["idosos_presentes"]
    )

    engine.families["fam2"] = Family(
        id="fam2",
        members=["p2"],
        joule_credits=80,
        social_relevance_tags=[]
    )

    # --------------------------
    # Casas
    # --------------------------
    engine.houses["casa1"] = House(
        id="casa1",
        block_id="blocoA",
        type="FIXA",
        capacity=3
    )

    engine.houses["casa2"] = House(
        id="casa2",
        block_id="blocoA",
        type="SUPLENTE",
        capacity=2
    )

    # --------------------------
    # Frota
    # --------------------------
    from modules.mobility import Vehicle

    engine.fleet["v1"] = Vehicle(
        id="v1",
        type="carro_autonomo",
        status="operacional",
        ownership="publico",
        location="blocoA"
    )

    engine.fleet["v2"] = Vehicle(
        id="v2",
        type="reboque",
        status="operacional",
        ownership="publico",
        location="blocoA"
    )

    # --------------------------
    # Força Cívica
    # --------------------------
    from modules.civic_force import CivicForceMember

    engine.civic_members["fc1"] = CivicForceMember(
        id="fc1",
        name="Ana Silva",
        skills=["seguranca", "ecologia"],
        available=True,
        location="blocoA"
    )

    # --------------------------
    # Educação
    # --------------------------
    engine.institutions["escolaA"] = education.Institution(
        id="escolaA",
        name="Escola do Bairro A",
        type="escola",
        location="blocoA",
        members=["p1"]
    )

    engine.specializations["p1"] = education.Specialization(
        person_id="p1",
        tags=["educacao"]
    )

    engine.curriculum_paths["cur1"] = education.CurriculumPath(
        id="cur1",
        name="Formação Restaurativa",
        required_tags=["restaurativa"],
        duration_months=6,
        grants_civic_force_access=True
    )

    # --------------------------
    # Ecologia
    # --------------------------
    engine.panels["blocoA"] = None  # será criado automaticamente

    return engine


def run_simulation(engine: CerebrusEngine):

    print("\n=== 1) Pedido de Casa ===")
    result = engine.request_house("casa1", "fam1", "FIXA")
    print(result)

    print("\n=== 2) Pedido de Transporte ===")
    mob = engine.request_mobility("p1", "blocoA", "centro")
    print(mob)

    print("\n=== 3) Resíduo com matéria orgânica anómala ===")
    res = engine.submit_logistics_request(
        req_id="req1",
        person_id="p1",
        req_type="residuo",
        content="sangue e tecido",
        location="blocoA"
    )
    print(res)

    print("\n=== 4) Processar incidente de justiça ===")
    actions = engine.process_incident("incident_req1")
    for a in actions:
        print(a)

    print("\n=== 5) Força Cívica intervém ===")
    msg = engine.dispatch_civic_force("incident_req1")
    print(msg)

    print("\n=== 6) Atualizar painel ecológico ===")
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
    print(panel_data)

    print("\n=== 7) Votação numa proposta ===")
    proposal = education.Proposal(
        id="prop1",
        title="Novo Jardim Vertical",
        description="Criar jardim vertical no Bloco A",
        context="educacao"
    )

    votes = [
        education.Vote("prop1", "p1", True),
        education.Vote("prop1", "p2", False)
    ]

    tally = engine.tally_proposal_votes(proposal, votes)
    print(tally)

    print("\n=== 8) Logs públicos ===")
    for log in engine.ledger.get_public_logs():
        print(log)


if __name__ == "__main__":
    engine = setup_engine()
    run_simulation(engine)
