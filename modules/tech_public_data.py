# modules/tech_public_data.py

from dataclasses import dataclass
from typing import Dict, List, Optional, Literal
import time
import hashlib
import json


# --------------------------
# Tipos base
# --------------------------

LogVisibility = Literal["publico", "privado", "anonimizado"]

@dataclass
class AuditLog:
    id: str
    timestamp: float
    module: str
    action: str
    details: dict
    visibility: LogVisibility = "publico"


@dataclass
class EncryptedData:
    owner_id: str
    encrypted_blob: str


@dataclass
class Explanation:
    module: str
    action: str
    reasoning: str
    inputs_used: List[str]


# --------------------------
# Encriptação simples (placeholder)
# --------------------------

def encrypt_data(owner_id: str, data: dict) -> EncryptedData:
    """
    Encriptação simbólica (placeholder).
    """
    blob = json.dumps(data)
    encrypted = hashlib.sha256(blob.encode()).hexdigest()
    return EncryptedData(owner_id=owner_id, encrypted_blob=encrypted)


def verify_owner(owner_id: str, encrypted: EncryptedData) -> bool:
    return owner_id == encrypted.owner_id


# --------------------------
# Logs públicos e auditáveis
# --------------------------

class PublicLedger:
    """
    Livro-razão público: cada módulo regista ações importantes.
    """

    def __init__(self):
        self.logs: Dict[str, AuditLog] = {}

    def add_log(self, module: str, action: str, details: dict, visibility: LogVisibility = "publico"):
        log_id = f"log_{len(self.logs)+1}"
        entry = AuditLog(
            id=log_id,
            timestamp=time.time(),
            module=module,
            action=action,
            details=details,
            visibility=visibility
        )
        self.logs[log_id] = entry
        return entry

    def get_public_logs(self) -> List[AuditLog]:
        return [l for l in self.logs.values() if l.visibility == "publico"]

    def get_logs_for_owner(self, owner_id: str) -> List[AuditLog]:
        """
        Logs privados só podem ser vistos pelo dono.
        """
        return [
            l for l in self.logs.values()
            if l.visibility == "privado" and l.details.get("owner_id") == owner_id
        ]


# --------------------------
# IA auditável e explicável
# --------------------------

def explain_decision(module: str, action: str, inputs: dict, reasoning: str) -> Explanation:
    """
    Cada decisão automatizada deve gerar uma explicação.
    """
    return Explanation(
        module=module,
        action=action,
        reasoning=reasoning,
        inputs_used=list(inputs.keys())
    )


# --------------------------
# Painéis de bairro
# --------------------------

@dataclass
class NeighborhoodPanel:
    id: str
    public_data: dict  # ex: consumos, resíduos, mobilidade, projetos
    last_update: float = 0.0

    def update(self, new_data: dict):
        self.public_data.update(new_data)
        self.last_update = time.time()


# --------------------------
# API ética
# --------------------------

class EthicalAPI:
    """
    API que só permite:
    - dados públicos
    - dados anonimizados
    - dados privados com consentimento
    """

    def __init__(self, ledger: PublicLedger):
        self.ledger = ledger

    def request_public_data(self, panel: NeighborhoodPanel):
        self.ledger.add_log(
            module="tech_public_data",
            action="request_public_data",
            details={"panel_id": panel.id},
            visibility="publico"
        )
        return panel.public_data

    def request_private_data(self, encrypted: EncryptedData, requester_id: str):
        if verify_owner(requester_id, encrypted):
            self.ledger.add_log(
                module="tech_public_data",
                action="request_private_data",
                details={"owner_id": requester_id},
                visibility="privado"
            )
            return encrypted.encrypted_blob
        else:
            self.ledger.add_log(
                module="tech_public_data",
                action="unauthorized_access_attempt",
                details={"attempted_by": requester_id},
                visibility="publico"
            )
            return None

    def request_anon_data(self, panel: NeighborhoodPanel):
        self.ledger.add_log(
            module="tech_public_data",
            action="request_anon_data",
            details={"panel_id": panel.id},
            visibility="publico"
        )
        # devolve apenas dados agregados
        return {k: v for k, v in panel.public_data.items() if not isinstance(v, dict)}
