"""Contrechamp, le co-auteur qui ne tient jamais le stylo.

Contrechamp est une IA socratique pour les jeunes cinéastes tunisiens. Elle lit
un scénario (en derja écrite en lettres latines, ou en français) et pose des
questions pour débloquer l'écriture. Elle n'écrit jamais une ligne à la place
de l'auteur.

Le projet est en phase de conception : ce paquet ne contient que le squelette
(données typées et signatures). Aucune fonction n'est encore implémentée.

Chaîne de traitement prévue :

    ingestion  ->  analyse  ->  socratique  ->  garde_fou  ->  interface
                                    |               |
                                   llm         autonomie
                                    |
                              transparence (journal et mesure)

Voir docs/architecture.md pour le détail.
"""

__version__ = "0.0.0"
