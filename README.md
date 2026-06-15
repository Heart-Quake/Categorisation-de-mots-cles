# 🎯 Clustering Sémantique Intelligent de Mots-Clés SEO

## Gouvernance Automation SEO

Statut Lot 4 : **local maintenu, non live pour le moment**.

Cet outil recouvre fortement la `Keyword Categorization App` déjà publiée dans le hub Automation SEO. Il doit rester un laboratoire de clustering sémantique tant qu'une comparaison de sorties n'a pas prouvé qu'il apporte une valeur supérieure ou complémentaire.

Voir : [docs/GOVERNANCE.md](docs/GOVERNANCE.md)

## 🚀 **Nouveautés - Normalisation Avancée des Mots-clés**

### ✨ **Système de Normalisation Complet**

Inspiré des meilleures pratiques Google Sheets, notre outil intègre désormais une **normalisation robuste** des mots-clés pour un clustering de qualité professionnelle.

#### 🔧 **Fonctionnalités de Normalisation**

**1. Gestion des Caractères Accentués**
- `à, â, ä, á, ã, å` → `a`
- `é, è, ë, ê, ę` → `e`
- `î, ï, í, ì, į` → `i`
- `ô, ö, ó, ò, õ, ø` → `o`
- `ù, û, ü, ú, ų` → `u`
- `ç, ć, č` → `c`
- Support majuscules et minuscules

**2. Nettoyage des Caractères Spéciaux**
- Ponctuation : `:;,.!?()[]{}` → supprimés
- Guillemets : `"'«»` → espaces
- Tirets et slashes : `-/_\|` → espaces
- Symboles : `+*=%#@°™®©` → supprimés
- Conversions intelligentes : `&` → `et`, `€` → `euro`

**3. Normalisation des Espaces**
- Espaces multiples → espace unique
- Suppression espaces début/fin
- Tirets → espaces

**4. Optimisation SEO**
- Suppression mots vides en début/fin
- Préservation du sens global
- Compatibilité clustering

#### 🎯 **Impact sur le Clustering**

**Avant la normalisation :**
```
"Complément alimentaire à base de collagène" ≠ "complement alimentaire a base de collagene"
"Gélules de collagène" ≠ "gelules de collagene"
"Où acheter ?" ≠ "ou acheter"
```

**Après la normalisation :**
```
"complement alimentaire a base de collagene" = "complement alimentaire a base de collagene" ✅
"gelules de collagene" = "gelules de collagene" ✅
"ou acheter" = "ou acheter" ✅
```

## 🔍 **Clustering Adaptatif Multi-Niveaux**

### 📊 **Détection de Patterns Spécifiques**

Notre algorithme détecte automatiquement 7 types de patterns :

1. **Dosage** : `par jour`, `dose`, `quantité`, `mg`, `gélule`
2. **Type/Forme** : `poudre`, `marin`, `végétal`, `bio`, `capsule`
3. **Effets** : `bénéfice`, `danger`, `aide`, `efficace`
4. **Programme** : `cure`, `traitement`, `posologie`
5. **Comparaison** : `vs`, `différence`, `meilleur`, `choisir`
6. **Achat** : `prix`, `acheter`, `pas cher`, `promo`
7. **Marque** : `avis`, `test`, `recommandation`, `top`

### 🎯 **Algorithme de Clustering Intelligent**

**Seuils Adaptatifs :**
- **> 100 mots-clés** : Seuil 0.25 + bonus 0.15
- **50-100 mots-clés** : Seuil 0.30 + bonus 0.20  
- **< 50 mots-clés** : Seuil 0.35 + bonus 0.25

**Critères de Regroupement :**
1. Même pattern + même intention + similarité > seuil
2. Même intention + groupes partagés + similarité > seuil+0.1
3. Similarité pure > seuil+0.3

**Bonus de Similarité :**
- Pattern identique : +0.15-0.25
- Même intention : +0.1
- Correspondance exacte normalisée : +0.2

### 📈 **Subdivision Automatique**

- **Clusters > 15 mots-clés** → Subdivision par patterns
- **Minimum 3 mots-clés** par sous-cluster
- **Labels intelligents** avec contexte

## 📊 **Analyse de Qualité Intégrée**

### 🎯 **Métriques de Performance**

- **Cohérence d'intention** : % mots-clés même intention
- **Distribution des tailles** : Singletons, Petits, Moyens, Grands
- **Recommandations automatiques** : Suggestions d'amélioration
- **Indicateurs visuels** : 🟢 🟡 🔴 selon qualité

### 📋 **Export Enrichi**

**Colonnes d'export :**
- `Keyword` : Mot-clé original
- `Keyword_Normalized` : Version normalisée
- `Volume` : Volume de recherche
- `Intent` : Intention détectée
- `Semantic_Groups` : Groupes sémantiques
- `Specific_Pattern` : Pattern spécifique
- `Cluster` : ID du cluster
- `Cluster_Label` : Label intelligent

**Formats disponibles :**
- **CSV** : Export simple
- **Excel multi-feuilles** :
  - Clustering complet
  - Statistiques par cluster
  - Analyse des intentions
  - Top mots-clés par cluster

## 🚀 **Installation et Utilisation**

### Prérequis
```bash
Python 3.8+
pip install -r requirements.txt
```

### Lancement
```bash
./launch_app.sh
```

### Format des Données
Fichier CSV avec colonnes obligatoires :
- `Keyword` : Mots-clés à analyser
- `Volume` : Volume de recherche mensuel

## 📈 **Exemples de Résultats**

### Avant (clustering basique)
```
Cluster 0: 47 mots-clés "par jour (informational)"
├─ collagène et prise de poids
├─ cure de collagène danger  
├─ combien de magnésium par jour
└─ ...tous mélangés
```

### Après (clustering intelligent)
```
🟢 collagène dosage (informational) - 12 mots-clés - 6,840 volume - 92% cohérence
├─ combien de collagène par jour (320)
├─ quelle dose de collagène par jour (590)
└─ dose collagène par jour (320)

🟢 collagène effets (informational) - 8 mots-clés - 4,200 volume - 88% cohérence  
├─ collagène et prise de poids (720)
├─ collagène perte de poids (170)
└─ peptide de collagène danger (390)

🟢 collagène type forme (informational) - 6 mots-clés - 2,880 volume - 100% cohérence
├─ collagène de type 1 (480)
├─ gélules de collagène (720)
└─ poudre de collagène marin (140)
```

## 🎯 **Avantages Business**

### Pour les SEO :
- **Clusters par intention** → Contenus adaptés au funnel
- **Groupement thématique** → Architecture site optimisée
- **Labels automatiques** → Fini la catégorisation manuelle

### Pour les Rédacteurs :
- **Briefs précis** par cluster d'intention
- **Mots-clés connexes** facilement identifiables
- **Contexte sémantique** pour chaque groupe

### Pour les Analystes :
- **Métriques par intention** (volume informationnel vs transactionnel)
- **Identification des gaps** de contenu
- **Priorisation** basée sur le volume par cluster

## 🔧 **Configuration Avancée**

Le fichier `config/settings.yaml` permet de personnaliser :
- Seuils de clustering
- Patterns de détection
- Langues supportées
- Formats d'export

---

**🎯 Clustering Sémantique Intelligent - Transformez vos mots-clés en stratégie SEO !**
