"""Interface web prévue.

Une page web locale, ouverte dans le navigateur de l'auteur. Elle permet :

- d'envoyer une scène ou un scénario complet (``ingestion.scenario``) ;
- de lire les questions, chacune avec sa page et sa scène ;
- d'ignorer une question, d'en demander plus ou de demander le silence
  (``autonomie.regulateur``) ;
- de choisir le moteur, local par défaut, et de donner ou retirer son accord
  pour le mode API (``llm.moteurs``) ;
- de consulter le journal et la consommation de la session
  (``transparence.journal`` et ``transparence.mesure``).

L'interface n'a jamais de zone où Contrechamp écrit dans le scénario : le
texte n'est modifiable que par l'auteur.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from contrechamp.autonomie.regulateur import EtatAutonomie
from contrechamp.ingestion.scenario import Scenario
from contrechamp.llm.moteurs import ConfigMoteur
from contrechamp.socratique.questions import Question


@dataclass
class Session:
    """L'état d'une session d'écriture dans l'interface."""

    identifiant: str
    config: ConfigMoteur
    scenario: Scenario | None = None
    questions: list[Question] = field(default_factory=list)
    autonomie: EtatAutonomie = field(default_factory=EtatAutonomie)


def nouvelle_session() -> Session:
    """Crée une session avec le moteur local par défaut."""
    raise NotImplementedError


def traiter_scene(session: Session, texte: str) -> list[Question]:
    """Reçoit une scène de l'auteur et renvoie les questions à afficher.

    Enchaîne : découpage, analyse, génération, garde-fou, journal.

    Args:
        session : la session en cours.
        texte : la scène envoyée par l'auteur.

    Returns:
        Les questions, chacune avec sa page et sa scène.
    """
    raise NotImplementedError


def lancer() -> None:
    """Démarre l'interface web locale."""
    raise NotImplementedError
