"""Bonus prévu : transcription des rushes en derja avec FarukSTT.

Une fois le tournage commencé, l'auteur pourra fournir ses rushes (les enregistrements
sonores de son tournage). Ce module prévoit de les transcrire en derja
avec le modèle de reconnaissance vocale FarukSTT, puis de rattacher chaque
transcription à la scène correspondante de ``ingestion.scenario``. L'analyse
(``analyse.narration``) pourra alors comparer ce qui a été écrit et ce qui a
été joué, et ``socratique.questions`` poser des questions sur l'écart.

La transcription se fait en local. Les rushes ne quittent pas l'ordinateur de
l'auteur. Ce module n'est pas prioritaire (voir docs/feuille-de-route.md).
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from contrechamp.ingestion.scenario import Scene


@dataclass(frozen=True)
class SegmentTranscrit:
    """Un passage transcrit d'un rush, avec ses temps de début et de fin (en secondes)."""

    debut_s: float
    fin_s: float
    texte: str


@dataclass
class Rush:
    """Un fichier de rush et sa transcription.

    Attributs :
        chemin : emplacement du fichier sur l'ordinateur de l'auteur.
        scene : numéro de la scène du scénario à laquelle le rush est rattaché,
            ou None si le rattachement n'est pas encore fait.
        segments : la transcription, découpée en passages.
    """

    chemin: Path
    scene: int | None
    segments: list[SegmentTranscrit]


def transcrire(chemin: Path) -> list[SegmentTranscrit]:
    """Transcrit un rush en derja avec FarukSTT, en local.

    Args:
        chemin : l'enregistrement à transcrire.

    Returns:
        Les passages transcrits, dans l'ordre.
    """
    raise NotImplementedError


def rattacher_a_scene(rush: Rush, scenes: list[Scene]) -> int | None:
    """Trouve la scène du scénario qui correspond le mieux à un rush transcrit.

    Args:
        rush : le rush transcrit.
        scenes : les scènes produites par ``ingestion.scenario``.

    Returns:
        Le numéro de la scène retenue, ou None si aucune ne correspond.
    """
    raise NotImplementedError

