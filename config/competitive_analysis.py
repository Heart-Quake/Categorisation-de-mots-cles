# Module d'analyse concurrentielle pour l'enrichissement SEO
# Expertise en intelligence competitive et analyse de marché

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
import requests
from urllib.parse import urljoin, urlparse
import time
from dataclasses import dataclass
from enum import Enum
import logging

class CompetitorLevel(Enum):
    """Niveaux de compétition"""
    LOW = "Faible"
    MEDIUM = "Moyenne"
    HIGH = "Forte"
    VERY_HIGH = "Très forte"

@dataclass
class CompetitorInsight:
    """Structure des insights concurrentiels"""
    keyword: str
    competition_level: CompetitorLevel
    top_competitors: List[str]
    market_opportunity: float  # 0-1 score
    content_gaps: List[str]
    recommended_strategy: str

class CompetitiveAnalyzer:
    """
    Analyseur concurrentiel avancé pour l'optimisation SEO
    """
    
    def __init__(self, config: Dict = None):
        self.config = config or self._default_config()
        self.logger = logging.getLogger(__name__)
        
        # Cache pour éviter les requêtes répétées
        self.cache = {}
    
    def _default_config(self) -> Dict:
        """Configuration par défaut de l'analyse concurrentielle"""
        return {
            'serp_analysis': {
                'max_results': 10,
                'features_to_analyze': [
                    'featured_snippets',
                    'people_also_ask',
                    'local_pack',
                    'images',
                    'videos',
                    'shopping_results'
                ]
            },
            'competition_thresholds': {
                'low': 0.3,
                'medium': 0.6,
                'high': 0.8
            },
            'market_opportunity': {
                'volume_weight': 0.4,
                'competition_weight': 0.3,
                'trend_weight': 0.3
            }
        }
    
    def analyze_serp_features(self, keywords: List[str]) -> Dict[str, Dict]:
        """
        Analyse des features SERP pour identifier les opportunités
        """
        serp_analysis = {}
        
        for keyword in keywords:
            # Simulation d'analyse SERP (en production, utiliser une API comme SerpAPI)
            features = self._simulate_serp_features(keyword)
            
            serp_analysis[keyword] = {
                'features_present': features,
                'opportunity_score': self._calculate_opportunity_score(features),
                'content_strategy': self._recommend_content_strategy(features),
                'competition_level': self._assess_competition_level(features)
            }
        
        return serp_analysis
    
    def _simulate_serp_features(self, keyword: str) -> Dict[str, bool]:
        """
        Simulation des features SERP basée sur des patterns de mots-clés
        En production, remplacer par des appels API réels
        """
        keyword_lower = keyword.lower()
        
        # Patterns pour différentes features SERP
        patterns = {
            'featured_snippets': [
                'comment', 'pourquoi', 'qu\'est-ce que', 'définition',
                'guide', 'tutoriel', 'étapes'
            ],
            'people_also_ask': [
                'comment', 'pourquoi', 'quand', 'où', 'qui', 'quoi'
            ],
            'local_pack': [
                'près de moi', 'à proximité', 'magasin', 'restaurant',
                'médecin', 'coiffeur', 'garage'
            ],
            'images': [
                'photo', 'image', 'design', 'modèle', 'style',
                'couleur', 'inspiration'
            ],
            'videos': [
                'vidéo', 'tutorial', 'comment faire', 'démonstration',
                'review', 'test'
            ],
            'shopping_results': [
                'prix', 'achat', 'acheter', 'pas cher', 'promo',
                'solde', 'comparatif'
            ]
        }
        
        features = {}
        for feature, feature_patterns in patterns.items():
            features[feature] = any(pattern in keyword_lower for pattern in feature_patterns)
        
        return features
    
    def _calculate_opportunity_score(self, features: Dict[str, bool]) -> float:
        """
        Calcul du score d'opportunité basé sur les features SERP
        """
        # Pondération des features par leur valeur SEO
        feature_weights = {
            'featured_snippets': 0.25,
            'people_also_ask': 0.20,
            'local_pack': 0.15,
            'images': 0.15,
            'videos': 0.15,
            'shopping_results': 0.10
        }
        
        opportunity_score = 0
        for feature, present in features.items():
            if present and feature in feature_weights:
                opportunity_score += feature_weights[feature]
        
        return min(opportunity_score, 1.0)
    
    def _recommend_content_strategy(self, features: Dict[str, bool]) -> str:
        """
        Recommandation de stratégie de contenu basée sur les features SERP
        """
        strategies = []
        
        if features.get('featured_snippets'):
            strategies.append("Optimiser pour les featured snippets avec du contenu structuré")
        
        if features.get('people_also_ask'):
            strategies.append("Créer du contenu FAQ pour People Also Ask")
        
        if features.get('local_pack'):
            strategies.append("Optimiser pour le SEO local avec Google My Business")
        
        if features.get('images'):
            strategies.append("Optimiser les images avec alt-text et données structurées")
        
        if features.get('videos'):
            strategies.append("Créer du contenu vidéo pour YouTube et intégrer sur le site")
        
        if features.get('shopping_results'):
            strategies.append("Optimiser les fiches produits avec données structurées")
        
        return " | ".join(strategies) if strategies else "Stratégie de contenu standard"
    
    def _assess_competition_level(self, features: Dict[str, bool]) -> CompetitorLevel:
        """
        Évaluation du niveau de compétition basé sur les features SERP
        """
        feature_count = sum(features.values())
        
        if feature_count >= 4:
            return CompetitorLevel.VERY_HIGH
        elif feature_count >= 3:
            return CompetitorLevel.HIGH
        elif feature_count >= 2:
            return CompetitorLevel.MEDIUM
        else:
            return CompetitorLevel.LOW
    
    def analyze_market_gaps(self, df: pd.DataFrame) -> Dict[str, List[str]]:
        """
        Identification des gaps de marché par domaine
        """
        market_gaps = {}
        
        # Analyse par domaine
        for domain in df['Domain'].unique():
            if pd.isna(domain):
                continue
                
            domain_df = df[df['Domain'] == domain]
            
            # Identification des sous-domaines manquants
            all_subdomains = set()
            current_subdomains = set(domain_df['Subdomain'].dropna().unique())
            
            # Sous-domaines potentiels par domaine (base de connaissances)
            subdomain_suggestions = {
                'Santé & Nutrition': [
                    'Compléments alimentaires', 'Nutrition sportive', 'Régimes spécialisés',
                    'Santé mentale', 'Prévention', 'Médecine alternative'
                ],
                'Beauté & Cosmétique': [
                    'Soins anti-âge', 'Maquillage professionnel', 'Soins hommes',
                    'Beauté bio', 'Parfums', 'Soins capillaires'
                ],
                'Sport & Fitness': [
                    'Musculation', 'Cardio-training', 'Sports collectifs',
                    'Nutrition sportive', 'Équipements', 'Récupération'
                ],
                'Maison & Jardin': [
                    'Décoration intérieure', 'Jardinage', 'Bricolage',
                    'Électroménager', 'Mobilier', 'Éclairage'
                ]
            }
            
            potential_subdomains = subdomain_suggestions.get(domain, [])
            missing_subdomains = [sub for sub in potential_subdomains if sub not in current_subdomains]
            
            market_gaps[domain] = missing_subdomains
        
        return market_gaps
    
    def calculate_keyword_difficulty(self, keywords: List[str]) -> Dict[str, float]:
        """
        Calcul de la difficulté des mots-clés (simulation)
        En production, utiliser des APIs comme Ahrefs ou SEMrush
        """
        difficulty_scores = {}
        
        for keyword in keywords:
            # Simulation basée sur la longueur et les patterns
            keyword_lower = keyword.lower()
            base_difficulty = 0.5
            
            # Facteurs augmentant la difficulté
            if len(keyword.split()) == 1:  # Mots-clés courts
                base_difficulty += 0.3
            
            if any(word in keyword_lower for word in ['achat', 'prix', 'meilleur']):
                base_difficulty += 0.2  # Mots-clés commerciaux
            
            if any(word in keyword_lower for word in ['gratuit', 'pas cher']):
                base_difficulty += 0.1  # Mots-clés populaires
            
            # Facteurs diminuant la difficulté
            if len(keyword.split()) >= 4:  # Long tail
                base_difficulty -= 0.2
            
            if any(word in keyword_lower for word in ['comment', 'pourquoi', 'guide']):
                base_difficulty -= 0.1  # Mots-clés informationnels
            
            difficulty_scores[keyword] = max(0.1, min(1.0, base_difficulty))
        
        return difficulty_scores
    
    def generate_competitive_insights(self, df: pd.DataFrame) -> List[CompetitorInsight]:
        """
        Génération d'insights concurrentiels complets
        """
        insights = []
        
        # Analyse SERP
        keywords = df['Keyword'].tolist()
        serp_analysis = self.analyze_serp_features(keywords)
        
        # Calcul de difficulté
        difficulty_scores = self.calculate_keyword_difficulty(keywords)
        
        # Analyse des gaps
        market_gaps = self.analyze_market_gaps(df)
        
        for _, row in df.iterrows():
            keyword = row['Keyword']
            domain = row.get('Domain', 'Unknown')
            
            # Récupération des données d'analyse
            serp_data = serp_analysis.get(keyword, {})
            difficulty = difficulty_scores.get(keyword, 0.5)
            
            # Calcul de l'opportunité de marché
            volume = row.get('Volume', 0)
            volume_normalized = min(volume / 10000, 1.0) if volume > 0 else 0
            
            market_opportunity = (
                volume_normalized * self.config['market_opportunity']['volume_weight'] +
                (1 - difficulty) * self.config['market_opportunity']['competition_weight'] +
                serp_data.get('opportunity_score', 0) * self.config['market_opportunity']['trend_weight']
            )
            
            # Recommandation stratégique
            if market_opportunity > 0.7:
                strategy = "Priorité haute - Opportunité excellente"
            elif market_opportunity > 0.5:
                strategy = "Priorité moyenne - Opportunité modérée"
            elif market_opportunity > 0.3:
                strategy = "Priorité faible - Surveillance recommandée"
            else:
                strategy = "Éviter - Trop compétitif pour le ROI"
            
            insight = CompetitorInsight(
                keyword=keyword,
                competition_level=serp_data.get('competition_level', CompetitorLevel.MEDIUM),
                top_competitors=["Concurrent 1", "Concurrent 2", "Concurrent 3"],  # Simulation
                market_opportunity=market_opportunity,
                content_gaps=market_gaps.get(domain, []),
                recommended_strategy=strategy
            )
            
            insights.append(insight)
        
        return insights

class SERPFeatureOptimizer:
    """
    Optimiseur spécialisé pour les features SERP
    """
    
    def __init__(self):
        self.optimization_rules = self._load_optimization_rules()
    
    def _load_optimization_rules(self) -> Dict:
        """
        Règles d'optimisation pour chaque feature SERP
        """
        return {
            'featured_snippets': {
                'content_structure': [
                    "Utiliser des listes à puces ou numérotées",
                    "Répondre directement à la question en 40-60 mots",
                    "Utiliser des balises HTML structurées (H2, H3)",
                    "Inclure des données structurées FAQ"
                ],
                'content_length': "40-60 mots pour la réponse principale",
                'format_preference': "Paragraphe, liste, ou tableau"
            },
            'people_also_ask': {
                'content_structure': [
                    "Créer une section FAQ complète",
                    "Utiliser des questions naturelles comme sous-titres",
                    "Répondre de manière concise et complète",
                    "Lier les questions connexes"
                ],
                'question_format': "Questions commençant par qui, quoi, où, quand, pourquoi, comment",
                'answer_length': "2-3 phrases par question"
            },
            'local_pack': {
                'optimization_factors': [
                    "Optimiser Google My Business",
                    "Obtenir des avis clients positifs",
                    "Utiliser des mots-clés géolocalisés",
                    "Créer du contenu local pertinent"
                ],
                'schema_markup': "LocalBusiness, Organization",
                'citation_consistency': "NAP (Name, Address, Phone) cohérent"
            }
        }
    
    def generate_optimization_recommendations(self, serp_features: Dict[str, bool]) -> List[str]:
        """
        Génération de recommandations d'optimisation spécifiques
        """
        recommendations = []
        
        for feature, present in serp_features.items():
            if present and feature in self.optimization_rules:
                rules = self.optimization_rules[feature]
                
                if 'content_structure' in rules:
                    recommendations.extend([
                        f"Pour {feature}: {rule}" for rule in rules['content_structure']
                    ])
                
                if 'schema_markup' in rules:
                    recommendations.append(
                        f"Implémenter le schema markup {rules['schema_markup']} pour {feature}"
                    )
        
        return recommendations

# Configuration des seuils d'analyse concurrentielle
COMPETITIVE_ANALYSIS_CONFIG = {
    'priority_matrix': {
        'high_volume_low_competition': {'min_volume': 1000, 'max_difficulty': 0.4},
        'medium_volume_medium_competition': {'min_volume': 500, 'max_difficulty': 0.6},
        'low_volume_high_opportunity': {'min_volume': 100, 'max_difficulty': 0.8}
    },
    'market_trends': {
        'emerging_keywords': [
            'ia', 'intelligence artificielle', 'durabilité', 'bio',
            'télétravail', 'wellness', 'mindfulness'
        ],
        'declining_keywords': [
            'flash', 'cd', 'dvd', 'fax', 'annuaire'
        ]
    },
    'content_gap_analysis': {
        'min_content_length': 300,
        'required_elements': ['title', 'meta_description', 'h1', 'structured_data'],
        'quality_indicators': ['readability_score', 'keyword_density', 'internal_links']
    }
} 