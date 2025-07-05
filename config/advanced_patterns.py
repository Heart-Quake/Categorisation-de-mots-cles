# Configuration avancée pour la catégorisation sémantique
# Patterns enrichis et hiérarchiques

# Domaines métier avec sous-catégories hiérarchiques
ADVANCED_DOMAIN_PATTERNS = {
    'sante_nutrition': {
        'name': 'Santé & Nutrition',
        'sub_categories': {
            'complements_alimentaires': {
                'name': 'Compléments Alimentaires',
                'patterns': [
                    'vitamine', 'mineral', 'omega', 'probiotique', 'magnesium', 'calcium',
                    'fer', 'zinc', 'complement', 'gelule', 'capsule', 'comprime'
                ]
            },
            'huiles_essentielles': {
                'name': 'Huiles Essentielles',
                'patterns': [
                    'huile essentielle', 'he ', 'aromatherapie', 'eucalyptus', 'lavande',
                    'tea tree', 'menthe poivree', 'citron', 'orange douce', 'diffuseur'
                ]
            },
            'nutrition_bio': {
                'name': 'Nutrition Bio',
                'patterns': [
                    'bio', 'organic', 'naturel', 'sans gluten', 'vegan', 'vegetarien',
                    'sans lactose', 'sans sucre', 'superaliment', 'graines', 'cereales'
                ]
            },
            'sante_generale': {
                'name': 'Santé Générale',
                'patterns': [
                    'medicament', 'traitement', 'symptome', 'maladie', 'douleur',
                    'inflammation', 'infection', 'allergie', 'stress', 'sommeil'
                ]
            }
        }
    },
    'beaute_cosmetique': {
        'name': 'Beauté & Cosmétique',
        'sub_categories': {
            'soins_visage': {
                'name': 'Soins Visage',
                'patterns': [
                    'creme visage', 'serum', 'nettoyant', 'demaquillant', 'masque',
                    'anti age', 'anti rides', 'hydratant', 'purifiant', 'exfoliant'
                ]
            },
            'soins_corps': {
                'name': 'Soins Corps',
                'patterns': [
                    'creme corps', 'lait corps', 'huile corps', 'gommage', 'gel douche',
                    'savon', 'baume', 'lotion', 'emulsion', 'beurre'
                ]
            },
            'maquillage': {
                'name': 'Maquillage',
                'patterns': [
                    'fond de teint', 'mascara', 'rouge levres', 'eye liner', 'fard',
                    'poudre', 'blush', 'crayon', 'palette', 'vernis'
                ]
            },
            'cheveux': {
                'name': 'Soins Cheveux',
                'patterns': [
                    'shampooing', 'apres shampooing', 'masque cheveux', 'huile cheveux',
                    'serum cheveux', 'spray', 'mousse', 'gel', 'cire', 'laque'
                ]
            }
        }
    },
    'sport_fitness': {
        'name': 'Sport & Fitness',
        'sub_categories': {
            'nutrition_sportive': {
                'name': 'Nutrition Sportive',
                'patterns': [
                    'proteine', 'whey', 'caseine', 'bcaa', 'creatine', 'pre workout',
                    'post workout', 'gainer', 'bruleur graisse', 'boisson energetique'
                ]
            },
            'equipement_fitness': {
                'name': 'Équipement Fitness',
                'patterns': [
                    'haltere', 'barre', 'banc', 'tapis course', 'velo', 'elliptique',
                    'rameur', 'kettlebell', 'elastique', 'corde sauter'
                ]
            },
            'vetements_sport': {
                'name': 'Vêtements Sport',
                'patterns': [
                    'tenue sport', 'legging', 'brassiere', 'short', 'debardeur',
                    'chaussure sport', 'running', 'basket', 'textile technique'
                ]
            }
        }
    },
    'maison_jardin': {
        'name': 'Maison & Jardin',
        'sub_categories': {
            'decoration': {
                'name': 'Décoration',
                'patterns': [
                    'decoration', 'meuble', 'luminaire', 'rideau', 'coussin',
                    'tapis', 'vase', 'cadre', 'miroir', 'bougie'
                ]
            },
            'jardinage': {
                'name': 'Jardinage',
                'patterns': [
                    'plante', 'fleur', 'graine', 'terreau', 'engrais', 'arrosoir',
                    'bêche', 'sécateur', 'tondeuse', 'taille haie'
                ]
            },
            'bricolage': {
                'name': 'Bricolage',
                'patterns': [
                    'outil', 'perceuse', 'visseuse', 'marteau', 'tournevis',
                    'scie', 'niveau', 'metre', 'clou', 'vis'
                ]
            }
        }
    }
}

# Patterns Consumer Journey enrichis avec scoring
ADVANCED_CONSUMER_JOURNEY = {
    'discovery': {
        'name': 'Découverte',
        'description': 'Recherche générale, prise de conscience du besoin',
        'patterns': {
            'generic_terms': {
                'weight': 3,
                'keywords': ['qu est ce que', 'c est quoi', 'definition', 'guide', 'conseil', 'astuce']
            },
            'category_exploration': {
                'weight': 2,
                'keywords': ['type de', 'genre de', 'sorte de', 'meilleur', 'top', 'comparatif']
            },
            'problem_awareness': {
                'weight': 2,
                'keywords': ['probleme', 'solution', 'comment', 'pourquoi', 'quand', 'ou']
            }
        }
    },
    'consideration': {
        'name': 'Considération',
        'description': 'Évaluation des options, comparaison',
        'patterns': {
            'comparison': {
                'weight': 3,
                'keywords': ['vs', 'ou', 'comparaison', 'difference', 'mieux', 'choisir']
            },
            'criteria_evaluation': {
                'weight': 2,
                'keywords': ['avis', 'test', 'review', 'note', 'qualite', 'prix']
            },
            'feature_focus': {
                'weight': 2,
                'keywords': ['avec', 'sans', 'bio', 'naturel', 'efficace', 'rapide']
            }
        }
    },
    'transaction': {
        'name': 'Transaction',
        'description': 'Intention d\'achat immédiate',
        'patterns': {
            'purchase_intent': {
                'weight': 3,
                'keywords': ['acheter', 'achat', 'commander', 'livraison', 'prix', 'pas cher']
            },
            'specific_product': {
                'weight': 3,
                'keywords': ['marque', 'modele', 'reference', 'promo', 'solde', 'reduction']
            },
            'urgency': {
                'weight': 2,
                'keywords': ['urgent', 'rapide', 'immediat', 'express', 'stock', 'disponible']
            }
        }
    },
    'informational': {
        'name': 'Informationnel',
        'description': 'Recherche d\'information complexe',
        'patterns': {
            'how_to': {
                'weight': 3,
                'keywords': ['comment utiliser', 'mode emploi', 'tutorial', 'etape', 'methode']
            },
            'deep_knowledge': {
                'weight': 2,
                'keywords': ['bienfait', 'propriete', 'effet', 'composition', 'ingredient']
            },
            'expert_advice': {
                'weight': 2,
                'keywords': ['expert', 'specialiste', 'professionnel', 'medecin', 'nutritionniste']
            }
        }
    }
}

# Patterns de volume pour ajuster la classification
VOLUME_PATTERNS = {
    'high_volume': {
        'threshold': 10000,
        'journey_boost': {
            'discovery': 1.2,  # Les gros volumes sont souvent en découverte
            'consideration': 1.0,
            'transaction': 0.8,
            'informational': 0.9
        }
    },
    'medium_volume': {
        'threshold': 1000,
        'journey_boost': {
            'discovery': 1.0,
            'consideration': 1.3,  # Volume moyen souvent en considération
            'transaction': 1.1,
            'informational': 1.0
        }
    },
    'low_volume': {
        'threshold': 100,
        'journey_boost': {
            'discovery': 0.8,
            'consideration': 1.1,
            'transaction': 1.4,  # Longue traîne souvent transactionnelle
            'informational': 1.2
        }
    }
}

# Mapping des intentions vers les types de contenu
INTENT_TO_CONTENT_MAPPING = {
    'informational': ['Blog Article', 'Guide Page', 'FAQ Page'],
    'commercial': ['Category Page', 'Comparison Page', 'Landing Page'],
    'transactional': ['Product Page', 'Shopping Page', 'Checkout Page'],
    'navigational': ['Homepage', 'Brand Page', 'Contact Page']
}

# Segments client avec patterns comportementaux
CUSTOMER_SEGMENTS = {
    'beginner': {
        'name': 'Débutant',
        'patterns': ['debuter', 'commencer', 'premier', 'facile', 'simple', 'guide']
    },
    'intermediate': {
        'name': 'Intermédiaire',
        'patterns': ['ameliorer', 'progresser', 'niveau', 'technique', 'avance']
    },
    'expert': {
        'name': 'Expert',
        'patterns': ['professionnel', 'expert', 'specialise', 'technique', 'pointe']
    },
    'price_sensitive': {
        'name': 'Sensible au Prix',
        'patterns': ['pas cher', 'economique', 'budget', 'promo', 'solde', 'reduction']
    },
    'premium': {
        'name': 'Premium',
        'patterns': ['haut de gamme', 'luxe', 'premium', 'qualite', 'exclusif']
    }
}

# Configuration des clusters hiérarchiques
CLUSTER_HIERARCHY = {
    'max_clusters': 50,
    'min_cluster_size': 3,
    'hierarchy_levels': {
        'domain': 1,      # Niveau 1: Domaine métier
        'subdomain': 2,   # Niveau 2: Sous-domaine
        'intent': 3,      # Niveau 3: Intention
        'journey': 4      # Niveau 4: Consumer Journey
    }
}

SEO_SYNONYMS = {
    # Immobilier
    "appartement": ["studio", "logement", "habitation", "appart", "loft", "duplex", "T2", "T3", "F2", "F3"],
    "maison": ["villa", "pavillon", "demeure", "résidence", "bâtisse", "longère", "fermette", "maisonette"],
    "location": ["louer", "bail", "appartement à louer", "maison à louer", "colocation", "locatif"],
    "achat": ["acquisition", "acheter", "investir", "investissement", "acquéreur"],
    "vente": ["vendre", "cession", "transaction", "mandat", "revente"],
    "terrain": ["parcelle", "lot", "propriété foncière"],

    # Automobile & Transport
    "voiture": ["auto", "véhicule", "bagnole", "automobile", "berline", "break", "SUV", "4x4", "citadine"],
    "moto": ["motocyclette", "scooter", "deux-roues", "cyclo", "mob", "trail", "roadster"],
    "camion": ["utilitaire", "fourgon", "camionnette", "poids lourd", "semi-remorque"],
    "location voiture": ["louer voiture", "voiture de location", "location auto", "auto partagée", "autopartage"],
    "assurance auto": ["assurance voiture", "assurance automobile", "assurance véhicule", "RC auto"],
    "garage": ["atelier auto", "réparateur", "mécanicien", "station-service"],

    # E-commerce & Shopping
    "acheter": ["achat", "commander", "commande", "acquérir", "panier", "shopping", "e-achat"],
    "prix": ["tarif", "coût", "montant", "valeur", "prix public", "prix promo", "prix barré"],
    "promotion": ["promo", "réduction", "remise", "soldes", "offre spéciale", "bon plan", "code promo"],
    "livraison": ["expédition", "envoi", "transport", "colis", "frais de port", "point relais"],
    "boutique": ["magasin", "store", "shop", "e-shop", "e-boutique", "marketplace"],

    # Mode & Vêtements
    "vêtement": ["habit", "tenue", "fringue", "linge", "prêt-à-porter", "outfit", "look"],
    "chaussure": ["soulier", "basket", "sneaker", "bottine", "escarpin", "mocassin", "sandale", "claquette"],
    "robe": ["jupe", "tunique", "dress", "chemise longue"],
    "pantalon": ["jean", "legging", "slim", "jogging", "chino", "cargo"],
    "manteau": ["veste", "blouson", "anorak", "parka", "doudoune", "imperméable"],

    # Beauté & Cosmétique
    "maquillage": ["make-up", "cosmétique", "fard", "palette", "mascara", "fond de teint"],
    "soin visage": ["crème visage", "hydratant", "lotion", "sérum", "gommage", "masque"],
    "parfum": ["eau de toilette", "fragrance", "eau de parfum", "déodorant", "brume"],
    "shampoing": ["shampoo", "soin cheveux", "après-shampoing", "masque capillaire"],

    # Santé & Bien-être
    "médecin": ["docteur", "généraliste", "praticien", "médecin traitant", "consultation"],
    "pharmacie": ["parapharmacie", "officine", "pharmacien", "pharma"],
    "mutuelle": ["assurance santé", "complémentaire santé", "mutualiste"],
    "psychologue": ["psy", "thérapeute", "psychothérapeute", "psychiatre"],
    "kiné": ["kinésithérapeute", "rééducateur", "ostéopathe"],

    # Alimentation & Cuisine
    "recette": ["plat", "préparation", "cuisine", "menu", "idée repas", "cuisine facile"],
    "restaurant": ["resto", "bistrot", "brasserie", "auberge", "table", "food court"],
    "livraison repas": ["commande repas", "plat à emporter", "take away", "click & collect"],
    "boulangerie": ["pâtisserie", "boulange", "boulanger", "viennoiserie"],
    "supermarché": ["hypermarché", "grande surface", "drive", "épicerie"],

    # Hôtellerie & Tourisme
    "hôtel": ["hostel", "auberge", "chambre d’hôtes", "gîte", "résidence hôtelière", "motel"],
    "voyage": ["séjour", "trip", "tourisme", "vacances", "circuit", "road trip"],
    "vol": ["avion", "billet d’avion", "aérien", "compagnie aérienne"],
    "location vacances": ["gîte", "maison de vacances", "appartement vacances", "airbnb"],

    # Loisirs & Culture
    "cinéma": ["film", "projection", "salle obscure", "séance", "ciné"],
    "musique": ["chanson", "morceau", "titre", "album", "playlist", "concert"],
    "livre": ["roman", "ouvrage", "bouquin", "publication", "bande dessinée", "BD", "manga"],
    "jeu vidéo": ["gaming", "console", "jeu", "vidéogame", "esport", "jeux en ligne"],
    "spectacle": ["théâtre", "comédie", "one man show", "représentation"],

    # Sport & Activités
    "sport": ["activité physique", "discipline sportive", "exercice", "fitness"],
    "football": ["foot", "soccer", "futsal"],
    "basketball": ["basket", "NBA"],
    "tennis": ["raquette", "court de tennis", "tennisman"],
    "salle de sport": ["fitness", "gym", "club de sport", "musculation", "crossfit"],
    "yoga": ["méditation", "relaxation", "pilates"],

    # Maison & Bricolage
    "meuble": ["mobilier", "table", "chaise", "canapé", "armoire", "commode"],
    "décoration": ["déco", "ornement", "aménagement", "design intérieur"],
    "bricolage": ["DIY", "travaux", "réparation", "outillage", "rénovation"],
    "jardin": ["potager", "espace vert", "extérieur", "terrasse", "balcon"],

    # High-Tech & Informatique
    "ordinateur": ["pc", "laptop", "portable", "ordinateur portable", "notebook"],
    "téléphone": ["mobile", "gsm", "smartphone", "cellulaire", "iphone", "android"],
    "tablette": ["ipad", "galaxy tab", "tablette tactile"],
    "imprimante": ["printer", "copieur", "scanner", "multifonction"],
    "télévision": ["tv", "écran plat", "smart tv"],

    # Assurance & Finance
    "banque": ["établissement bancaire", "agence bancaire", "banquier"],
    "crédit": ["prêt", "emprunt", "financement", "microcrédit"],
    "assurance": ["mutuelle", "protection", "garantie", "assureur"],
    "bourse": ["marché financier", "actions", "investissement", "trading"],

    # RH & Emploi
    "emploi": ["job", "travail", "poste", "boulot", "recrutement", "offre d’emploi"],
    "recrutement": ["embauche", "chasse de tête", "sélection", "job board"],
    "cv": ["curriculum vitae", "résumé", "profil", "parcours"],
    "formation": ["cours", "apprentissage", "stage", "MOOC", "e-learning"],

    # Juridique & Administratif
    "avocat": ["conseil juridique", "juriste", "cabinet d’avocat", "défenseur"],
    "notaire": ["officier public", "étude notariale", "acte notarié"],
    "contrat": ["accord", "convention", "engagement", "signature"],
    "démarche": ["procédure", "formalités", "processus", "administratif"],

    # Parentalité & Enfance
    "crèche": ["garderie", "halte-garderie", "micro-crèche"],
    "école": ["établissement scolaire", "primaire", "collège", "lycée", "université"],
    "poussette": ["landau", "carriole", "buggy"],
    "jouet": ["jeu", "peluche", "doudou", "joujou"],

    # Animaux
    "chien": ["canidé", "toutou", "chiot", "dog"],
    "chat": ["félin", "minou", "chaton", "cat"],
    "vétérinaire": ["véto", "docteur animalier", "clinique vétérinaire"],
    "animalerie": ["magasin animaux", "boutique animaux"],

    # Energie & Environnement
    "électricité": ["courant", "énergie électrique", "EDF"],
    "gaz": ["énergie gaz", "gaz naturel", "GRDF"],
    "panneau solaire": ["photovoltaïque", "solaire", "énergie renouvelable"],
    "chauffage": ["radiateur", "chaudière", "pompe à chaleur"],

    # Transport & Mobilité
    "train": ["sncf", "tgv", "ter", "rail"],
    "bus": ["autocar", "navette", "car"],
    "taxi": ["chauffeur", "voiture de transport", "VTC", "uber"],
    "vélo": ["bicyclette", "cycle", "vélib"],

    # Agriculture & Agroalimentaire
    "ferme": ["exploitation agricole", "agriculteur", "élevage"],
    "céréale": ["blé", "orge", "maïs", "riz"],
    "vin": ["cave", "vignoble", "domaine viticole", "œnologie"],

    # Industrie & BTP
    "chantier": ["travaux", "construction", "bâtiment", "gros œuvre"],
    "machine": ["engin", "appareil", "équipement", "outil industriel"],
    "usine": ["site industriel", "atelier", "production"],

    # Services B2B
    "logiciel": ["application", "programme", "solution digitale", "SaaS"],
    "consultant": ["expert", "conseiller", "prestataire"],
    "audit": ["contrôle", "vérification", "diagnostic"],

    # Santé animale
    "croquette": ["alimentation chien", "alimentation chat", "nourriture animale"],

    # Autres généralistes (ultra-enrichi)
    "avis": ["opinion", "retour", "témoignage", "review", "note", "évaluation"],
    "conseil": ["astuce", "recommandation", "suggestion", "tip"],
    "guide": ["tutoriel", "mode d’emploi", "notice", "manuel", "how-to"],
    "comparatif": ["comparaison", "match", "vs", "versus", "comparateur"],
    "meilleur": ["top", "plus efficace", "plus performant", "best of"],
    "pas cher": ["discount", "prix bas", "bon marché", "low cost"],
    "gratuit": ["free", "sans frais", "offert", "zéro euro"],
    "proche": ["près de", "à côté de", "à proximité", "voisin"],
    "urgence": ["dépannage", "immédiat", "rapidement", "SOS"],
    "numéro": ["téléphone", "contact", "hotline", "service client"],
    "horaire": ["heures d’ouverture", "planning", "calendrier", "agenda"],
    "adresse": ["localisation", "lieu", "emplacement", "coordonnées"],
    "service": ["prestation", "offre", "solution", "aide"],
    "site": ["plateforme", "portail", "web", "site internet"],
    "forum": ["communauté", "discussion", "groupe", "board"],
    "actualité": ["news", "information", "dernier", "actualité récente"],
    "événement": ["salon", "foire", "manifestation", "expo", "conférence"],
    "offre": ["promotion", "deal", "bon plan", "remise"],
} 