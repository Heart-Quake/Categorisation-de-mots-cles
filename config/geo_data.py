# Module de données géographiques françaises pour la détection d'intentions locales
# Données géographiques complètes de la France

import json
import requests
from typing import Set, List, Dict
import logging

class FrenchGeoData:
    """Classe pour gérer les données géographiques françaises"""
    
    def __init__(self):
        self.regions = set()
        self.departements = set()
        self.communes = set()
        self.villes_principales = set()
        self.loaded = False
        
    def load_data(self):
        """Charge toutes les données géographiques"""
        if self.loaded:
            return
            
        try:
            # Chargement des données locales d'abord
            self._load_static_data()
            
            # Tentative de chargement des données API (optionnel)
            try:
                self._load_api_data()
            except Exception as e:
                logging.warning(f"Impossible de charger les données API: {e}")
                
            self.loaded = True
            logging.info(f"Données géographiques chargées: {len(self.communes)} communes, {len(self.departements)} départements, {len(self.regions)} régions")
            
        except Exception as e:
            logging.error(f"Erreur lors du chargement des données géographiques: {e}")
            
    def _load_static_data(self):
        """Charge les données géographiques statiques essentielles"""
        
        # Régions françaises (13 régions métropolitaines + 5 DROM)
        self.regions.update([
            'auvergne-rhône-alpes', 'auvergne rhône alpes', 'auvergne', 'rhône-alpes', 'rhone alpes',
            'bourgogne-franche-comté', 'bourgogne franche comte', 'bourgogne', 'franche-comté', 'franche comte',
            'bretagne',
            'centre-val de loire', 'centre val de loire', 'centre', 'val de loire',
            'corse', 'corse-du-sud', 'haute-corse',
            'grand est', 'grand-est', 'alsace', 'champagne-ardenne', 'lorraine',
            'hauts-de-france', 'hauts de france', 'nord-pas-de-calais', 'picardie',
            'île-de-france', 'ile de france', 'idf', 'région parisienne',
            'normandie', 'basse-normandie', 'haute-normandie',
            'nouvelle-aquitaine', 'nouvelle aquitaine', 'aquitaine', 'limousin', 'poitou-charentes',
            'occitanie', 'languedoc-roussillon', 'midi-pyrénées', 'midi pyrenees',
            'pays de la loire', 'pays-de-la-loire',
            'provence-alpes-côte d\'azur', 'provence alpes cote d azur', 'paca', 'provence', 'côte d\'azur', 'cote d azur',
            # DROM
            'guadeloupe', 'martinique', 'guyane', 'guyane française', 'la réunion', 'reunion', 'mayotte'
        ])
        
        # Départements (codes et noms)
        departements_data = {
            '01': 'ain', '02': 'aisne', '03': 'allier', '04': 'alpes-de-haute-provence', '05': 'hautes-alpes',
            '06': 'alpes-maritimes', '07': 'ardèche', '08': 'ardennes', '09': 'ariège', '10': 'aube',
            '11': 'aude', '12': 'aveyron', '13': 'bouches-du-rhône', '14': 'calvados', '15': 'cantal',
            '16': 'charente', '17': 'charente-maritime', '18': 'cher', '19': 'corrèze', '2A': 'corse-du-sud',
            '2B': 'haute-corse', '21': 'côte-d\'or', '22': 'côtes-d\'armor', '23': 'creuse', '24': 'dordogne',
            '25': 'doubs', '26': 'drôme', '27': 'eure', '28': 'eure-et-loir', '29': 'finistère',
            '30': 'gard', '31': 'haute-garonne', '32': 'gers', '33': 'gironde', '34': 'hérault',
            '35': 'ille-et-vilaine', '36': 'indre', '37': 'indre-et-loire', '38': 'isère', '39': 'jura',
            '40': 'landes', '41': 'loir-et-cher', '42': 'loire', '43': 'haute-loire', '44': 'loire-atlantique',
            '45': 'loiret', '46': 'lot', '47': 'lot-et-garonne', '48': 'lozère', '49': 'maine-et-loire',
            '50': 'manche', '51': 'marne', '52': 'haute-marne', '53': 'mayenne', '54': 'meurthe-et-moselle',
            '55': 'meuse', '56': 'morbihan', '57': 'moselle', '58': 'nièvre', '59': 'nord',
            '60': 'oise', '61': 'orne', '62': 'pas-de-calais', '63': 'puy-de-dôme', '64': 'pyrénées-atlantiques',
            '65': 'hautes-pyrénées', '66': 'pyrénées-orientales', '67': 'bas-rhin', '68': 'haut-rhin', '69': 'rhône',
            '70': 'haute-saône', '71': 'saône-et-loire', '72': 'sarthe', '73': 'savoie', '74': 'haute-savoie',
            '75': 'paris', '76': 'seine-maritime', '77': 'seine-et-marne', '78': 'yvelines', '79': 'deux-sèvres',
            '80': 'somme', '81': 'tarn', '82': 'tarn-et-garonne', '83': 'var', '84': 'vaucluse',
            '85': 'vendée', '86': 'vienne', '87': 'haute-vienne', '88': 'vosges', '89': 'yonne',
            '90': 'territoire de belfort', '91': 'essonne', '92': 'hauts-de-seine', '93': 'seine-saint-denis',
            '94': 'val-de-marne', '95': 'val-d\'oise',
            # DROM
            '971': 'guadeloupe', '972': 'martinique', '973': 'guyane', '974': 'la réunion', '976': 'mayotte'
        }
        
        # Ajouter les départements avec leurs variantes
        for code, nom in departements_data.items():
            self.departements.add(nom)
            self.departements.add(nom.replace('-', ' '))
            self.departements.add(nom.replace('\'', ' '))
            
        # Villes principales (préfectures + grandes villes)
        self.villes_principales.update([
            # Préfectures et grandes métropoles
            'paris', 'marseille', 'lyon', 'toulouse', 'nice', 'nantes', 'montpellier', 'strasbourg',
            'bordeaux', 'lille', 'rennes', 'reims', 'saint-étienne', 'toulon', 'grenoble', 'dijon',
            'angers', 'nîmes', 'villeurbanne', 'clermont-ferrand', 'aix-en-provence', 'brest',
            'limoges', 'tours', 'amiens', 'perpignan', 'metz', 'besançon', 'orléans', 'mulhouse',
            'rouen', 'caen', 'nancy', 'argenteuil', 'montreuil', 'roubaix', 'tourcoing', 'nanterre',
            'avignon', 'créteil', 'dunkerque', 'poitiers', 'asnieres-sur-seine', 'courbevoie',
            'versailles', 'colombes', 'fort-de-france', 'aulnay-sous-bois', 'saint-paul', 'aubervilliers',
            'calais', 'saint-pierre', 'antibes', 'boulogne-billancourt', 'cannes', 'le mans',
            # Préfectures
            'ajaccio', 'bastia', 'châlons-en-champagne', 'charleville-mézières', 'épinal', 'mâcon',
            'melun', 'châteauroux', 'chartres', 'évreux', 'blois', 'laval', 'alençon', 'beauvais',
            'arras', 'amiens', 'cahors', 'agen', 'mende', 'privas', 'foix', 'carcassonne',
            'rodez', 'aurillac', 'tulle', 'guéret', 'périgueux', 'valence', 'gap', 'digne-les-bains',
            'auch', 'mont-de-marsan', 'tarbes', 'lons-le-saunier', 'bourg-en-bresse', 'le puy-en-velay',
            'saint-brieuc', 'vannes', 'quimper', 'annecy', 'chambéry', 'chaumont', 'vesoul',
            'bar-le-duc', 'verdun', 'nevers', 'auxerre', 'troyes', 'belfort', 'évry', 'bobigny',
            'pontoise', 'créteil', 'nanterre', 'versailles'
        ])
        
    def _load_api_data(self):
        """Charge des données supplémentaires via API (optionnel)"""
        try:
            # API geo.api.gouv.fr pour les communes
            response = requests.get("https://geo.api.gouv.fr/communes?fields=nom&format=json", timeout=10)
            if response.status_code == 200:
                communes_data = response.json()
                for commune in communes_data:
                    nom = commune.get('nom', '').lower()
                    if nom:
                        self.communes.add(nom)
                        # Ajouter variantes sans accents et tirets
                        nom_clean = nom.replace('-', ' ').replace('\'', ' ')
                        self.communes.add(nom_clean)
        except Exception as e:
            logging.warning(f"Impossible de charger les communes via API: {e}")
            
    def get_all_locations(self) -> Set[str]:
        """Retourne toutes les localisations (régions, départements, villes)"""
        if not self.loaded:
            self.load_data()
        return self.regions | self.departements | self.villes_principales | self.communes
        
    def is_location(self, word: str) -> bool:
        """Vérifie si un mot est une localisation française"""
        if not self.loaded:
            self.load_data()
        word_lower = word.lower().strip()
        return word_lower in self.get_all_locations()
        
    def get_location_type(self, word: str) -> str:
        """Retourne le type de localisation (région, département, ville, commune)"""
        if not self.loaded:
            self.load_data()
        word_lower = word.lower().strip()
        
        if word_lower in self.regions:
            return "région"
        elif word_lower in self.departements:
            return "département"
        elif word_lower in self.villes_principales:
            return "ville"
        elif word_lower in self.communes:
            return "commune"
        else:
            return "inconnu"

# Instance globale
french_geo = FrenchGeoData()

# Fonction utilitaire pour l'import
def get_french_locations() -> Set[str]:
    """Retourne toutes les localisations françaises"""
    return french_geo.get_all_locations()

def is_french_location(word: str) -> bool:
    """Vérifie si un mot est une localisation française"""
    return french_geo.is_location(word) 