"""Interface commune des moteurs de langage.

Tous les autres modules (``analyse.narration``, ``socratique.questions``)
parlent au modèle de langage à travers l'interface ``Moteur`` définie ici. Ils
ne savent donc pas si le modèle tourne sur l'ordinateur de l'auteur ou chez un
fournisseur externe.

Deux moteurs sont prévus :

- ``MoteurLocal`` (par défaut) : un modèle de langage ouvert servi par Ollama
  sur l'ordinateur de l'auteur. Le scénario ne quitte jamais la machine.
- ``MoteurAPI`` (en option) : un fournisseur externe, utilisé seulement si
  l'auteur l'a choisi et a donné son accord explicite. Aucun texte n'est
  conservé par Contrechamp ni utilisé pour entraîner un modèle.

Chaque appel est mesuré par ``transparence.mesure`` (temps, tokens, énergie).
Le choix du moteur se fait dans le fichier .env (voir .env.example).
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum

from contrechamp.transparence.mesure import Mesure


class TypeMoteur(str, Enum):
    """L'endroit où tourne le modèle."""

    LOCAL = "local"
    API = "api"


@dataclass(frozen=True)
class ConfigMoteur:
    """Configuration lue dans le fichier .env.

    Attributs :
        type : local ou API.
        modele : nom du modèle (dans Ollama, ou chez le fournisseur).
        url : adresse du serveur Ollama, ou de l'API.
        cle_api : clé du fournisseur, en mode API seulement.
        accord_auteur : True seulement si l'auteur a accepté que son texte
            sorte de son ordinateur. Obligatoire en mode API.
    """

    type: TypeMoteur
    modele: str
    url: str | None = None
    cle_api: str | None = None
    accord_auteur: bool = False


@dataclass(frozen=True)
class Reponse:
    """La réponse brute d'un moteur, avec la mesure de sa consommation."""

    texte: str
    moteur: str
    mesure: Mesure


class Moteur(ABC):
    """Interface commune à tous les moteurs de langage."""

    @property
    @abstractmethod
    def nom(self) -> str:
        """Le nom affiché du moteur, repris dans le format JSON d'une question."""
        raise NotImplementedError

    @abstractmethod
    def generer(self, systeme: str, message: str, max_tokens: int) -> Reponse:
        """Envoie une requête au modèle et renvoie sa réponse mesurée.

        Args:
            systeme : le prompt système (``socratique/prompts/systeme.md``).
            message : le contenu de la requête (scène et analyse).
            max_tokens : la longueur maximale de la réponse.

        Returns:
            La réponse du modèle et sa mesure.
        """
        raise NotImplementedError


class MoteurLocal(Moteur):
    """Modèle ouvert servi par Ollama sur l'ordinateur de l'auteur."""

    def __init__(self, config: ConfigMoteur) -> None:
        raise NotImplementedError

    @property
    def nom(self) -> str:
        raise NotImplementedError

    def generer(self, systeme: str, message: str, max_tokens: int) -> Reponse:
        raise NotImplementedError


class MoteurAPI(Moteur):
    """Fournisseur externe, utilisé seulement avec l'accord explicite de l'auteur.

    Le constructeur doit refuser de créer le moteur si ``accord_auteur`` est False.
    """

    def __init__(self, config: ConfigMoteur) -> None:
        raise NotImplementedError

    @property
    def nom(self) -> str:
        raise NotImplementedError

    def generer(self, systeme: str, message: str, max_tokens: int) -> Reponse:
        raise NotImplementedError


def charger_config() -> ConfigMoteur:
    """Lit le choix du moteur dans le fichier .env.

    Returns:
        La configuration, en mode local si rien n'est précisé.
    """
    raise NotImplementedError


def creer_moteur(config: ConfigMoteur) -> Moteur:
    """Crée le moteur correspondant à la configuration.

    Args:
        config : la configuration lue par ``charger_config``.

    Returns:
        Un ``MoteurLocal`` ou un ``MoteurAPI``.
    """
    raise NotImplementedError
