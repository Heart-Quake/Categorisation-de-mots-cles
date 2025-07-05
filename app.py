import streamlit as st
import pandas as pd
import numpy as np
import re
import unicodedata
from collections import Counter
import base64
from datetime import datetime
import io
import spacy
from sentence_transformers import SentenceTransformer
from sklearn.cluster import HDBSCAN
from sklearn.preprocessing import StandardScaler
import umap
import difflib
from config.advanced_patterns import SEO_SYNONYMS
# 1. Import sécurisé de stqdm
# Suppression de l'import stqdm et de tout fallback associé
# 2. Import de Tuple pour les annotations de type
from typing import Tuple

# Configuration de la page
st.set_page_config(
    page_title="Clustering SEO - Mots-clés", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS pour améliorer l'apparence
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .stProgress .st-bo {
        background-color: #667eea;
    }
    .metric-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #667eea;
    }
</style>
""", unsafe_allow_html=True)

# Initialisation des variables de session
if 'df_original' not in st.session_state:
    st.session_state.df_original = None
if 'df_processed' not in st.session_state:
    st.session_state.df_processed = None
if 'df_clustered' not in st.session_state:
    st.session_state.df_clustered = None
if 'df_final' not in st.session_state:
    st.session_state.df_final = None

@st.cache_resource
def load_models():
    """Charge les modèles nécessaires"""
    try:
        # Modèle de transformation de phrases
        sentence_model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Modèle spaCy pour le français
        try:
            nlp = spacy.load("fr_core_news_sm")
        except OSError:
            st.warning("Modèle spaCy français non trouvé. Utilisation du modèle anglais.")
            nlp = spacy.load("en_core_web_sm")
        
        return sentence_model, nlp
    except Exception as e:
        st.error(f"Erreur lors du chargement des modèles : {e}")
        return None, None

def normalize_keyword(keyword: str) -> str:
    """Normalise un mot-clé en supprimant les caractères unicode et en lemmatisant"""
    if pd.isna(keyword):
        return ""
    
    # Conversion en string et nettoyage de base
    keyword = str(keyword).strip().lower()
    
    # Suppression des caractères unicode et normalisation
    keyword = unicodedata.normalize('NFKD', keyword)
    keyword = ''.join(char for char in keyword if unicodedata.category(char) != 'Mn')
    
    # Suppression des caractères spéciaux et symboles
    keyword = re.sub(r'[^\w\s-]', ' ', keyword)
    
    # Nettoyage des espaces multiples
    keyword = re.sub(r'\s+', ' ', keyword).strip()
    
    return keyword

def clean_question_prefix(keyword: str) -> str:
    """
    Préserve les locutions interrogatives et nettoie les tirets/apostrophes.
    """
    if not isinstance(keyword, str):
        return keyword
    # Liste des locutions à préserver
    question_patterns = [
        r"^est-ce que", r"^est-ce", r"^qu'est-ce que", r"^c'est", r"^y a-t-il", r"^peut-on", r"^comment", r"^pourquoi", r"^où", r"^quand", r"^qui", r"^quel", r"^quelle", r"^quels", r"^quelles"
    ]
    for pattern in question_patterns:
        if re.match(pattern, keyword):
            # On ne touche pas à la locution interrogative
            return keyword.replace("’", "'")
    # Nettoyer les tirets isolés
    keyword = re.sub(r"(^| )-+", " ", keyword)
    # Nettoyer les apostrophes mal placées
    keyword = re.sub(r"’", "'", keyword)
    keyword = re.sub(r" +", " ", keyword)
    return keyword.strip()

def lemmatize_keyword(keyword: str, nlp) -> str:
    """
    Lemmatisation avancée qui préserve les locutions interrogatives et nettoie les tirets.
    """
    if not keyword or nlp is None:
        return keyword
    keyword = clean_question_prefix(keyword)
    # Liste des mots-outils à conserver (déterminants, pronoms, particules interrogatives)
    mots_essentiels = {
        "le", "la", "les", "un", "une", "des", "du", "de", "au", "aux", "ce", "cette", "ces", "son", "sa", "ses", "mon", "ma", "mes", "notre", "votre", "leur", "leurs", "est-ce", "est-ce que", "qu'est-ce que", "c'est", "y a-t-il", "peut-on", "comment", "pourquoi", "où", "quand", "qui", "quel", "quelle", "quels", "quelles"
    }
    try:
        doc = nlp(keyword)
        lemmatized = ' '.join([
            token.lemma_ if (token.text.lower() in mots_essentiels or token.lemma_ in mots_essentiels)
            else token.lemma_ for token in doc if not token.is_punct and (token.text.strip() != "-")
        ])
        return lemmatized if lemmatized else keyword
    except Exception:
        return keyword

def detect_search_intent(keyword: str) -> str:
    """Détecte l'intention de recherche du mot-clé avec logique affinée et stricte pour 'Locale'"""
    keyword_lower = keyword.lower().strip()
    words = set(keyword_lower.split())

    # Chargement des entités géographiques françaises
    try:
        from config.geo_data import FRENCH_CITIES, FRENCH_DEPARTMENTS, FRENCH_REGIONS
    except ImportError:
        FRENCH_CITIES, FRENCH_DEPARTMENTS, FRENCH_REGIONS = set(), set(), set()

    # === LOCALE : Détection stricte d'une entité géographique ===
    for city in FRENCH_CITIES:
        if city in keyword_lower:
            return "Locale"
    for dep in FRENCH_DEPARTMENTS:
        if dep in keyword_lower:
            return "Locale"
    for region in FRENCH_REGIONS:
        if region in keyword_lower:
            return "Locale"

    # === DÉCOUVERTE : Requêtes génériques, peu précises, en amont du parcours ===
    decouverte_patterns = [
        "qu'est-ce que", "c'est quoi", "comment", "pourquoi", "définition", "apprendre", "comprendre", "découvrir", "connaître", "guide", "tutoriel", "introduction", "tout savoir", "univers", "catégorie", "type", "liste", "panorama", "variété"
    ]
    for pattern in decouverte_patterns:
        if pattern in keyword_lower:
            return "Découverte"
    
    # === AUTRES INTENTIONS (temporaire - à affiner dans les prochaines étapes) ===
    consideration_patterns = [
        'meilleur', 'comparaison', 'vs', 'versus', 'avis', 'test', 'review',
        'avantage', 'inconvenient', 'difference', 'choisir', 'selection'
    ]
    
    transaction_patterns = [
        'acheter', 'achat', 'prix', 'tarif', 'cout', 'promotion', 'reduction',
        'pas cher', 'gratuit', 'livraison', 'commande', 'boutique', 'magasin'
    ]
    
    # Vérification des autres patterns (ordre important)
    for pattern in transaction_patterns:
        if pattern in keyword_lower:
            return 'Transaction'
    
    for pattern in consideration_patterns:
        if pattern in keyword_lower:
            return 'Considération'
    
    # Par défaut : Informationnel
    return 'Informationnel'

def normalize_advanced(keyword: str, synonyms_dict: dict, enable_correction: bool = True) -> Tuple[str, str]:
    """
    Applique une correction orthographique légère et un mapping de synonymes SEO.
    Retourne (forme canonique, justification/correction appliquée).
    """
    if not keyword:
        return "", ""
    keyword_clean = keyword.strip().lower()
    # 1. Mapping direct (variante -> canonique)
    for canonical, variants in synonyms_dict.items():
        if keyword_clean == canonical:
            return canonical, "canonique"
        if keyword_clean in variants:
            return canonical, f"synonyme de '{canonical}'"
    # 2. Correction orthographique légère (si activée)
    if enable_correction:
        all_forms = list(synonyms_dict.keys()) + [v for variants in synonyms_dict.values() for v in variants]
        match = difflib.get_close_matches(keyword_clean, all_forms, n=1, cutoff=0.88)
        if match:
            # Trouver la forme canonique associée
            for canonical, variants in synonyms_dict.items():
                if match[0] == canonical or match[0] in variants:
                    return canonical, f"correction vers '{canonical}' (proche de '{match[0]}')"
    # 3. Pas de correspondance
    return keyword, "aucune correction"

def load_csv_file(uploaded_file):
    """Charge et valide le fichier CSV"""
    try:
        # Lecture du fichier avec différents encodages
        encodings = ['utf-8', 'latin-1', 'cp1252']
        separators = [',', ';', '\t']
        
        df = None
        for encoding in encodings:
            for sep in separators:
                try:
                    uploaded_file.seek(0)
                    df = pd.read_csv(uploaded_file, encoding=encoding, sep=sep)
                    if len(df.columns) >= 2:
                        break
                except:
                    continue
            if df is not None and len(df.columns) >= 2:
                break
        
        if df is None:
            st.error("Impossible de lire le fichier. Vérifiez le format.")
            return None
        
        # Validation des colonnes requises
        columns = df.columns.tolist()
        
        # Recherche des colonnes Keyword et Volume
        keyword_col = None
        volume_col = None
        
        for col in columns:
            col_lower = col.lower()
            if 'keyword' in col_lower or 'mot' in col_lower or 'requete' in col_lower:
                keyword_col = col
            elif 'volume' in col_lower or 'recherche' in col_lower or 'trafic' in col_lower:
                volume_col = col
        
        if keyword_col is None:
            st.error("Colonne 'Keyword' non trouvée. Vérifiez que votre fichier contient une colonne avec les mots-clés.")
            return None
        
        # Renommage des colonnes
        df = df.rename(columns={keyword_col: 'Keyword'})
        if volume_col:
            df = df.rename(columns={volume_col: 'Volume'})
        else:
            df['Volume'] = 0
        
        # Nettoyage des données
        df = df.dropna(subset=['Keyword'])
        df['Keyword'] = df['Keyword'].astype(str)
        df['Volume'] = pd.to_numeric(df['Volume'], errors='coerce').fillna(0)
        
        st.success(f"✅ Fichier chargé avec succès : {len(df)} mots-clés")
        return df[['Keyword', 'Volume']]
        
    except Exception as e:
        st.error(f"Erreur lors du chargement : {e}")
        return None

def process_keywords(df, nlp, enable_synonyms=True, enable_correction=True):
    """Traite les mots-clés : normalisation, lemmatisation, synonymes, correction et déduplication"""
    if df is None or df.empty:
        return None, None
    progress_bar = st.progress(0)
    status_text = st.empty()
    # Étape 1: Normalisation
    status_text.text("🔄 Normalisation des mots-clés...")
    progress_bar.progress(20)
    df_processed = df.copy()
    df_processed['Keyword_Normalized'] = df_processed['Keyword'].apply(normalize_keyword)
    # Étape 2: Lemmatisation
    status_text.text("🔄 Lemmatisation des mots-clés...")
    progress_bar.progress(40)
    df_processed['Keyword_Lemmatized'] = df_processed['Keyword_Normalized'].apply(
        lambda x: lemmatize_keyword(x, nlp)
    )
    # Étape 3: Synonymes & Correction
    if enable_synonyms:
        status_text.text("🔄 Correction orthographique et mapping synonymes...")
        progress_bar.progress(60)
        results = df_processed['Keyword_Lemmatized'].apply(
            lambda x: normalize_advanced(x, SEO_SYNONYMS, enable_correction)
        )
        df_processed['Keyword_Canonical'] = results.apply(lambda x: x[0])
        df_processed['Correction_Info'] = results.apply(lambda x: x[1])
    else:
        df_processed['Keyword_Canonical'] = df_processed['Keyword_Lemmatized']
        df_processed['Correction_Info'] = "aucune correction"
    # Étape 4: Déduplication (garder le volume le plus élevé)
    status_text.text("🔄 Suppression des doublons...")
    progress_bar.progress(80)
    df_deduplicated = df_processed.loc[
        df_processed.groupby('Keyword_Canonical')['Volume'].idxmax()
    ].reset_index(drop=True)
    # Étape 5: Détection des intentions
    status_text.text("🔄 Détection des intentions de recherche...")
    progress_bar.progress(95)
    df_deduplicated['Search_Intent'] = df_deduplicated['Keyword'].apply(detect_search_intent)
    progress_bar.progress(100)
    status_text.text("✅ Traitement terminé !")
    # Aperçu des corrections appliquées
    corrections_applied = df_processed[df_processed['Correction_Info'] != 'aucune correction'][['Keyword', 'Keyword_Canonical', 'Correction_Info']]
    return df_deduplicated, corrections_applied

def create_clusters(df, sentence_model):
    """Crée les clusters de mots-clés"""
    if df is None or df.empty:
        return None
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    # Étape 1: Vectorisation
    status_text.text("🔄 Vectorisation des mots-clés...")
    progress_bar.progress(25)
    
    keywords = df['Keyword_Lemmatized'].tolist()
    embeddings = sentence_model.encode(keywords, show_progress_bar=False)
    
    # Étape 2: Réduction de dimensionnalité
    status_text.text("🔄 Réduction de dimensionnalité...")
    progress_bar.progress(50)
    
    umap_model = umap.UMAP(
        n_neighbors=15,
        n_components=5,
        min_dist=0.0,
        metric='cosine',
        random_state=42
    )
    umap_embeddings = umap_model.fit_transform(embeddings)
    
    # Étape 3: Clustering
    status_text.text("🔄 Création des clusters...")
    progress_bar.progress(75)
    
    hdbscan_model = HDBSCAN(
        min_cluster_size=max(2, len(df) // 20),
        metric='euclidean',
        cluster_selection_method='eom'
    )
    cluster_labels = hdbscan_model.fit_predict(umap_embeddings)
    
    # Étape 4: Génération des labels de clusters
    status_text.text("🔄 Génération des labels de clusters...")
    progress_bar.progress(90)
    
    df_clustered = df.copy()
    df_clustered['Cluster_ID'] = cluster_labels
    
    # Génération des labels de clusters
    cluster_labels_dict = {}
    for cluster_id in set(cluster_labels):
        if cluster_id == -1:
            cluster_labels_dict[cluster_id] = "Divers"
        else:
            # Prendre les mots les plus fréquents du cluster
            cluster_keywords = df_clustered[df_clustered['Cluster_ID'] == cluster_id]['Keyword_Lemmatized']
            
            # Compter les mots
            all_words = []
            for keyword in cluster_keywords:
                all_words.extend(keyword.split())
            
            word_counts = Counter(all_words)
            top_words = [word for word, count in word_counts.most_common(3) if len(word) > 2]
            
            if top_words:
                cluster_labels_dict[cluster_id] = f"Cluster {cluster_id + 1}: {' + '.join(top_words[:2])}"
            else:
                cluster_labels_dict[cluster_id] = f"Cluster {cluster_id + 1}"
    
    df_clustered['Cluster_Label'] = df_clustered['Cluster_ID'].map(cluster_labels_dict)
    
    progress_bar.progress(100)
    status_text.text("✅ Clustering terminé !")
    
    return df_clustered

def create_export_file(df, format_type):
    """Crée le fichier d'export"""
    if df is None or df.empty:
        return None
    
    # Préparation des données pour l'export
    export_df = df[['Keyword', 'Volume', 'Cluster_ID', 'Cluster_Label', 'Search_Intent']].copy()
    export_df = export_df.rename(columns={
        'Keyword': 'Mot-clé',
        'Volume': 'Volume de recherche',
        'Cluster_ID': 'ID Cluster',
        'Cluster_Label': 'Label Cluster',
        'Search_Intent': 'Intention de recherche'
    })
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    if format_type == "CSV":
        csv_data = export_df.to_csv(index=False, encoding='utf-8')
        b64 = base64.b64encode(csv_data.encode()).decode()
        filename = f"clustering_mots_cles_{timestamp}.csv"
        href = f'<a href="data:file/csv;base64,{b64}" download="{filename}" class="download-link">📥 Télécharger CSV</a>'
        return href
    
    elif format_type == "Excel":
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            # Feuille principale
            export_df.to_excel(writer, sheet_name='Mots-clés clustérisés', index=False)
            
            # Feuille de synthèse
            summary_df = df.groupby(['Cluster_Label', 'Search_Intent']).agg({
                'Keyword': 'count',
                'Volume': 'sum'
            }).reset_index()
            summary_df.columns = ['Cluster', 'Intention', 'Nb mots-clés', 'Volume total']
            summary_df.to_excel(writer, sheet_name='Synthèse', index=False)
        
        output.seek(0)
        b64 = base64.b64encode(output.read()).decode()
        filename = f"clustering_mots_cles_{timestamp}.xlsx"
        href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="{filename}" class="download-link">📥 Télécharger Excel</a>'
        return href
    
    return None

# === INTERFACE SIMPLIFIÉE POUR CONSULTANT SEO ===
st.sidebar.title("Outil de regroupement de mots-clés SEO")
st.sidebar.markdown("""
**Étapes :**
1. Importez votre fichier de mots-clés (CSV/Excel)
2. Cliquez sur "Lancer l'analyse"
3. Explorez et exportez vos groupes de mots-clés
""")

# --- Bouton principal ---
# SUPPRIMÉ : if st.sidebar.button("🚀 Lancer l'analyse", help="Cliquez ici pour regrouper automatiquement vos mots-clés par sens et volume."):
# SUPPRIMÉ :     st.session_state['run_analysis'] = True

# === CORRECTION : Paramètres avancés UNIQUEMENT dans l'expander ===
# Supprimer tout slider/select/titre HDBSCAN, UMAP, dédoublonnage hors du bloc ci-dessous :
with st.sidebar.expander('⚙️ Paramètres avancés (facultatif)', expanded=False):
    st.markdown('''<span style="font-size: 0.95em; color: #888;">Les options ci-dessous sont réservées aux utilisateurs avancés. Pour un usage standard, laissez les valeurs par défaut.</span>''', unsafe_allow_html=True)
    # --- Section HDBSCAN ---
    st.markdown("### 🧩 Clustering HDBSCAN")
    min_cluster_size = st.slider(
        "Taille minimale d’un cluster",
        min_value=2, max_value=50, value=8,
        help="Nombre minimal de mots-clés pour former un cluster. Plus la valeur est élevée, plus les groupes sont gros et stables."
    )
    min_samples = st.slider(
        "Min. samples (robustesse)",
        min_value=1, max_value=20, value=1,
        help="Robustesse du regroupement. Laisser à 1 pour la plupart des cas."
    )
    metric_hdbscan = st.selectbox(
        "Métrique de distance (HDBSCAN)",
        ["euclidean", "manhattan", "cosine"],
        index=0,
        help="Type de calcul de distance pour regrouper les mots-clés."
    )
    # --- Section UMAP ---
    st.markdown("### 🗺️ Réduction de dimension UMAP")
    n_neighbors = st.slider(
        "Voisinage local (n_neighbors)",
        min_value=5, max_value=100, value=15,
        help="Nombre de voisins pris en compte pour la réduction de dimension."
    )
    min_dist = st.slider(
        "Distance minimale (min_dist)",
        min_value=0.0, max_value=0.99, value=0.1, step=0.01,
        help="Plus la valeur est basse, plus les groupes sont compacts."
    )
    metric_umap = st.selectbox(
        "Métrique de distance (UMAP)",
        ["euclidean", "manhattan", "cosine"],
        index=2,
        help="Type de calcul de distance pour la projection visuelle."
    )
    # --- Section dédoublonnage ---
    st.markdown("### 🔄 Dédoublonnage sémantique")
    seuil_cosine = st.slider(
        "Seuil de similarité cosine (fusion sémantique)",
        min_value=0.80, max_value=0.99, value=0.90, step=0.01,
        help="Plus la valeur est basse, plus la fusion de mots-clés proches est agressive."
    )
    seuil_lev = st.slider(
        "Seuil de ratio Levenshtein (fusion lexicale)",
        min_value=0.70, max_value=1.00, value=0.85, step=0.01,
        help="Plus la valeur est basse, plus la fusion de variantes orthographiques est agressive."
    )
# === FIN CORRECTION : NE PAS DÉCLARER DE PARAMÈTRES AVANCÉS HORS DE CE BLOC ===

# --- Page principale ---
st.title("Clustering SEO simplifié")
st.markdown("""
Cet outil regroupe automatiquement vos mots-clés par sens et volume de recherche. Idéal pour préparer un audit, une stratégie de contenu ou un plan de clustering sémantique.

- **Importez** votre liste de mots-clés
- **Lancez l'analyse**
- **Explorez** les groupes et exportez le résultat

*Paramètres avancés disponibles dans la barre latérale.*
""")

# Chargement des modèles
with st.spinner("🔄 Chargement des modèles..."):
    sentence_model, nlp = load_models()

if sentence_model is None or nlp is None:
    st.error("Impossible de charger les modèles. Vérifiez votre installation.")

# Sidebar pour les étapes
st.sidebar.header("📋 Étapes du processus")

# === PARAMÈTRES INTERFACE STREAMLIT ===
# SUPPRESSION de tout doublon :
# - Enlever tout st.markdown('Paramètres avancés'), st.header('Paramètres avancés'), st.markdown('Options avancées'), etc. en dehors de l'expander
# - Ne garder que le bloc expander '⚙️ Paramètres avancés (facultatif)' en bas de la sidebar

# --- Section HDBSCAN ---
# SUPPRIMÉ : st.sidebar.markdown("### 🧩 Clustering HDBSCAN")
# SUPPRIMÉ : min_cluster_size = st.sidebar.slider(...)
# SUPPRIMÉ : min_samples = st.sidebar.slider(...)
# SUPPRIMÉ : hdbscan_metric = st.sidebar.selectbox(...)

# --- Section UMAP ---
# SUPPRIMÉ : st.sidebar.markdown("### 🗺️ Réduction de dimension UMAP")
# SUPPRIMÉ : n_neighbors = st.sidebar.slider(...)
# SUPPRIMÉ : min_dist = st.sidebar.slider(...)
# SUPPRIMÉ : umap_metric = st.sidebar.selectbox(...)

# --- Section Dédoublonnage sémantique ---
# SUPPRIMÉ : st.sidebar.markdown("### 🔄 Dédoublonnage sémantique")
# SUPPRIMÉ : cosine_threshold = st.sidebar.slider(...)
# SUPPRIMÉ : levenshtein_threshold = st.sidebar.slider(...)
    
# Étape 1: Import des données
st.sidebar.subheader("1️⃣ Import des données")
uploaded_file = st.sidebar.file_uploader(
    "Choisir un fichier CSV",
    type=['csv'],
    help="Le fichier doit contenir au minimum une colonne 'Keyword' et optionnellement une colonne 'Volume'"
)
    
if uploaded_file is not None:
    if st.session_state.df_original is None:
        st.session_state.df_original = load_csv_file(uploaded_file)
    
# Affichage des données importées
if st.session_state.df_original is not None:
    st.subheader("📊 Données importées")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Nombre de mots-clés", len(st.session_state.df_original))
    with col2:
        st.metric("Volume total", f"{st.session_state.df_original['Volume'].sum():,}")
    with col3:
        st.metric("Volume moyen", f"{st.session_state.df_original['Volume'].mean():.0f}")
    
    # Slider pour contrôler le nombre de lignes à afficher
    n_rows_original = st.slider("Nombre de lignes à afficher (données originales)", 
                               min_value=10, max_value=min(100, len(st.session_state.df_original)), 
                               value=min(50, len(st.session_state.df_original)), step=10)
    
    st.dataframe(st.session_state.df_original.head(n_rows_original), use_container_width=True)
    
    # Étape 2: Traitement des données
    st.sidebar.subheader("2️⃣ Traitement des données")
    enable_synonyms = st.sidebar.checkbox("Activer la correction orthographique et les synonymes", value=True)
    if st.sidebar.button("🚀 Lancer le traitement", type="primary"):
        with st.spinner("Traitement en cours..."):
            result = process_keywords(st.session_state.df_original, nlp, enable_synonyms=enable_synonyms, enable_correction=enable_synonyms)
            if result is not None:
                st.session_state.df_processed, st.session_state.corrections_applied = result
    
    # Affichage des données traitées
    if st.session_state.df_processed is not None:
        st.subheader("🔧 Données traitées")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            original_count = len(st.session_state.df_original)
            processed_count = len(st.session_state.df_processed)
            st.metric("Mots-clés après déduplication", processed_count, 
                     delta=processed_count - original_count)
        with col2:
            intent_counts = st.session_state.df_processed['Search_Intent'].value_counts()
            st.metric("Intentions détectées", len(intent_counts))
        with col3:
            st.metric("Volume conservé", f"{st.session_state.df_processed['Volume'].sum():,}")
        
        # Répartition des intentions
        st.subheader("📈 Répartition des intentions de recherche")
        
        col1, col2 = st.columns(2)
        
        with col1:
            intent_df = st.session_state.df_processed['Search_Intent'].value_counts().reset_index()
            intent_df.columns = ['Intention', 'Nombre']
            st.bar_chart(intent_df.set_index('Intention'))
        
        with col2:
            st.write("**Détail par intention :**")
            for intent in intent_df['Intention']:
                count = intent_df[intent_df['Intention'] == intent]['Nombre'].iloc[0]
                percentage = (count / len(st.session_state.df_processed)) * 100
                st.write(f"• **{intent}** : {count} mots-clés ({percentage:.1f}%)")
        
        # Slider pour les données traitées
        n_rows_processed = st.slider("Nombre de lignes à afficher (données traitées)", 
                                   min_value=10, max_value=min(100, len(st.session_state.df_processed)), 
                                   value=min(50, len(st.session_state.df_processed)), step=10)
        
        # Affichage des données traitées avec plus de colonnes
        display_cols = ['Keyword', 'Volume', 'Keyword_Normalized', 'Keyword_Lemmatized', 'Keyword_Canonical', 'Search_Intent']
        available_cols = [col for col in display_cols if col in st.session_state.df_processed.columns]
        
        st.dataframe(st.session_state.df_processed[available_cols].head(n_rows_processed), 
                    use_container_width=True)
        
        # Aperçu des corrections/synonymes appliqués
        if enable_synonyms and hasattr(st.session_state, 'corrections_applied') and st.session_state.corrections_applied is not None and not st.session_state.corrections_applied.empty:
            st.subheader("🔍 Corrections et synonymes appliqués")
            st.dataframe(st.session_state.corrections_applied.head(30), use_container_width=True)
        
        # Étape 3: Clustering
        st.sidebar.subheader("3️⃣ Clustering")
        if st.sidebar.button("🎯 Créer les clusters", type="primary"):
            with st.spinner("Clustering en cours..."):
                st.session_state.df_clustered = create_clusters(st.session_state.df_processed, sentence_model)
                st.session_state.df_final = st.session_state.df_clustered
        
        # Affichage des résultats de clustering
        if st.session_state.df_clustered is not None:
            st.subheader("🎯 Résultats du clustering")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                n_clusters = len(st.session_state.df_clustered['Cluster_ID'].unique())
                st.metric("Nombre de clusters", n_clusters)
            with col2:
                noise_count = len(st.session_state.df_clustered[st.session_state.df_clustered['Cluster_ID'] == -1])
                st.metric("Mots-clés non classés", noise_count)
            with col3:
                avg_cluster_size = st.session_state.df_clustered[st.session_state.df_clustered['Cluster_ID'] != -1].groupby('Cluster_ID').size().mean()
                st.metric("Taille moyenne des clusters", f"{avg_cluster_size:.1f}")
            
            # Distribution des clusters
            st.subheader("📊 Distribution des clusters")
            
            col1, col2 = st.columns(2)
            
            with col1:
                cluster_counts = st.session_state.df_clustered['Cluster_Label'].value_counts().head(10)
                st.bar_chart(cluster_counts)
            
            with col2:
                st.write("**Top 10 des clusters :**")
                for i, (cluster, count) in enumerate(cluster_counts.head(10).items(), 1):
                    percentage = (count / len(st.session_state.df_clustered)) * 100
                    st.write(f"{i}. **{cluster}** : {count} mots-clés ({percentage:.1f}%)")
            
            # Tableau des résultats
            st.subheader("📋 Tableau des résultats")
            
            # Slider pour les résultats de clustering
            n_rows_clustered = st.slider("Nombre de lignes à afficher (résultats clustering)", 
                                       min_value=10, max_value=min(100, len(st.session_state.df_clustered)), 
                                       value=min(50, len(st.session_state.df_clustered)), step=10)
            
            # Affichage des résultats avec toutes les colonnes importantes
            display_cols = ['Keyword', 'Volume', 'Cluster_ID', 'Cluster_Label', 'Search_Intent', 'Keyword_Normalized', 'Keyword_Lemmatized']
            available_cols = [col for col in display_cols if col in st.session_state.df_clustered.columns]
            
            display_df = st.session_state.df_clustered[available_cols].head(n_rows_clustered)
            st.dataframe(display_df, use_container_width=True)
            
            # Étape 4: Export
            st.sidebar.subheader("4️⃣ Export")
            export_format = st.sidebar.selectbox("Format d'export", ["CSV", "Excel"])
            
            if st.sidebar.button("📥 Générer l'export", type="primary"):
                download_link = create_export_file(st.session_state.df_final, export_format)
                if download_link:
                    st.sidebar.markdown(download_link, unsafe_allow_html=True)
                    st.sidebar.success("✅ Export généré !")

if __name__ == "__main__":
    # main()  # Décommente si la fonction main() existe
    pass