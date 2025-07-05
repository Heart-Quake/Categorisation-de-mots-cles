# Module d'amélioration Machine Learning pour la catégorisation SEO
# Expertise Data Science avancée

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.model_selection import cross_val_score, GridSearchCV
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.preprocessing import LabelEncoder
import joblib
from typing import Dict, List, Tuple, Optional
import logging

class AdvancedSEOClassifier:
    """
    Classificateur ML avancé pour la catégorisation sémantique SEO
    Intègre les meilleures pratiques de data science
    """
    
    def __init__(self, config: Dict = None):
        self.config = config or self._default_config()
        self.models = {}
        self.vectorizers = {}
        self.label_encoders = {}
        self.is_trained = False
        
        # Configuration logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def _default_config(self) -> Dict:
        """Configuration par défaut optimisée pour le SEO"""
        return {
            'vectorizer': {
                'max_features': 10000,
                'ngram_range': (1, 3),
                'min_df': 2,
                'max_df': 0.95,
                'stop_words': None  # Géré séparément pour le français
            },
            'models': {
                'domain': {
                    'algorithm': 'random_forest',
                    'n_estimators': 200,
                    'max_depth': 15,
                    'min_samples_split': 5
                },
                'intent': {
                    'algorithm': 'gradient_boosting',
                    'n_estimators': 150,
                    'learning_rate': 0.1,
                    'max_depth': 10
                },
                'consumer_journey': {
                    'algorithm': 'random_forest',
                    'n_estimators': 100,
                    'max_depth': 12,
                    'class_weight': 'balanced'
                }
            },
            'validation': {
                'cv_folds': 5,
                'test_size': 0.2,
                'random_state': 42
            }
        }
    
    def prepare_features(self, df: pd.DataFrame) -> Dict[str, np.ndarray]:
        """
        Préparation avancée des features pour le ML
        Intègre volume, longueur, patterns linguistiques
        """
        features = {}
        
        # Features textuelles principales
        text_features = df['Keyword'].fillna('')
        
        # Vectorisation TF-IDF
        if 'text' not in self.vectorizers:
            self.vectorizers['text'] = TfidfVectorizer(**self.config['vectorizer'])
            features['text'] = self.vectorizers['text'].fit_transform(text_features)
        else:
            features['text'] = self.vectorizers['text'].transform(text_features)
        
        # Features numériques
        numerical_features = []
        
        # Volume (log-transformé pour normaliser)
        if 'Volume' in df.columns:
            volume_log = np.log1p(df['Volume'].fillna(0))
            numerical_features.append(volume_log.values.reshape(-1, 1))
        
        # Longueur du mot-clé
        keyword_length = df['Keyword'].str.len().fillna(0)
        numerical_features.append(keyword_length.values.reshape(-1, 1))
        
        # Nombre de mots
        word_count = df['Keyword'].str.split().str.len().fillna(0)
        numerical_features.append(word_count.values.reshape(-1, 1))
        
        # Features linguistiques avancées
        # Présence de mots interrogatifs
        question_words = ['comment', 'pourquoi', 'quand', 'où', 'que', 'quoi', 'qui']
        has_question = df['Keyword'].str.contains('|'.join(question_words), case=False, na=False)
        numerical_features.append(has_question.astype(int).values.reshape(-1, 1))
        
        # Présence de mots transactionnels
        transactional_words = ['acheter', 'achat', 'prix', 'pas cher', 'promo', 'solde']
        has_transactional = df['Keyword'].str.contains('|'.join(transactional_words), case=False, na=False)
        numerical_features.append(has_transactional.astype(int).values.reshape(-1, 1))
        
        # Combiner les features numériques
        if numerical_features:
            features['numerical'] = np.hstack(numerical_features)
        
        return features
    
    def train_models(self, df: pd.DataFrame, target_columns: List[str]) -> Dict[str, float]:
        """
        Entraînement des modèles avec validation croisée
        Retourne les scores de performance
        """
        self.logger.info("🤖 Début de l'entraînement des modèles ML")
        
        # Préparation des features
        features = self.prepare_features(df)
        X = np.hstack([features['text'].toarray(), features.get('numerical', np.array([]).reshape(len(df), 0))])
        
        performance_scores = {}
        
        for target_col in target_columns:
            if target_col not in df.columns:
                self.logger.warning(f"⚠️ Colonne {target_col} manquante, ignorée")
                continue
            
            self.logger.info(f"📊 Entraînement pour {target_col}")
            
            # Préparation des labels
            y = df[target_col].fillna('unknown')
            
            # Encodage des labels
            if target_col not in self.label_encoders:
                self.label_encoders[target_col] = LabelEncoder()
                y_encoded = self.label_encoders[target_col].fit_transform(y)
            else:
                y_encoded = self.label_encoders[target_col].transform(y)
            
            # Sélection et configuration du modèle
            model_config = self.config['models'].get(target_col, self.config['models']['domain'])
            
            if model_config['algorithm'] == 'random_forest':
                model = RandomForestClassifier(
                    n_estimators=model_config['n_estimators'],
                    max_depth=model_config['max_depth'],
                    min_samples_split=model_config['min_samples_split'],
                    random_state=self.config['validation']['random_state'],
                    n_jobs=-1
                )
            elif model_config['algorithm'] == 'gradient_boosting':
                model = GradientBoostingClassifier(
                    n_estimators=model_config['n_estimators'],
                    learning_rate=model_config['learning_rate'],
                    max_depth=model_config['max_depth'],
                    random_state=self.config['validation']['random_state']
                )
            else:
                # Fallback sur Random Forest
                model = RandomForestClassifier(random_state=42)
            
            # Validation croisée
            cv_scores = cross_val_score(
                model, X, y_encoded, 
                cv=self.config['validation']['cv_folds'],
                scoring='accuracy'
            )
            
            performance_scores[target_col] = {
                'cv_mean': cv_scores.mean(),
                'cv_std': cv_scores.std(),
                'cv_scores': cv_scores.tolist()
            }
            
            # Entraînement final
            model.fit(X, y_encoded)
            self.models[target_col] = model
            
            self.logger.info(f"✅ {target_col}: Accuracy CV = {cv_scores.mean():.3f} ± {cv_scores.std():.3f}")
        
        self.is_trained = True
        return performance_scores
    
    def predict_with_confidence(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Prédiction avec scores de confiance
        """
        if not self.is_trained:
            raise ValueError("Modèles non entraînés. Appelez train_models() d'abord.")
        
        # Préparation des features
        features = self.prepare_features(df)
        X = np.hstack([features['text'].toarray(), features.get('numerical', np.array([]).reshape(len(df), 0))])
        
        results = df.copy()
        
        for target_col, model in self.models.items():
            # Prédictions
            predictions = model.predict(X)
            probabilities = model.predict_proba(X)
            
            # Décodage des labels
            predictions_decoded = self.label_encoders[target_col].inverse_transform(predictions)
            
            # Score de confiance (probabilité max)
            confidence_scores = np.max(probabilities, axis=1)
            
            # Ajout au DataFrame
            results[f'{target_col}_ML'] = predictions_decoded
            results[f'{target_col}_Confidence_ML'] = confidence_scores
        
        return results
    
    def save_models(self, filepath: str):
        """Sauvegarde des modèles entraînés"""
        model_data = {
            'models': self.models,
            'vectorizers': self.vectorizers,
            'label_encoders': self.label_encoders,
            'config': self.config,
            'is_trained': self.is_trained
        }
        joblib.dump(model_data, filepath)
        self.logger.info(f"💾 Modèles sauvegardés: {filepath}")
    
    def load_models(self, filepath: str):
        """Chargement des modèles pré-entraînés"""
        model_data = joblib.load(filepath)
        self.models = model_data['models']
        self.vectorizers = model_data['vectorizers']
        self.label_encoders = model_data['label_encoders']
        self.config = model_data['config']
        self.is_trained = model_data['is_trained']
        self.logger.info(f"📂 Modèles chargés: {filepath}")

class SEOTrendAnalyzer:
    """
    Analyseur de tendances SEO avec données temporelles
    """
    
    def __init__(self):
        self.seasonal_patterns = {}
        self.trend_data = None
    
    def analyze_seasonality(self, df: pd.DataFrame, date_column: str = None) -> Dict:
        """
        Analyse de la saisonnalité des mots-clés
        """
        if date_column and date_column in df.columns:
            # Analyse temporelle réelle
            df['month'] = pd.to_datetime(df[date_column]).dt.month
            df['quarter'] = pd.to_datetime(df[date_column]).dt.quarter
            
            seasonal_analysis = {
                'monthly_trends': df.groupby(['month', 'Domain'])['Volume'].mean().unstack(fill_value=0),
                'quarterly_trends': df.groupby(['quarter', 'Consumer_Journey'])['Volume'].mean().unstack(fill_value=0)
            }
        else:
            # Patterns saisonniers basés sur les mots-clés
            seasonal_keywords = {
                'spring': ['printemps', 'jardin', 'plante', 'allergie'],
                'summer': ['été', 'vacances', 'solaire', 'plage'],
                'autumn': ['automne', 'rentrée', 'école', 'rhume'],
                'winter': ['hiver', 'noël', 'froid', 'grippe']
            }
            
            seasonal_analysis = {}
            for season, keywords in seasonal_keywords.items():
                pattern = '|'.join(keywords)
                seasonal_mask = df['Keyword'].str.contains(pattern, case=False, na=False)
                seasonal_analysis[season] = {
                    'keyword_count': seasonal_mask.sum(),
                    'total_volume': df[seasonal_mask]['Volume'].sum() if 'Volume' in df.columns else 0
                }
        
        return seasonal_analysis
    
    def predict_trend_impact(self, keywords: List[str]) -> Dict[str, float]:
        """
        Prédiction de l'impact des tendances sur les mots-clés
        """
        # Simulation basée sur des patterns connus
        trend_indicators = {
            'rising': ['ia', 'intelligence artificielle', 'chatgpt', 'bio', 'écologique'],
            'stable': ['santé', 'beauté', 'sport', 'maison'],
            'declining': ['flash', 'cd', 'dvd', 'fax']
        }
        
        predictions = {}
        for keyword in keywords:
            keyword_lower = keyword.lower()
            
            if any(indicator in keyword_lower for indicator in trend_indicators['rising']):
                predictions[keyword] = 1.2  # +20% de croissance prédite
            elif any(indicator in keyword_lower for indicator in trend_indicators['declining']):
                predictions[keyword] = 0.8  # -20% de déclin prédit
            else:
                predictions[keyword] = 1.0  # Stabilité prédite
        
        return predictions

# Configuration d'optimisation avancée
ADVANCED_OPTIMIZATION_CONFIG = {
    'hyperparameter_tuning': {
        'random_forest': {
            'n_estimators': [100, 200, 300],
            'max_depth': [10, 15, 20, None],
            'min_samples_split': [2, 5, 10],
            'min_samples_leaf': [1, 2, 4]
        },
        'gradient_boosting': {
            'n_estimators': [100, 150, 200],
            'learning_rate': [0.05, 0.1, 0.15],
            'max_depth': [6, 8, 10, 12]
        }
    },
    'feature_engineering': {
        'enable_word_embeddings': True,
        'enable_topic_modeling': True,
        'enable_sentiment_analysis': False,  # Moins pertinent pour le SEO
        'enable_competitor_analysis': True
    },
    'validation': {
        'enable_time_series_split': True,
        'enable_stratified_sampling': True,
        'min_samples_per_class': 10
    }
} 