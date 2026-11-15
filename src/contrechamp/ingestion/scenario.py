"""Découpage du scénario en pages et en scènes.

C'est la porte d'entrée de Contrechamp. Ce module lit le texte du scénario
(derja en lettres latines, français ou arabe) et le découpe en pages et en
scènes numérotées. Ces numéros servent ensuite partout : chaque question
générée par ``socratique.questions`` cite la page et la scène qui l'ont
inspirée, et le journal (``transparence.journal``) les enregistre.

Le module ne transmet rien à l'extérieur : il travaille sur l'ordinateur de
l'auteur. Le format accepté est décrit dans docs/formats.md.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path


class Langue(str, Enum):
    """Langue principale détectée dans un passage du scénario."""

    DERJA_LATINE = "derja-latine"
    FRANCAIS = "francais"
    ARABE = "arabe"
    INCONNUE = "inconnue"


@dataclass(frozen=True)
class Page:
    """Une page du scénario, telle qu'elle apparaît dans le document source."""

    numero: int
    texte: str


@dataclass(frozen=True)
class Scene:
    """Une scène du scénario, repérée par son en-tête (INT./EXT.) s'il existe.

    Attributs :
        numero : numéro de la scène dans le scénario, à partir de 1.
        page_debut : page où commence la scène.
        page_fin : page où elle se termine.
        en_tete : l'en-tête tel qu'écrit par l'auteur (ex. « INT. MAISON - NUIT »),
            ou None si l'auteur n'en a pas mis.
        texte : le texte brut de la scène, sans modification.
        langues : les langues repérées dans la scène.
    """

    numero: int
    page_debut: int
    page_fin: int
    en_tete: str | None
    texte: str
    langues: tuple[Langue, ...] = ()


@dataclass
class Scenario:
    """Un scénario découpé, propriété de son auteur.

    Le titre et le contenu ne sont jamais réutilisés en dehors de la session
    de l'auteur (voir docs/ethique.md, angle « Droits »).
    """

    titre: str | None
    pages: list[Page] = field(default_factory=list)
    scenes: list[Scene] = field(default_factory=list)


def lire_fichier(chemin: Path) -> str:
    """Lit un scénario sur le disque (texte brut, Fountain ou PDF) et renvoie son texte.

    Args:
        chemin : chemin du fichier fourni par l'auteur.

    Returns:
        Le texte complet du scénario.
    """
    raise NotImplementedError


def decouper_pages(texte: str) -> list[Page]:
    """Découpe le texte en pages, à partir des sauts de page ou d'une longueur standard.

    Args:
        texte : le texte complet du scénario.

    Returns:
        La liste des pages, numérotées à partir de 1.
    """
    raise NotImplementedError


def decouper_scenes(pages: list[Page]) -> list[Scene]:
    """Repère les scènes à partir des en-têtes INT./EXT. ou des séparations de l'auteur.

    Args:
        pages : les pages produites par ``decouper_pages``.

    Returns:
        La liste des scènes, chacune avec ses pages de début et de fin.
    """
    raise NotImplementedError


def detecter_langues(texte: str) -> tuple[Langue, ...]:
    """Repère les langues présentes dans un passage (derja latine, français, arabe).

    Args:
        texte : un passage du scénario.

    Returns:
        Les langues repérées, de la plus présente à la moins présente.
    """
    raise NotImplementedError


def charger_scenario(texte: str, titre: str | None = None) -> Scenario:
    """Point d'entrée du module : découpe un texte complet en un ``Scenario``.

    Args:
        texte : le texte complet envoyé par l'auteur.
        titre : le titre du projet, s'il est connu.

    Returns:
        Le scénario découpé en pages et en scènes.
    """
    raise NotImplementedError
