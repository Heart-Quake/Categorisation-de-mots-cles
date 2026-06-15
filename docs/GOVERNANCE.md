# Gouvernance produit, Clustering Semantique de Mots-Cles

## Decision Lot 4

Statut recommande : **local maintenu, non live pour le moment**.

Raison : l'outil recouvre fortement la `Keyword Categorization App` deja publiee dans le hub live, mais il conserve une valeur de laboratoire pour tester des approches de clustering semantique, HDBSCAN, UMAP, sentence-transformers et typologies metier.

Decision a ne pas prendre sans validation produit : publier cet outil tel quel dans le hub public. La priorite est d'abord de comparer ses sorties a `automation-seo-keyword-categorization`, puis de fusionner uniquement les briques qui apportent un gain mesurable.

## Source de verite

| Element | Valeur |
|---|---|
| Repo local | `/Users/vincentflaceliere/Github/Categorisation-de-mots-cles` |
| Exposition actuelle | local uniquement |
| Entrypoint | `app.py` |
| Commande locale | `streamlit run app.py` |
| Compilation | `python3 -m py_compile app.py` |
| Tests | Aucun test automatise detecte au Lot 4 |
| Decision produit | maintenir comme labo/fonction source, ne pas publier |

## Contrat d'entree

Formats acceptes par l'interface :

- CSV avec separateur `,` ou `;`
- Excel `.xlsx` ou `.xls`

Colonnes attendues :

| Colonne canonique | Obligatoire | Alias constates | Regle |
|---|---:|---|---|
| `Keyword` | oui | variantes detectees dans `app.py` | converti en texte, lignes vides supprimees |
| `Volume` | non | variantes detectees dans `app.py` | converti en numerique, valeur `0` si absent ou invalide |

Nettoyage applique :

- normalisation minuscules, accents, ponctuation et espaces
- lemmatisation
- deduplication par mot-cle lemmatise
- conservation du volume maximum par groupe deduplique

## Contrat de sortie

Exports generes :

- CSV `clustering_mots_cles_<timestamp>.csv`
- Excel `clustering_mots_cles_<timestamp>.xlsx`

Colonnes principales :

| Colonne | Description |
|---|---|
| `Mot-cle` | mot-cle source conserve |
| `Volume de recherche` | volume numerique conserve |
| `Cluster_ID` | identifiant numerique du cluster, `-1` pour divers/singletons |
| `Cluster_Label` | libelle genere automatiquement |
| `Intention de recherche` | intention detectee par regles |

L'export Excel ajoute une synthese par cluster et un onglet de tracabilite du nettoyage si disponible.

## Criteres avant passage live

Passage live bloque tant que les points suivants ne sont pas traites :

- ajouter des tests unitaires sur import, normalisation, deduplication et export
- extraire la logique metier hors de `app.py`
- comparer les sorties sur un meme fixture avec `automation-seo-keyword-categorization`
- trancher fusion ou abandon des modules `config/ml_enhancement.py`, `config/competitive_analysis.py`, `config/advanced_patterns.py`
- appliquer le design system Automation SEO uniquement si publication live validee

## Risques

- Dette applicative : `app.py` concentre UI, logique metier, clustering et export.
- Dependances lourdes : `sentence-transformers`, spaCy, UMAP, HDBSCAN.
- Runtime potentiellement lent ou instable sur Streamlit Cloud si les modeles sont charges a froid.
- Doublon produit avec l'app live de categorisation.

## Commandes de reprise

```bash
cd /Users/vincentflaceliere/Github/Categorisation-de-mots-cles
python3 -m py_compile app.py
streamlit run app.py
```

## Prochaine action recommandee

Creer un fixture de 30 a 100 mots-cles et comparer manuellement :

- cohesion des clusters
- qualite des labels
- stabilite runtime
- valeur supplementaire vs `automation-seo-keyword-categorization`

Si l'outil n'apporte pas de gain clair, le classer comme source historique et ne pas le maintenir dans le hub.
