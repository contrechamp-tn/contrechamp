# Formats de données

> Statut : **en conception**. Ces formats sont ceux que le prototype devra respecter.

## Format de scénario accepté

Contrechamp accepte un scénario sous forme de texte. Formats de fichier prévus :

| Format | Extension | Remarque |
|---|---|---|
| Texte brut | `.txt` | Le plus simple : ce que l'auteur a écrit, tel quel. |
| Fountain | `.fountain` | Format texte standard des scénaristes. |
| PDF | `.pdf` | Le texte est extrait, les pages du PDF sont gardées. |

L'auteur peut aussi coller une scène directement dans l'interface.

**Langues.** Le texte peut être écrit en derja en lettres latines, en français, en arabe, ou dans un mélange des trois. Contrechamp ne corrige jamais la langue de l'auteur.

**Pages.** Les pages sont repérées par les sauts de page du fichier (PDF, caractère de saut de page). À défaut, Contrechamp découpe le texte selon une longueur standard. À décider pendant le prototype : longueur retenue pour une page.

**Scènes.** Une scène commence par un en-tête, s'il y en a un :

```
INT. MAISON DE JEDDA - SALON - JOUR
```

L'en-tête n'est pas obligatoire : beaucoup de premiers scénarios n'en ont pas. Sans en-tête, Contrechamp découpe aux lignes vides doubles ou à une ligne `===`. Les scènes sont numérotées à partir de 1.

**Répliques.** Le nom du personnage, en capitales sur sa propre ligne, puis la réplique en dessous :

```
LEILA
Jedda, el karhba testanna.
```

Un exemple complet se trouve dans [`exemples/leila.txt`](../exemples/leila.txt).

## Format JSON d'une question

Chaque question affichée à l'auteur correspond à la dataclass `Question` (`src/contrechamp/socratique/questions.py`) :

```json
{
  "texte": "Que garde-t-elle ici ?",
  "page": 1,
  "scene": 1,
  "moteur": "local:<nom du modèle>",
  "axe": "desir"
}
```

| Champ | Type | Obligatoire | Description |
|---|---|---|---|
| `texte` | chaîne | oui | La question, une seule phrase qui se termine par « ? ». |
| `page` | entier ≥ 1 | oui | La page du scénario qui a inspiré la question. |
| `scene` | entier ≥ 1 | oui | Le numéro de la scène qui a inspiré la question. |
| `moteur` | chaîne | oui | Le moteur qui l'a générée : `local:<modèle>`, `api:<modèle>`, ou `secours` pour une question écrite à l'avance. |
| `axe` | chaîne ou `null` | non | L'aspect visé : `desir`, `obstacle`, `tension`, `lieu`, `structure`, `point-de-vue`. |

## Format du journal (JSONL)

Le journal est un fichier texte au format [JSON Lines](https://jsonlines.org/) : **une entrée JSON par ligne**, ajoutée à la fin du fichier. Il est rangé dans le dossier `CONTRECHAMP_DOSSIER_JOURNAL` (voir `.env.example`) et reste sur l'ordinateur de l'auteur.

Chaque ligne correspond à la dataclass `EntreeJournal` (`src/contrechamp/transparence/journal.py`). Exemple, présenté sur plusieurs lignes pour la lecture (dans le fichier, il tient sur une seule ligne) :

```json
{
  "horodatage": "2026-11-15T21:30:00+01:00",
  "session": "<identifiant de session>",
  "question": {
    "texte": "Que garde-t-elle ici ?",
    "page": 1,
    "scene": 1,
    "moteur": "local:<nom du modèle>",
    "axe": "desir"
  },
  "verdict": {
    "accepte": true,
    "motifs": []
  },
  "tentatives": 2,
  "secours": false,
  "mesure": {
    "duree_s": null,
    "tokens_entree": null,
    "tokens_sortie": null,
    "energie_wh": null
  }
}
```

Les valeurs de `mesure` sont laissées à `null` dans cet exemple : aucune mesure n'a encore été faite.

| Champ | Type | Description |
|---|---|---|
| `horodatage` | chaîne ISO 8601 | Date et heure, avec le fuseau. |
| `session` | chaîne | Identifiant de la session d'écriture. |
| `question` | objet | La question affichée, au format ci-dessus. |
| `verdict.accepte` | booléen | Décision du garde-fou sur la **première** sortie du modèle. |
| `verdict.motifs` | liste de chaînes | Raisons du rejet : `replique`, `dialogue-guillemets`, `en-tete`, `description`, `trop-longue`, `pas-une-question`. |
| `tentatives` | entier ≥ 1 | Nombre de générations nécessaires. |
| `secours` | booléen | `true` si la question affichée est une question de secours. |
| `mesure.duree_s` | nombre | Durée cumulée des tentatives, en secondes. |
| `mesure.tokens_entree` | entier | Tokens envoyés au modèle. |
| `mesure.tokens_sortie` | entier | Tokens produits par le modèle. |
| `mesure.energie_wh` | nombre ou `null` | Énergie estimée en wattheures ; `null` si elle n'est pas estimable (mode API). |

Le journal ne contient jamais le texte du scénario, ni celui des sorties rejetées par le garde-fou : seulement la page, la scène, la question, le moteur, l'heure et la mesure, avec la décision du garde-fou. L'auteur peut l'exporter ou l'effacer depuis l'interface.
