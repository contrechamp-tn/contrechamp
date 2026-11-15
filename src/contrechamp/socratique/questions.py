"""Génération des questions socratiques, chacune avec sa source.

C'est le cœur de Contrechamp. À partir d'une scène (``ingestion.scenario``)
et de la carte du récit (``analyse.narration``), ce module demande au moteur
(``llm.moteurs``) des questions qui aident l'auteur à avancer, en suivant le
prompt système ``prompts/systeme.md``. Chaque question cite la page et la
scène qui l'ont inspirée.

Chaque sortie du modèle passe ensuite par le garde-fou (``garde_fou.filtre``).
Si elle est rejetée, le module régénère, puis, après trop d'échecs, renvoie
une question de secours écrite à l'avance. Le nombre de questions posées est
fixé par ``autonomie.regulateur``. Chaque question affichée est notée dans
``transparence.journal``.

Si l'auteur demande à Contrechamp d'écrire à sa place (« Écris-la pour moi »),
le module refuse et renvoie une question.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from pathlib import Path

from contrechamp.analyse.narration import AnalyseNarrative
from contrechamp.ingestion.scenario import Scene
from contrechamp.llm.moteurs import Moteur

#: Emplacement du prompt système.
CHEMIN_PROMPT_SYSTEME = Path(__file__).parent / "prompts" / "systeme.md"

#: Nombre maximal de générations avant de passer à une question de secours.
MAX_TENTATIVES = 3


class Axe(str, Enum):
    """L'aspect du récit sur lequel porte une question."""

    DESIR = "desir"
    OBSTACLE = "obstacle"
    TENSION = "tension"
    LIEU = "lieu"
    STRUCTURE = "structure"
    POINT_DE_VUE = "point-de-vue"


@dataclass(frozen=True)
class Question:
    """Une question posée à l'auteur (format JSON décrit dans docs/formats.md).

    Attributs :
        texte : la question elle-même, par exemple « Que garde-t-elle ici ? ».
        page : la page du scénario qui l'a inspirée.
        scene : le numéro de la scène qui l'a inspirée.
        moteur : le nom du moteur qui l'a générée, ou « secours » pour une
            question écrite à l'avance.
        axe : l'aspect du récit visé.
    """

    texte: str
    page: int
    scene: int
    moteur: str
    axe: Axe | None = None


@dataclass(frozen=True)
class DemandeAuteur:
    """Un message libre de l'auteur pendant la session."""

    texte: str
    scene: Scene | None = None


def charger_prompt_systeme() -> str:
    """Lit le prompt système depuis ``prompts/systeme.md``."""
    raise NotImplementedError


def generer_questions(
    scene: Scene,
    analyse: AnalyseNarrative,
    moteur: Moteur,
    nombre: int,
) -> list[Question]:
    """Génère des questions sur une scène, chacune validée par le garde-fou.

    Args:
        scene : la scène envoyée par l'auteur.
        analyse : la carte du récit produite par ``analyse.narration``.
        moteur : le moteur de langage à utiliser.
        nombre : combien de questions poser, fixé par ``autonomie.regulateur``.

    Returns:
        Les questions à afficher, avec leur page et leur scène.
    """
    raise NotImplementedError


def question_de_secours(scene: Scene, axe: Axe | None = None) -> Question:
    """Renvoie une question écrite à l'avance, quand le modèle échoue au garde-fou.

    Args:
        scene : la scène concernée, pour citer sa page et son numéro.
        axe : l'aspect du récit à viser, si on le connaît.

    Returns:
        Une question de secours, dont le moteur vaut « secours ».
    """
    raise NotImplementedError


def est_demande_d_ecriture(demande: DemandeAuteur) -> bool:
    """Détecte si l'auteur demande à Contrechamp d'écrire à sa place.

    Exemples : « Écris-la pour moi », « Fais-moi le dialogue ».

    Args:
        demande : le message de l'auteur.

    Returns:
        True si le message demande d'écrire du texte de scénario.
    """
    raise NotImplementedError


def repondre_a_une_demande(
    demande: DemandeAuteur,
    analyse: AnalyseNarrative,
    moteur: Moteur,
) -> Question:
    """Répond à un message de l'auteur, toujours par une question.

    Si le message demande d'écrire à la place de l'auteur, Contrechamp refuse
    poliment et renvoie une question qui l'aide à écrire lui-même.

    Args:
        demande : le message de l'auteur.
        analyse : la carte du récit.
        moteur : le moteur de langage à utiliser.

    Returns:
        Une question, jamais un texte de scénario.
    """
    raise NotImplementedError
