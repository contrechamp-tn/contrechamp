# Architecture de Contrechamp

> Statut : **en conception**. Ce document décrit l'architecture prévue. Aucun composant n'est encore implémenté.

Contrechamp lit un scénario et renvoie des questions. Il n'écrit jamais dans le scénario. Toute l'architecture est organisée autour de cette règle : la sortie du modèle de langage passe par deux sécurités avant d'arriver à l'auteur, et chaque question affichée est notée dans un journal local.

## Rôle de chaque composant

| Composant | Module | Rôle |
|---|---|---|
| Ingestion du scénario | `ingestion/scenario.py` | Lit le texte (derja en lettres latines, français, arabe) et le découpe en pages et en scènes numérotées. Ces numéros sont la source de chaque question. |
| Ingestion des rushes (bonus prévu) | `ingestion/rushes.py` | Transcrit les rushes en derja avec FarukSTT, en local, et les rattache aux scènes. |
| Analyse narrative | `analyse/narration.py` | Repère les personnages, ce qu'ils veulent, ce qui s'y oppose, l'évolution de la tension, et la structure du récit (dont celle du conte tunisien). Cette analyse nourrit les questions ; elle n'est jamais montrée comme un verdict. |
| Génération socratique | `socratique/questions.py` | Demande au moteur des questions sur la scène, en suivant le prompt système. Chaque question porte sa page, sa scène et le nom du moteur. Gère les demandes « Écris-la pour moi ». |
| Prompt système | `socratique/prompts/systeme.md` | Première sécurité : la consigne donnée au modèle (poser des questions, ne jamais écrire de dialogue, de scène ou de description). |
| Garde-fou | `garde_fou/filtre.py` | Seconde sécurité : relit chaque sortie sans faire appel au modèle et bloque tout ce qui ressemble à du texte de scénario. Voir [garde-fou.md](garde-fou.md). |
| Régulateur d'autonomie | `autonomie/regulateur.py` | Décide combien de questions poser. Le nombre baisse à mesure que l'auteur avance seul. |
| Moteurs de langage | `llm/moteurs.py` | Interface commune : modèle ouvert en local avec Ollama (par défaut), ou API externe en option, avec l'accord de l'auteur. |
| Mesure | `transparence/mesure.py` | Mesure le temps, les tokens et l'énergie estimée de chaque requête. |
| Journal | `transparence/journal.py` | Note chaque question dans un fichier JSONL local, avec sa source, le verdict du garde-fou et la mesure. |
| Interface | `interface/app.py` | Page web locale : envoyer une scène, lire les questions, régler l'autonomie, choisir le moteur, consulter le journal. |

## Diagramme des composants

```mermaid
flowchart LR
    A([Auteur]) -->|scène ou scénario| UI[Interface<br/>interface/app.py]
    R[(Rushes)] -.->|bonus prévu| RU[Ingestion des rushes<br/>ingestion/rushes.py]

    UI --> IN[Ingestion du scénario<br/>ingestion/scenario.py]
    IN -->|pages et scènes| AN[Analyse narrative<br/>analyse/narration.py]
    RU -.->|transcriptions| AN
    AN -->|carte du récit| SO[Génération socratique<br/>socratique/questions.py]
    PS[Prompt système<br/>prompts/systeme.md] --> SO
    AU[Régulateur d'autonomie<br/>autonomie/regulateur.py] -->|nombre de questions| SO

    SO <-->|requêtes| LLM[Moteurs<br/>llm/moteurs.py]
    AN <-->|requêtes| LLM
    LLM --> OL[Ollama<br/>modèle ouvert local]
    LLM -.->|option, avec accord| API[API externe]
    LLM --> ME[Mesure<br/>transparence/mesure.py]

    SO -->|sortie brute| GF{Garde-fou<br/>garde_fou/filtre.py}
    GF -->|rejet : régénérer| SO
    GF -->|question acceptée| UI
    GF --> JO[(Journal JSONL<br/>transparence/journal.py)]
    ME --> JO

    UI -->|questions avec page et scène| A
    UI -->|réactions de l'auteur| AU
```

## Séquence d'une session

L'auteur envoie une scène ; Contrechamp renvoie des questions, chacune avec sa page et sa scène.

```mermaid
sequenceDiagram
    autonumber
    actor Auteur
    participant UI as Interface
    participant IN as Ingestion
    participant AN as Analyse
    participant AU as Régulateur
    participant SO as Socratique
    participant LLM as Moteur
    participant GF as Garde-fou
    participant JO as Journal

    Auteur->>UI: envoie une scène
    UI->>IN: charger_scenario(texte)
    IN-->>UI: pages et scènes numérotées
    UI->>AN: analyser(scenario)
    AN->>LLM: generer(...)
    LLM-->>AN: personnages, désirs, tension, structure
    AN-->>UI: carte du récit
    UI->>AU: nombre_de_questions(etat)
    AU-->>UI: n questions
    UI->>SO: generer_questions(scene, analyse, n)
    loop au plus MAX_TENTATIVES fois
        SO->>LLM: generer(prompt système, scène)
        LLM-->>SO: sortie brute et mesure
        SO->>GF: verifier(sortie)
        alt sortie acceptée
            GF-->>SO: Verdict(accepte = vrai)
        else sortie rejetée
            GF-->>SO: Verdict(accepte = faux, motifs)
            Note over SO,GF: rejet : on régénère
        end
    end
    opt toutes les tentatives rejetées
        SO->>SO: question_de_secours(scene)
    end
    SO-->>UI: questions (texte, page, scène, moteur)
    UI->>JO: ecrire(entrée : question, verdict, tentatives, mesure)
    UI-->>Auteur: affiche les questions avec page et scène
```

## Séquence d'une demande « Écris-la pour moi »

Contrechamp ne fait jamais d'exception : il refuse et renvoie une question.

```mermaid
sequenceDiagram
    autonumber
    actor Auteur
    participant UI as Interface
    participant SO as Socratique
    participant LLM as Moteur
    participant GF as Garde-fou
    participant JO as Journal

    Auteur->>UI: « Écris-la pour moi »
    UI->>SO: repondre_a_une_demande(demande)
    SO->>SO: est_demande_d_ecriture(demande) renvoie vrai
    SO->>LLM: generer(prompt système, consigne de refus et de question)
    LLM-->>SO: sortie brute
    SO->>GF: verifier(sortie)
    alt sortie acceptée
        GF-->>SO: Verdict(accepte = vrai)
    else sortie rejetée (le modèle a écrit la scène)
        GF-->>SO: Verdict(accepte = faux)
        SO->>SO: question_de_secours(scene)
    end
    SO-->>UI: refus et question, avec page et scène
    UI->>JO: ecrire(entrée)
    UI-->>Auteur: « Ce texte est le tien, je ne l'écrirai pas. Mais dis-moi : … ? »
```

## Flux des données

Par défaut, **rien ne quitte l'ordinateur de l'auteur**.

| Donnée | Où elle est traitée | Où elle est gardée | Sort-elle de l'ordinateur ? |
|---|---|---|---|
| Scénario | Ingestion, analyse, génération (en local) | Nulle part par Contrechamp : il reste dans le fichier de l'auteur | Seulement en mode API, avec l'accord de l'auteur |
| Rushes (bonus prévu) | Transcription locale avec FarukSTT | Sur l'ordinateur de l'auteur | Non |
| Questions | Génération et garde-fou | Journal JSONL local | Non |
| Journal | Écrit en local | Dossier `CONTRECHAMP_DOSSIER_JOURNAL` | Non (l'auteur peut l'exporter ou l'effacer) |
| Mesures | Calculées en local | Journal JSONL local | Non |
| Clé d'API | Lue dans `.env` | `.env`, jamais publié (voir `.gitignore`) | Envoyée seulement au fournisseur choisi |

```mermaid
flowchart TB
    subgraph PC[Ordinateur de l'auteur]
        S[Scénario] --> C[Contrechamp]
        RU[Rushes] -.-> C
        C <--> O[Ollama<br/>modèle ouvert]
        C --> J[(Journal JSONL)]
    end
    subgraph EXT[Extérieur]
        P[Fournisseur d'API]
    end
    C -.->|mode API seulement,<br/>avec l'accord de l'auteur| P
    P -.->|réponse| C
```

En mode API :

- l'auteur active le mode lui-même, et l'interface lui demande son accord explicite avant le premier envoi (`ConfigMoteur.accord_auteur`) ;
- seule la scène en cours et la carte du récit nécessaires à la question sont envoyées, pas le scénario entier ;
- Contrechamp ne garde rien chez le fournisseur et ne lui demande jamais d'utiliser les textes pour entraîner un modèle. À COMPLÉTER : vérifier les conditions d'utilisation du fournisseur retenu sur ce point ;
- l'auteur peut retirer son accord à tout moment : Contrechamp repasse alors en local.
