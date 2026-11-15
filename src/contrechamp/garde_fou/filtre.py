"""Garde-fou : bloque toute sortie qui écrit à la place de l'auteur.

C'est la seconde sécurité de Contrechamp. La première est le prompt système
(``socratique/prompts/systeme.md``), qui demande au modèle de ne poser que des
questions. Mais un modèle peut désobéir : ce filtre relit donc chaque sortie
avant qu'elle n'atteigne l'auteur, sans faire appel au modèle.

Il bloque :

- une réplique au format « NOM : … » ;
- un dialogue entre guillemets ;
- un en-tête de scène INT. ou EXT. ;
- une phrase de description (une phrase affirmative qui raconte l'action) ;
- une sortie trop longue.

Une sortie rejetée renvoie ``socratique.questions`` à une nouvelle génération,
ou à une question de secours. Chaque verdict est noté dans
``transparence.journal``. Les règles et les exemples sont détaillés dans
docs/garde-fou.md ; les cas à couvrir sont dans tests/test_garde_fou.py.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

#: Longueur maximale d'une sortie acceptée, en caractères.
#: À définir pendant le prototype : valeur exacte.
LONGUEUR_MAX: int | None = None


class Motif(str, Enum):
    """Les raisons pour lesquelles une sortie peut être bloquée."""

    REPLIQUE = "replique"            # « LEILA : Je ne partirai jamais. »
    DIALOGUE_GUILLEMETS = "dialogue-guillemets"  # « "Je reste", dit-elle. »
    EN_TETE = "en-tete"              # « INT. MAISON - NUIT »
    DESCRIPTION = "description"      # « Leila entre dans la cuisine. »
    TROP_LONGUE = "trop-longue"
    PAS_UNE_QUESTION = "pas-une-question"


@dataclass(frozen=True)
class Verdict:
    """La décision du filtre sur une sortie du modèle.

    Attributs :
        accepte : True si la sortie peut être montrée à l'auteur.
        motifs : les raisons du rejet (vide si acceptée).

    Le verdict ne garde aucun extrait de la sortie rejetée : celle-ci peut
    contenir du texte de scénario, qui ne doit jamais entrer dans le journal.
    """

    accepte: bool
    motifs: tuple[Motif, ...] = field(default_factory=tuple)


def contient_replique(texte: str) -> bool:
    """Repère une réplique au format « NOM : … » (nom en capitales suivi de deux-points)."""
    raise NotImplementedError


def contient_dialogue_guillemets(texte: str) -> bool:
    """Repère un dialogue entre guillemets (« », " ", “ ”)."""
    raise NotImplementedError


def contient_en_tete(texte: str) -> bool:
    """Repère un en-tête de scène (INT., EXT., INT./EXT.)."""
    raise NotImplementedError


def contient_description(texte: str) -> bool:
    """Repère une phrase de description : une phrase affirmative qui raconte l'action."""
    raise NotImplementedError


def est_trop_longue(texte: str) -> bool:
    """Indique si la sortie dépasse ``LONGUEUR_MAX``."""
    raise NotImplementedError


def est_une_question(texte: str) -> bool:
    """Indique si chaque phrase de la sortie est bien une question."""
    raise NotImplementedError


def verifier(texte: str) -> Verdict:
    """Point d'entrée du module : applique toutes les règles à une sortie.

    Args:
        texte : la sortie brute du modèle.

    Returns:
        Le verdict, avec les motifs du rejet s'il y en a.
    """
    raise NotImplementedError
