# Feuille de route

> Statut actuel : **phase 1, conception**. Aucune date n'est fixée au-delà de cette phase. À COMPLÉTER : calendrier des phases suivantes.

## Les phases

### Phase 1 : conception (en cours)

- Structure du dépôt et squelette typé de chaque module.
- Architecture, garde-fou, formats de données et charte d'éthique documentés.
- Prompt système rédigé.
- Cas de test du garde-fou écrits (marqués « à implémenter »).

### Phase 2 : prototype

- Découpage du scénario en pages et en scènes (`ingestion/scenario.py`).
- Moteur local avec Ollama, et choix d'un petit modèle ouvert après essais (`llm/moteurs.py`).
- Génération des questions avec page et scène (`socratique/questions.py`).
- Filtre du garde-fou, jusqu'à ce que tous les tests de `tests/test_garde_fou.py` passent (`garde_fou/filtre.py`).
- Journal JSONL et mesure de la consommation (`transparence/`).
- Première interface web locale (`interface/app.py`).

### Phase 3 : test avec de jeunes cinéastes

- Rencontrer de jeunes cinéastes, surtout hors de Tunis, pour vérifier le problème.
- Sessions avec de jeunes cinéastes tunisiens, en particulier hors de Tunis. À COMPLÉTER : partenaires, lieux et nombre de participants.
- Analyse narrative complète, dont la structure du conte tunisien (`analyse/narration.py`).
- Régulateur d'autonomie, réglé à partir des sessions (`autonomie/regulateur.py`).
- Ajustement du garde-fou sur les sorties réelles.
- Mode API en option, avec accord explicite de l'auteur.

### Phase 4 : version derja et rushes

- Qualité en derja : questions générées en derja, cas de test du garde-fou en derja et en arabe.
- Bonus : transcription des rushes en derja avec FarukSTT et rattachement aux scènes (`ingestion/rushes.py`).

## Répartition des tâches

| Tâche | Module | Responsable |
|---|---|---|
| Découpage en pages et en scènes | `ingestion/scenario.py` | L'équipe |
| Transcription des rushes (bonus) | `ingestion/rushes.py` | L'équipe |
| Analyse narrative et conte tunisien | `analyse/narration.py` | L'équipe |
| Génération des questions | `socratique/questions.py` | L'équipe |
| Prompt système | `socratique/prompts/systeme.md` | L'équipe |
| Filtre du garde-fou et ses tests | `garde_fou/filtre.py`, `tests/test_garde_fou.py` | L'équipe |
| Régulateur d'autonomie | `autonomie/regulateur.py` | L'équipe |
| Journal | `transparence/journal.py` | L'équipe |
| Mesure de la consommation | `transparence/mesure.py` | L'équipe |
| Moteurs local et API | `llm/moteurs.py` | L'équipe |
| Interface web | `interface/app.py` | L'équipe |
| Sessions de test avec de jeunes cinéastes | — | L'équipe |
| Documentation | `docs/`, `README.md` | L'équipe |
