"""
Anti-Capture Module
-------------------

This module acts as the immune system of the Cerebrus Engine.
It detects patterns of institutional capture, manipulation, opacity,
fear dynamics, and bureaucratic stagnation.

When a capture signal is detected, the module triggers corrective actions:
- Restorative or corrective assemblies
- Transparency injections
- Civic Force audits

This is a simplified but functional model of systemic anti-capture logic.
"""

from dataclasses import dataclass
from typing import List, Dict, Any, Optional


# ---------------------------------------------------------
# Data Models
# ---------------------------------------------------------

@dataclass
class CaptureSignal:
    """
    Represents a detected capture signal.

    Types include:
    - propaganda
    - bureaucracy
    - fear
    - power_capture
    - opacity
    - manipulation
    """
    type: str
    severity: str  # "low", "medium", "high"
    description: str
    metadata: Optional[Dict[str, Any]] = None


# ---------------------------------------------------------
# Anti-Capture Module
# ---------------------------------------------------------

class AntiCaptureModule:
    """
    Core anti-capture module.

    Detects:
    - Manipulative language (propaganda)
    - Excessive bureaucracy
    - Fear patterns in reports
    - Power concentration in voting
    - Opacity in decision-making

    Responds with:
    - Corrective assemblies
    - Transparency injections
    - Civic Force audits
    """

    # -----------------------------------------------------
    # Detection Methods
    # -----------------------------------------------------

    def detect_propaganda(self, text: str) -> Optional[CaptureSignal]:
        """
        Detects manipulative or propagandistic language.

        Keywords are simplified for demonstration.
        """

        propaganda_keywords = [
            "enemy", "traitor", "purity", "absolute truth",
            "only we", "everyone else", "threat", "corrupt"
        ]

        if any(k in text.lower() for k in propaganda_keywords):
            return CaptureSignal(
                type="propaganda",
                severity="medium",
                description="Detected manipulative or polarizing language.",
                metadata={"text": text}
            )

        return None

    def detect_bureaucracy(self, delay_days: int, steps: int) -> Optional[CaptureSignal]:
        """
        Detects excessive bureaucracy based on delays and number of steps.
        """

        if delay_days > 30 or steps > 10:
            return CaptureSignal(
                type="bureaucracy",
                severity="high" if delay_days > 60 else "medium",
                description="Detected excessive bureaucratic delay.",
                metadata={"delay_days": delay_days, "steps": steps}
            )

        return None

    def detect_fear_pattern(self, reports: List[str]) -> Optional[CaptureSignal]:
        """
        Detects fear or silence patterns in community reports.
        """

        fear_keywords = ["afraid", "fear", "unsafe", "threatened", "silence"]

        count = sum(1 for r in reports if any(k in r.lower() for k in fear_keywords))

        if count >= 3:
            return CaptureSignal(
                type="fear",
                severity="high",
                description="Detected fear pattern in community reports.",
                metadata={"reports": reports}
            )

        return None

    def detect_power_capture(self, votes: List[Dict[str, Any]]) -> Optional[CaptureSignal]:
        """
        Detects concentration of power in voting patterns.

        Example:
        If one group consistently dominates >70% of weighted votes.
        """

        group_totals = {}

        for v in votes:
            group = v.get("group", "unknown")
            weight = v.get("weight", 1.0)
            group_totals[group] = group_totals.get(group, 0) + weight

        total = sum(group_totals.values())

        for group, w in group_totals.items():
            if w / total > 0.7:
                return CaptureSignal(
                    type="power_capture",
                    severity="high",
                    description=f"Detected power concentration in group '{group}'.",
                    metadata={"group": group, "weight_share": w / total}
                )

        return None

    def detect_opacity(self, missing_logs: int) -> Optional[CaptureSignal]:
        """
        Detects opacity based on missing or incomplete logs.
        """

        if missing_logs > 5:
            return CaptureSignal(
                type="opacity",
                severity="medium",
                description="Detected missing or incomplete logs.",
                metadata={"missing_logs": missing_logs}
            )

        return None

    # -----------------------------------------------------
    # Corrective Actions
    # -----------------------------------------------------

    def corrective_assembly(self, signal: CaptureSignal) -> Dict[str, Any]:
        """
        Creates a corrective assembly to address systemic issues.
        """

        return {
            "action": "corrective_assembly",
            "focus": signal.type,
            "severity": signal.severity,
            "description": signal.description
        }

    def transparency_injection(self, signal: CaptureSignal) -> Dict[str, Any]:
        """
        Forces additional transparency in the affected module.
        """

        return {
            "action": "transparency_injection",
            "target": signal.type,
            "details": signal.metadata
        }

    def civic_force_audit(self, signal: CaptureSignal) -> Dict[str, Any]:
        """
        Requests a Civic Force audit for high-severity signals.
        """

        return {
            "action": "civic_force_audit",
            "priority": 3,
            "required_skills": ["inspection", "justice"],
            "location": "Block A",
            "signal": signal.type
        }

    # -----------------------------------------------------
    # Full Processing Pipeline
    # -----------------------------------------------------

    def process_capture_signal(self, signal: CaptureSignal) -> Dict[str, Any]:
        """
        Processes a capture signal and triggers corrective actions.

        Returns:
            dict: structured result for logging and UI.
        """

        actions = [
            self.corrective_assembly(signal),
            self.transparency_injection(signal)
        ]

        if signal.severity == "high":
            actions.append(self.civic_force_audit(signal))

        return {
            "signal_type": signal.type,
            "severity": signal.severity,
            "actions": actions
        }
