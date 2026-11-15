# Éthique à 360°

> Statut : **en conception**. Ce document dit comment chaque risque sera traité et quel module l'applique. Aucune de ces protections n'est encore implémentée.

Contrechamp s'adresse à de jeunes auteurs qui écrivent souvent seuls et sans formation. Une IA mal conçue pourrait leur prendre leur voix, leur texte ou leurs données. Nous avons examiné six angles. Pour chacun : le risque, notre réponse, et le module qui l'applique.

## Résumé

| Angle | Risque | Réponse | Module |
|---|---|---|---|
| Créateurs | Suivre l'IA sans réfléchir | Elle ne fait que poser des questions ; on peut les ignorer ; elles se font plus rares | `autonomie/regulateur.py` |
| Droits | Vol du scénario | Le scénario reste la propriété de l'auteur et n'est jamais réutilisé | `llm/moteurs.py`, `transparence/journal.py` |
| Données | Fuite des textes | Traitement en local quand c'est possible. Le scénario ne quitte pas l'ordinateur de l'auteur et n'entraîne aucun modèle ; le journal local garde les questions, pas le texte, et l'auteur peut l'effacer. | `llm/moteurs.py` |
| Cultures et langues | Une IA qui pense « à la Hollywood » | Derja, français, arabe, et structure des contes tunisiens | `analyse/narration.py` |
| Transparence | Ne pas savoir d'où vient une question | Chaque question cite sa page et sa scène ; tout est noté dans un journal | `transparence/journal.py` |
| Planète | Consommer trop d'énergie | Du texte seulement, de petits modèles, une consommation mesurée | `transparence/mesure.py` |

## 1. Créateurs

**Risque.** Un jeune auteur sans lecteur peut prendre chaque remarque de l'IA pour une vérité, et finir par écrire le film que l'IA imagine plutôt que le sien. Les outils actuels aggravent ce risque : ils écrivent à la place de l'auteur, qui n'apprend rien.

**Réponse.**

- Contrechamp ne fait que poser des questions. Il ne donne ni réponse, ni verdict, ni réécriture (`socratique/prompts/systeme.md`, `garde_fou/filtre.py`).
- L'auteur peut ignorer une question, demander le silence ou en demander plus. Ignorer une question n'est pas un échec.
- Les questions se font plus rares à mesure que l'auteur avance seul : le but est qu'il n'ait plus besoin de Contrechamp.

**Module.** `autonomie/regulateur.py` (nombre de questions selon l'autonomie), avec `garde_fou/filtre.py`.

## 2. Droits

**Risque.** Le scénario est l'œuvre de l'auteur. Un outil pourrait le copier, le réutiliser pour d'autres utilisateurs ou s'en attribuer une part.

**Réponse.**

- Le scénario reste la propriété exclusive de l'auteur. Contrechamp n'écrit aucune ligne du texte et ne revendique donc aucune part de l'œuvre.
- Le scénario n'est jamais réutilisé : ni pour un autre auteur, ni pour un exemple, ni pour entraîner un modèle.
- Le journal ne contient aucun texte du scénario, seulement les questions et leur source (page et scène).

**Modules.** `llm/moteurs.py` (aucune réutilisation, aucun envoi sans accord), `transparence/journal.py` (pas de copie du scénario).

## 3. Données

**Risque.** Un scénario de premier film est souvent intime : celui de Leila parle de sa grand-mère. Envoyé à un service externe, il pourrait fuiter, être conservé ou servir à entraîner un modèle.

**Réponse.**

- Par défaut, tout est traité en local, avec un modèle ouvert servi par Ollama sur l'ordinateur de l'auteur.
- Le mode API est une option. Il ne s'active qu'avec l'accord explicite de l'auteur, qui peut le retirer à tout moment. Seule la scène en cours est envoyée.
- Contrechamp ne garde rien hors de l'ordinateur de l'auteur et n'utilise aucun texte pour entraîner un modèle. À décider pendant le prototype : choix du fournisseur d'API, après vérification de ses conditions d'utilisation.
- La clé d'API reste dans `.env`, qui n'est jamais publié.

**Module.** `llm/moteurs.py` (`MoteurLocal` par défaut, `ConfigMoteur.accord_auteur` obligatoire pour `MoteurAPI`). Le flux des données est détaillé dans [architecture.md](architecture.md#flux-des-données).

## 4. Cultures et langues

**Risque.** Les modèles de langage ont surtout appris sur des textes anglophones et sur le cinéma américain. Ils risquent de pousser chaque scénario vers la structure hollywoodienne en trois actes, de mal comprendre la derja, ou de « corriger » la langue de l'auteur.

**Réponse.**

- Contrechamp lit la derja en lettres latines, le français et l'arabe, et le mélange des trois. Il répond dans la langue de l'auteur et ne corrige jamais sa langue.
- L'analyse connaît plusieurs structures, dont celle du conte tunisien, et ne juge pas un récit selon un seul modèle.
- La méthode elle-même vient d'une pratique tunisienne : la grand-mère de Leila qui demandait « Et après ? » au lieu de donner la suite.
- À définir pendant le prototype : sources et personnes consultées sur la structure du conte tunisien.
- À décider pendant le prototype : choix d'un modèle qui comprend bien la derja, après essais.

**Module.** `analyse/narration.py` (`ModeleStructure.CONTE_TUNISIEN`), avec `ingestion/scenario.py` (détection des langues).

## 5. Transparence

**Risque.** Une question qui sort de nulle part ne peut pas être discutée. L'auteur doit savoir sur quoi elle s'appuie, et pouvoir vérifier que l'IA n'a jamais écrit à sa place.

**Réponse.**

- Chaque question cite la page et la scène qui l'ont inspirée, et le moteur qui l'a générée.
- Chaque question est notée dans un journal local, avec le verdict du garde-fou, le nombre de tentatives et la consommation. L'auteur peut le lire, l'exporter ou l'effacer.
- Le prompt système est public, dans le dépôt.

**Module.** `transparence/journal.py`, avec `socratique/questions.py` (champs `page`, `scene`, `moteur`). Formats détaillés dans [formats.md](formats.md).

## 6. Planète

**Risque.** Les grands modèles consomment beaucoup d'énergie, et chaque requête compte.

**Réponse.**

- Du texte seulement : pas de génération d'image ni de son.
- De petits modèles ouverts, qui tournent sur un ordinateur personnel.
- Peu de requêtes : quelques questions courtes par scène, de moins en moins à mesure que l'auteur progresse.
- Une consommation mesurée pour chaque requête (temps, tokens, énergie estimée), notée dans le journal et montrée à l'auteur.
- À décider pendant le prototype : méthode d'estimation de l'énergie ; les premiers chiffres seront mesurés pendant le prototype.

**Module.** `transparence/mesure.py`, avec `autonomie/regulateur.py` (moins de requêtes).
