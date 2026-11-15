"""Analyse narrative : personnages, ce qu'ils veulent, tension et structure.

Ce module lit les scènes produites par ``ingestion.scenario`` et en tire une
carte du récit : qui sont les personnages, ce que chacun veut, ce qui s'y
oppose, où la tension monte ou retombe. Il repère aussi la structure du récit
selon plusieurs modèles, dont celle du conte tunisien (formule d'ouverture,
épreuves répétées, retour et morale), pour ne pas juger un scénario
uniquement à l'aune de la structure hollywoodienne en trois actes.

Cette carte ne sert qu'à nourrir ``socratique.questions`` : elle n'est jamais
montrée à l'auteur comme un verdict, et elle ne sert jamais à réécrire le
texte. L'analyse s'appuie sur le moteur choisi dans ``llm.moteurs``.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

from contrechamp.ingestion.scenario import Scenario, Scene
from contrechamp.llm.moteurs import Moteur


class ModeleStructure(str, Enum):
    """Les modèles de structure que l'analyse sait reconnaître."""

    CONTE_TUNISIEN = "conte-tunisien"
    TROIS_ACTES = "trois-actes"
    LIBRE = "libre"


@dataclass(frozen=True)
class Reference:
    """L'endroit précis du scénario sur lequel s'appuie une observation."""

    page: int
    scene: int


@dataclass
class Personnage:
    """Un personnage repéré dans le scénario.

    Attributs :
        nom : le nom tel qu'écrit par l'auteur (ex. « LEILA », « JEDDA »).
        desir : ce que le personnage semble vouloir, ou None s'il n'est pas clair.
            Un désir absent est une piste de question, pas une erreur.
        obstacles : ce qui s'oppose à ce désir.
        apparitions : les scènes où le personnage apparaît.
    """

    nom: str
    desir: str | None = None
    obstacles: list[str] = field(default_factory=list)
    apparitions: list[Reference] = field(default_factory=list)


@dataclass(frozen=True)
class PointDeTension:
    """Un moment du récit où la tension change.

    Attributs :
        reference : la page et la scène concernées.
        niveau : estimation de la tension, de 0 (calme) à 1 (crise).
        description : ce qui crée ou relâche la tension, en une phrase
            d'analyse destinée au module socratique, jamais à l'auteur.
    """

    reference: Reference
    niveau: float
    description: str


@dataclass
class EtapeStructure:
    """Une étape d'un modèle de structure, et la scène où elle semble se trouver."""

    nom: str
    reference: Reference | None


@dataclass
class AnalyseNarrative:
    """La carte complète du récit, transmise au module socratique."""

    personnages: list[Personnage] = field(default_factory=list)
    tensions: list[PointDeTension] = field(default_factory=list)
    structure: ModeleStructure = ModeleStructure.LIBRE
    etapes: list[EtapeStructure] = field(default_factory=list)


def extraire_personnages(scenes: list[Scene], moteur: Moteur) -> list[Personnage]:
    """Repère les personnages, leur désir et leurs obstacles.

    Args:
        scenes : les scènes à analyser.
        moteur : le moteur de langage à utiliser.

    Returns:
        Les personnages trouvés, avec leurs apparitions.
    """
    raise NotImplementedError


def mesurer_tension(scenes: list[Scene], moteur: Moteur) -> list[PointDeTension]:
    """Estime l'évolution de la tension de scène en scène.

    Args:
        scenes : les scènes à analyser.
        moteur : le moteur de langage à utiliser.

    Returns:
        Un point de tension par scène.
    """
    raise NotImplementedError


def reconnaitre_structure(
    scenes: list[Scene], moteur: Moteur
) -> tuple[ModeleStructure, list[EtapeStructure]]:
    """Cherche quel modèle de structure le récit suit, dont celui du conte tunisien.

    Args:
        scenes : les scènes à analyser.
        moteur : le moteur de langage à utiliser.

    Returns:
        Le modèle le plus proche et la place de chacune de ses étapes.
    """
    raise NotImplementedError


def analyser(scenario: Scenario, moteur: Moteur) -> AnalyseNarrative:
    """Point d'entrée du module : produit la carte complète du récit.

    Args:
        scenario : le scénario découpé par ``ingestion.scenario``.
        moteur : le moteur de langage à utiliser.

    Returns:
        L'analyse narrative, destinée à ``socratique.questions``.
    """
    raise NotImplementedError
