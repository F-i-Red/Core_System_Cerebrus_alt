"""
Public Data & Transparency Module
---------------------------------

This module implements the transparency layer of the Cerebrus Engine.
It provides:

- A public ledger for all modules
- Public, private, and anonymized logging
- A unified interface for requesting data
- Explanations for automated decisions

The philosophy:
Every action taken by the system must be traceable, explainable,
and accessible at the appropriate visibility level.
"""

from dataclasses import dataclass
from typing import Any, Dict, List, Optional


# ---------------------------------------------------------
# Data Models
# ---------------------------------------------------------

@dataclass
class LedgerEntry:
    """
    Represents a single entry in the public ledger.

    Visibility levels:
    - public: visible to everyone
    - private: visible only to the owner
    - anon: anonymized aggregate data
    """
    module: str
    action: str
    details: Dict[str, Any]
    visibility: str  # "public", "private", "anon"


@dataclass
class Explanation:
    """
    Represents an explanation for an automated decision.

    Includes:
    - reasoning: human-readable explanation
    - inputs_used: data that influenced the decision
    """
    reasoning: str
    inputs_used: Dict[str, Any]


# ---------------------------------------------------------
# Public Ledger
# ---------------------------------------------------------

class PublicLedger:
    """
    Central ledger for all modules.

    Stores:
    - Public actions
    - Private actions
    - Anonymized actions

    Provides:
    - append()
    - get_public()
    - get_private(owner_id)
    - get_anon()
    """

    def __init__(self):
        self.entries: List[LedgerEntry] = []

    def append(self, module: str, action: str, details: Dict[str, Any], visibility: str = "public") -> None:
        """
        Appends a new entry to the ledger.
        """

        entry = LedgerEntry(
            module=module,
            action=action,
            details=details,
            visibility=visibility
        )

        self.entries.append(entry)

    def get_public(self) -> List[Dict[str, Any]]:
        """Returns all public ledger entries."""
        return [
            {
                "module": e.module,
                "action": e.action,
                "details": e.details
            }
            for e in self.entries if e.visibility == "public"
        ]

    def get_private(self, owner_id: str) -> List[Dict[str, Any]]:
        """Returns private entries belonging to a specific owner."""
        return [
            {
                "module": e.module,
                "action": e.action,
                "details": e.details
            }
            for e in self.entries
            if e.visibility == "private" and e.details.get("owner_id") == owner_id
        ]

    def get_anon(self) -> List[Dict[str, Any]]:
        """Returns anonymized entries."""
        return [
            {
                "module": e.module,
                "action": e.action,
                "summary": "anonymized_data"
            }
            for e in self.entries if e.visibility == "anon"
        ]


# ---------------------------------------------------------
# Ethical API Layer
# ---------------------------------------------------------

class EthicalAPI:
    """
    Ethical API wrapper for the Cerebrus Engine.

    Provides:
    - request_public_data()
    - request_private_data()
    - request_anon_data()
    - explain_decision()

    Ensures:
    - Privacy
    - Transparency
    - Auditability
    """

    def __init__(self, ledger: PublicLedger):
        self.ledger = ledger

    # -----------------------------------------------------
    # Public Data
    # -----------------------------------------------------

    def request_public_data(self, module: str) -> List[Dict[str, Any]]:
        """
        Returns public data for a module and logs the request.
        """

        self.ledger.append(
            module="tech_public_data",
            action="public_data_request",
            details={"requested_module": module},
            visibility="public"
        )

        return self.ledger.get_public()

    # -----------------------------------------------------
    # Private Data
    # -----------------------------------------------------

    def request_private_data(self, owner_id: str) -> List[Dict[str, Any]]:
        """
        Returns private data belonging to the owner.

        Logs unauthorized attempts as public warnings.
        """

        private_data = self.ledger.get_private(owner_id)

        if not private_data:
            self.ledger.append(
                module="tech_public_data",
                action="unauthorized_access_attempt",
                details={"owner_id": owner_id},
                visibility="public"
            )
            return []

        self.ledger.append(
            module="tech_public_data",
            action="private_data_request",
            details={"owner_id": owner_id},
            visibility="private"
        )

        return private_data

    # -----------------------------------------------------
    # Anonymized Data
    # -----------------------------------------------------

    def request_anon_data(self) -> List[Dict[str, Any]]:
        """
        Returns anonymized data for aggregate analysis.
        """

        self.ledger.append(
            module="tech_public_data",
            action="anon_data_request",
            details={},
            visibility="public"
        )

        return self.ledger.get_anon()

    # -----------------------------------------------------
    # Explanations
    # -----------------------------------------------------

    def explain_decision(self, reasoning: str, inputs_used: Dict[str, Any]) -> Explanation:
        """
        Returns a structured explanation for an automated decision.
        """

        explanation = Explanation(
            reasoning=reasoning,
            inputs_used=inputs_used
        )

        self.ledger.append(
            module="tech_public_data",
            action="explanation_generated",
            details={"reasoning": reasoning},
            visibility="public"
        )

        return explanation
