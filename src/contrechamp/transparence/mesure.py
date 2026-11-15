"""Mesure de la consommation de chaque requête : temps, tokens et énergie.

Chaque appel à un moteur de ``llm.moteurs`` est mesuré ici. La mesure est
ensuite enregistrée dans le journal (``transparence.journal``) et peut être
montrée à l'auteur par l'interface. Elle répond à l'angle « Planète » de la
charte d'éthique (docs/ethique.md) : on ne réduit que ce qu'on mesure.

L'énergie est une estimation, pas une mesure physique exacte. La méthode
d'estimation sera choisie au moment du prototype.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Mesure:
    """La consommation d'une requête.

    Attributs :
        duree_s : temps écoulé entre l'envoi et la réponse, en secondes.
        tokens_entree : nombre de tokens envoyés au modèle.
        tokens_sortie : nombre de tokens produits par le modèle.
        energie_wh : énergie estimée, en wattheures, ou None si l'estimation
            n'est pas disponible (par exemple en mode API).
    """

    duree_s: float
    tokens_entree: int
    tokens_sortie: int
    energie_wh: float | None


class Chronometre:
    """Gestionnaire de contexte qui mesure une requête.

    Utilisation prévue :

        with Chronometre() as chrono:
            reponse = ...
        mesure = chrono.resultat(tokens_entree, tokens_sortie)
    """

    def __enter__(self) -> "Chronometre":
        raise NotImplementedError

    def __exit__(self, *exc: object) -> None:
        raise NotImplementedError

    def resultat(self, tokens_entree: int, tokens_sortie: int) -> Mesure:
        """Renvoie la mesure de la requête une fois terminée."""
        raise NotImplementedError


def compter_tokens(texte: str) -> int:
    """Compte de façon approchée le nombre de tokens d'un texte.

    Args:
        texte : le texte à compter.

    Returns:
        Le nombre approché de tokens.
    """
    raise NotImplementedError


def estimer_energie(duree_s: float, tokens: int) -> float | None:
    """Estime l'énergie consommée par une requête locale.

    Args:
        duree_s : durée de la requête.
        tokens : nombre total de tokens traités.

    Returns:
        L'énergie estimée en wattheures, ou None si elle ne peut pas être estimée.
    """
    raise NotImplementedError


def cumuler(mesures: list[Mesure]) -> Mesure:
    """Additionne les mesures d'une session, pour l'affichage final à l'auteur.

    Args:
        mesures : les mesures de toutes les requêtes de la session.

    Returns:
        Le total de la session.
    """
    raise NotImplementedError
