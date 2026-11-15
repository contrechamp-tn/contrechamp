"""Régulateur d'autonomie : moins de questions à mesure que l'auteur progresse.

Le but de Contrechamp est que l'auteur n'en ait plus besoin. Ce module suit
la session (questions ignorées, réécritures faites par l'auteur, scènes
avancées sans aide) et décide combien de questions ``socratique.questions``
doit poser sur la scène suivante. Plus l'auteur avance seul, plus Contrechamp
se tait.

L'auteur garde la main : il peut ignorer une question, demander le silence, ou
demander plus de questions. Le régulateur ne lit que des signaux d'usage
gardés en local ; il ne juge jamais la qualité du texte.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class Reaction(str, Enum):
    """Ce que l'auteur a fait d'une question."""

    IGNOREE = "ignoree"
    REECRITURE = "reecriture"        # l'auteur a modifié sa scène après la question
    DEMANDE_PLUS = "demande-plus"
    DEMANDE_SILENCE = "demande-silence"


@dataclass
class EtatAutonomie:
    """L'état de la session, du point de vue de l'autonomie.

    Attributs :
        questions_posees : nombre de questions affichées depuis le début.
        reactions : ce que l'auteur a fait de chaque question.
        scenes_sans_aide : scènes écrites ou réécrites sans avoir demandé de question.
        niveau : estimation de l'autonomie, de 0 (débutant) à 1 (autonome).
    """

    questions_posees: int = 0
    reactions: list[Reaction] = field(default_factory=list)
    scenes_sans_aide: int = 0
    niveau: float = 0.0


def enregistrer_reaction(etat: EtatAutonomie, reaction: Reaction) -> EtatAutonomie:
    """Met à jour l'état après une réaction de l'auteur.

    Args:
        etat : l'état actuel.
        reaction : ce que l'auteur a fait de la dernière question.

    Returns:
        Le nouvel état.
    """
    raise NotImplementedError


def nombre_de_questions(etat: EtatAutonomie) -> int:
    """Décide combien de questions poser sur la prochaine scène.

    Le nombre baisse quand le niveau d'autonomie monte, et tombe à zéro si
    l'auteur a demandé le silence.

    Args:
        etat : l'état actuel de la session.

    Returns:
        Le nombre de questions (0 ou plus).
    """
    raise NotImplementedError
