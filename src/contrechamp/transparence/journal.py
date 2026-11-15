"""Journal local de chaque question posée.

Chaque question affichée à l'auteur est notée ici, avec sa source (page et
scène), le moteur utilisé, la décision du garde-fou et la mesure de
consommation. Le journal permet à l'auteur de savoir d'où vient chaque
question et de vérifier que Contrechamp n'a jamais écrit à sa place.

Le journal ne contient jamais le texte du scénario, ni celui des sorties
rejetées par le garde-fou : seulement la page, la scène, la question, le
moteur, l'heure et la mesure, avec la décision du garde-fou.

Le journal est un fichier JSONL (une ligne JSON par entrée) rangé dans le
dossier choisi dans .env (``CONTRECHAMP_DOSSIER_JOURNAL``). Il reste sur
l'ordinateur de l'auteur, qui peut le lire, l'exporter ou l'effacer. Le format
est décrit dans docs/formats.md.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from contrechamp.garde_fou.filtre import Verdict
from contrechamp.socratique.questions import Question
from contrechamp.transparence.mesure import Mesure


@dataclass(frozen=True)
class EntreeJournal:
    """Une ligne du journal.

    Attributs :
        horodatage : date et heure de la question.
        session : identifiant de la session d'écriture.
        question : la question affichée, avec sa page, sa scène et son moteur.
        verdict : la décision du garde-fou sur la première sortie du modèle
            (accepté ou non, et motifs ; jamais le texte rejeté).
        tentatives : nombre de générations nécessaires (1 si acceptée d'emblée).
        secours : True si la question affichée est une question de secours.
        mesure : la consommation cumulée des tentatives.
    """

    horodatage: datetime
    session: str
    question: Question
    verdict: Verdict
    tentatives: int
    secours: bool
    mesure: Mesure


class Journal:
    """Accès au fichier JSONL du journal, sur l'ordinateur de l'auteur."""

    def __init__(self, dossier: Path) -> None:
        """Ouvre (ou crée) le journal dans le dossier donné."""
        raise NotImplementedError

    def ecrire(self, entree: EntreeJournal) -> None:
        """Ajoute une entrée à la fin du journal."""
        raise NotImplementedError

    def lire(self, session: str | None = None) -> list[EntreeJournal]:
        """Relit le journal, pour une session ou en entier."""
        raise NotImplementedError

    def effacer(self) -> None:
        """Efface tout le journal, à la demande de l'auteur."""
        raise NotImplementedError


def vers_json(entree: EntreeJournal) -> str:
    """Convertit une entrée en une ligne JSON (format décrit dans docs/formats.md)."""
    raise NotImplementedError


def depuis_json(ligne: str) -> EntreeJournal:
    """Relit une ligne JSON du journal."""
    raise NotImplementedError
