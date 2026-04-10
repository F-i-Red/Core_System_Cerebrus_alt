# modules/anti_capture.py

from dataclasses import dataclass
from typing import List, Dict, Optional, Literal
import time
import random

CaptureType = Literal[
    "propaganda",
    "burocracia",
    "medo",
    "captura_poder",
    "manipulacao",
    "opacidade"
]

Severity = Literal["baixo", "medio", "alto", "critico"]


@dataclass
class CaptureSignal:
    id: str
    type: CaptureType
    source: str           # módulo ou pessoa
    description: str
    severity: Severity
    timestamp: float


@dataclass
class AntiCaptureAction:
    signal_id: str
    action: str
    details: str
    timestamp: float


# --------------------------
# Deteção de padrões
# --------------------------

def detect_propaganda(text: str) -> Optional[CaptureSignal]:
    """
    Deteção simples de propaganda/manipulação.
    """
    keywords = ["inimigo", "traidor", "obrigatório", "única solução", "culpados"]
    if any(k in text.lower() for k in keywords):
        return CaptureSignal(
            id=f"signal_{int(time.time())}",
            type="propaganda",
            source="comunicacao",
            description="Padrões de linguagem manipulativa detectados",
            severity="medio",
            timestamp=time.time()
        )
    return None


def detect_bureaucracy(delay_days: int, steps: int) -> Optional[CaptureSignal]:
    """
    Se um processo tem demasiados passos ou demora excessiva.
    """
    if delay_days > 7 or steps > 5:
        return CaptureSignal(
            id=f"signal_{int(time.time())}",
            type="burocracia",
            source="processo",
            description="Processo excessivamente lento ou complexo",
            severity="alto" if delay_days > 14 else "medio",
            timestamp=time.time()
        )
    return None


def detect_fear_pattern(reports: List[str]) -> Optional[CaptureSignal]:
    """
    Se várias pessoas reportam medo, silêncio ou autocensura.
    """
    fear_words = ["medo", "calar", "não posso falar", "represália"]
    count = sum(1 for r in reports if any(w in r.lower() for w in fear_words))

    if count >= 3:
        return CaptureSignal(
            id=f"signal_{int(time.time())}",
            type="medo",
            source="comunidade",
            description="Padrão de medo sistémico detectado",
            severity="alto",
            timestamp=time.time()
        )
    return None


def detect_power_capture(votes: List[str], threshold: float = 0.8) -> Optional[CaptureSignal]:
    """
    Se um grupo domina votações de forma anómala.
    """
    if not votes:
        return None

    most_common = max(set(votes), key=votes.count)
    ratio = votes.count(most_common) / len(votes)

    if ratio >= threshold:
        return CaptureSignal(
            id=f"signal_{int(time.time())}",
            type="captura_poder",
            source="assembleia",
            description="Grupo dominante detectado em votações",
            severity="critico",
            timestamp=time.time()
        )
    return None


# --------------------------
# Ações corretivas
# --------------------------

def corrective_assembly(signal: CaptureSignal) -> AntiCaptureAction:
    """
    Convoca assembleia de correção.
    """
    return AntiCaptureAction(
        signal_id=signal.id,
        action="assembleia_corretiva",
        details=f"Assembleia convocada para tratar: {signal.type}",
        timestamp=time.time()
    )


def transparency_injection(signal: CaptureSignal) -> AntiCaptureAction:
    """
    Aumenta transparência em módulos capturados.
    """
    return AntiCaptureAction(
        signal_id=signal.id,
        action="transparencia_extra",
        details=f"Logs e decisões do módulo {signal.source} tornados públicos",
        timestamp=time.time()
    )


def civic_force_audit(signal: CaptureSignal) -> AntiCaptureAction:
    """
    Força Cívica faz auditoria física ou processual.
    """
    return AntiCaptureAction(
        signal_id=signal.id,
        action="auditoria_civica",
        details=f"Força Cívica enviada para auditar {signal.source}",
        timestamp=time.time()
    )


# --------------------------
# Pipeline principal
# --------------------------

def process_capture_signal(signal: CaptureSignal) -> List[AntiCaptureAction]:
    """
    Pipeline:
    - assembleia corretiva
    - transparência extra
    - auditoria da Força Cívica
    """

    actions = [
        corrective_assembly(signal),
        transparency_injection(signal),
        civic_force_audit(signal)
    ]

    return actions
