"""Cas que le garde-fou (``contrechamp.garde_fou.filtre``) devra gérer.

Le filtre n'est pas encore implémenté : tous les tests sont marqués
« à implémenter ». Ils décrivent le comportement attendu et serviront de
cahier des charges au prototype. Les règles sont détaillées dans
docs/garde-fou.md.
"""

from __future__ import annotations

import pytest

from contrechamp.garde_fou.filtre import Motif, verifier

A_IMPLEMENTER = pytest.mark.skip(reason="à implémenter")


# Sorties que le filtre doit bloquer, avec le motif attendu.
A_BLOQUER: list[tuple[str, Motif]] = [
    ("LEILA : Je ne partirai jamais.", Motif.REPLIQUE),
    ("JEDDA : Khalliha testanna.", Motif.REPLIQUE),
    ("« Je reste ici », murmure-t-elle.", Motif.DIALOGUE_GUILLEMETS),
    ('"Je ne partirai pas", dit Jedda.', Motif.DIALOGUE_GUILLEMETS),
    ("INT. MAISON DE JEDDA - NUIT", Motif.EN_TETE),
    ("EXT. COUR - JOUR", Motif.EN_TETE),
    ("INT./EXT. VOITURE - SOIR", Motif.EN_TETE),
    ("Leila entre dans la cuisine et pose les clés sur la table.", Motif.DESCRIPTION),
    ("La grand-mère s'assoit sur le seuil et ferme les yeux.", Motif.DESCRIPTION),
]

# Sorties que le filtre doit accepter.
A_ACCEPTER: list[str] = [
    "Que garde-t-elle ici ?",
    "Qui veut qu'elle parte ?",
    "Et si la maison refusait de la laisser partir ?",
    "Que voit Jedda quand elle regarde les cartons ?",
]


@A_IMPLEMENTER
@pytest.mark.parametrize(("sortie", "motif"), A_BLOQUER)
def test_bloque(sortie: str, motif: Motif) -> None:
    """Le filtre bloque chaque sortie qui écrit à la place de l'auteur."""
    verdict = verifier(sortie)
    assert not verdict.accepte
    assert motif in verdict.motifs


@A_IMPLEMENTER
@pytest.mark.parametrize("sortie", A_ACCEPTER)
def test_accepte(sortie: str) -> None:
    """Le filtre laisse passer une question courte."""
    assert verifier(sortie).accepte


@A_IMPLEMENTER
def test_bloque_sortie_trop_longue() -> None:
    """Une sortie qui dépasse la longueur maximale est bloquée, même si c'est une question."""
    sortie = "Et si " + "la maison, " * 200 + "refusait ?"
    verdict = verifier(sortie)
    assert not verdict.accepte
    assert Motif.TROP_LONGUE in verdict.motifs


@A_IMPLEMENTER
def test_bloque_question_suivie_d_une_replique() -> None:
    """Une question valide ne suffit pas à faire passer une réplique cachée après elle."""
    verdict = verifier("Que garde-t-elle ici ? LEILA : Je ne partirai jamais.")
    assert not verdict.accepte
    assert Motif.REPLIQUE in verdict.motifs


@A_IMPLEMENTER
def test_accepte_deux_points_dans_une_question() -> None:
    """Des deux-points dans une question ne sont pas pris pour une réplique."""
    assert verifier("Une question : que garde-t-elle ici ?").accepte


@A_IMPLEMENTER
def test_accepte_citation_courte_du_scenario() -> None:
    """Citer un mot de l'auteur entre guillemets n'est pas écrire un dialogue.

    À définir pendant le prototype : règle exacte à fixer (longueur maximale d'une citation,
    obligation qu'elle figure déjà dans la scène de l'auteur).
    """
    assert verifier("Pourquoi Jedda dit-elle « khalliha » ?").accepte


@A_IMPLEMENTER
def test_bloque_affirmation_sans_question() -> None:
    """Une sortie qui ne contient aucune question est bloquée."""
    verdict = verifier("Cette scène manque de tension.")
    assert not verdict.accepte
    assert Motif.PAS_UNE_QUESTION in verdict.motifs
