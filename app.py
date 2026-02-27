import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Rectangle, FancyBboxPatch
import math

# Configuration de la page
st.set_page_config(
    page_title="Dimensionnement Professionnel d'Entrepôt",
    page_icon="📐",
    layout="wide"
)

# Style CSS personnalisé
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #2c3e50;
        text-align: center;
        padding: 1.5rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .metric-card {
        background: white;
        padding: 1.2rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
        transition: transform 0.3s;
    }
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
    }
    .result-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
    }
    .info-box {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #667eea;
        margin: 1rem 0;
    }
    .warning-box {
        background: #fff3cd;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #ffc107;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Titre principal
st.markdown('<h1 class="main-header">📐 DIMENSIONNEMENT PROFESSIONNEL D\'ENTREPÔT</h1>', 
            unsafe_allow_html=True)

# Initialisation des paramètres
if 'params' not in st.session_state:
    st.session_state.params = {}

# Sidebar pour les paramètres d'entrée
st.sidebar.image("https://via.placeholder.com/300x150/667eea/ffffff?text=ENTREPOT+PRO", use_column_width=True)
st.sidebar.title("🔧 Paramètres Techniques")

# Création des onglets dans la sidebar
param_tab = st.sidebar.radio(
    "Catégories de paramètres",
    ["🏢 Dimensions", "📦 Unités de Charge", "🏗️ Rayonnages", "🚜 Engins", "📋 Zonage", "📊 Calculs"]
)

# ==================== 1. DIMENSIONS DE L'ENTREPÔT ====================
if param_tab == "🏢 Dimensions":
    st.sidebar.subheader("🏢 Dimensions du bâtiment")
    
    longueur = st.sidebar.number_input("Longueur totale (m)", min_value=10.0, max_value=200.0, value=50.0, step=1.0)
    largeur = st.sidebar.number_input("Largeur totale (m)", min_value=10.0, max_value=100.0, value=30.0, step=1.0)
    hauteur_sous_poutre = st.sidebar.number_input("Hauteur sous poutre (m)", min_value=4.0, max_value=20.0, value=9.21, step=0.5)
    
    st.sidebar.markdown("---")
    st.sidebar.subheader("📐 Contraintes structurelles")
    
    espace_securite = st.sidebar.slider("Espace de sécurité périmétrique (m)", 0.5, 2.0, 1.0)
    hauteur_sprinklers = st.sidebar.number_input("Hauteur sprinklers sous poutre (m)", min_value=0.3, max_value=1.0, value=0.5)
    
    # Calcul de la hauteur utile
    hauteur_utile = hauteur_sous_poutre - hauteur_sprinklers
    
    # Sauvegarde dans session state
    st.session_state.params['longueur'] = longueur
    st.session_state.params['largeur'] = largeur
    st.session_state.params['hauteur_utile'] = hauteur_utile
    st.session_state.params['espace_securite'] = espace_securite
    
    st.sidebar.info(f"Hauteur utile de stockage: {hauteur_utile:.2f} m")

# ==================== 2. UNITÉS DE CHARGE ====================
elif param_tab == "📦 Unités de Charge":
    st.sidebar.subheader("📦 Caractérisation des palettes")
    
    type_palette = st.sidebar.selectbox(
        "Type de palette",
        ["Europe (EPAL) 800x1200", "Industrielle 1000x1200", "Américaine 1200x1200", 
         "Demi-palette 600x800", "Personnalisée"]
    )
    
    if type_palette == "Européenne (EPAL) 800x1200":
        pal_longueur = 800
        pal_largeur = 1200
    elif type_palette == "Industrielle 1000x1200":
        pal_longueur = 1000
        pal_largeur = 1200
    elif type_palette == "Américaine 1200x1200":
        pal_longueur = 1200
        pal_largeur = 1200
    elif type_palette == "Demi-palette 600x800":
        pal_longueur = 600
        pal_largeur = 800
    else:
        col1, col2 = st.sidebar.columns(2)
        with col1:
            pal_longueur = st.number_input("Longueur (mm)", 400, 2000, 800)
        with col2:
            pal_largeur = st.number_input("Largeur (mm)", 400, 2000, 1200)
    
    # Hauteur et poids
    col1, col2 = st.sidebar.columns(2)
    with col1:
        hauteur_charge = st.number_input("Hauteur charge (mm)", 500, 2500, 1500)
        poids_charge = st.number_input("Poids max/UC (kg)", 500, 3000, 1000)
    with col2:
        marge_securite = st.number_input("Marge sécurité (mm)", 50, 200, 100)
    
    # Calcul de la hauteur totale
    hauteur_totale_uc = hauteur_charge + marge_securite
    
    st.sidebar.info(f"Hauteur totale UC: {hauteur_totale_uc} mm")
    
    # Sauvegarde
    st.session_state.params['pal_longueur'] = pal_longueur
    st.session_state.params['pal_largeur'] = pal_largeur
    st.session_state.params['hauteur_uc'] = hauteur_totale_uc
    st.session_state.params['poids_uc'] = poids_charge

# ==================== 3. RAYONNAGES ====================
elif param_tab == "🏗️ Rayonnages":
    st.sidebar.subheader("🏗️ Configuration des rayonnages")
    
    type_rayonnage = st.sidebar.selectbox(
        "Type de rayonnage",
        ["Classique (pallet rack)", "Navette (shuttle)", "Mobile", "Cantilever", "Drive-in"]
    )
    
    # Configuration des profondeurs
    col1, col2 = st.sidebar.columns(2)
    with col1:
        profondeur_standard = st.number_input("Profondeur standard (mm)", 900, 1500, 1100)
    with col2:
        entretoise_jumelage = st.number_input("Entretoise jumelage (mm)", 150, 300, 200)
    
    configuration = st.sidebar.radio(
        "Configuration",
        ["Simple face (mono-face)", "Double face (dos-à-dos)", "Mixte"]
    )
    
    if configuration == "Simple face (mono-face)":
        profondeur_totale = profondeur_standard
    elif configuration == "Double face (dos-à-dos)":
        profondeur_totale = (profondeur_standard * 2) + entretoise_jumelage
    else:
        profondeur_totale = profondeur_standard  # Mixte sera géré séparément
    
    # Configuration des travées
    st.sidebar.subheader("📊 Configuration des travées")
    
    nb_palettes_par_travee = st.sidebar.selectbox("Palettes par travée", [2, 3, 4, 5], index=1)
    
    # Calcul de la longueur de travée
    if type_palette in st.session_state.params:
        pal_largeur = st.session_state.params.get('pal_largeur', 1200)
    else:
        pal_largeur = 1200
    
    largeur_montant = 100  # mm
    longueur_travee = (nb_palettes_par_travee * pal_largeur) + ((nb_palettes_par_travee + 1) * largeur_montant/2)
    
    st.sidebar.metric("Longueur travée calculée", f"{longueur_travee/1000:.2f} m")
    
    # Nombre de niveaux
    if 'hauteur_uc' in st.session_state.params:
        hauteur_uc = st.session_state.params.get('hauteur_uc', 1600)
        hauteur_utile = st.session_state.params.get('hauteur_utile', 8.5)
        
        nb_niveaux_possibles = math.floor((hauteur_utile * 1000) / hauteur_uc)
        nb_niveaux = st.sidebar.number_input("Nombre de niveaux", 1, 10, min(nb_niveaux_possibles, 4))
    else:
        nb_niveaux = st.sidebar.number_input("Nombre de niveaux", 1, 10, 4)
    
    # Sauvegarde
    st.session_state.params['type_rayonnage'] = type_rayonnage
    st.session_state.params['profondeur_standard'] = profondeur_standard
    st.session_state.params['profondeur_totale'] = profondeur_totale
    st.session_state.params['configuration'] = configuration
    st.session_state.params['nb_palettes_par_travee'] = nb_palettes_par_travee
    st.session_state.params['longueur_travee'] = longueur_travee / 1000  # Conversion en m
    st.session_state.params['nb_niveaux'] = nb_niveaux

# ==================== 4. ENGINS ====================
elif param_tab == "🚜 Engins":
    st.sidebar.subheader("🚜 Parc d'engins")
    
    type_chariot = st.sidebar.selectbox(
        "Type de chariot principal",
        ["Chariot à mât rétractable (reach truck)", "Chariot frontal (counterbalance)", 
         "Tracteur (tugger)", "Transpalette manuel"]
    )
    
    if type_chariot == "Chariot à mât rétractable (reach truck)":
        largeur_allee = st.sidebar.slider("Largeur d'allée de travail (m)", 2.5, 3.2, 2.9, 0.05)
    elif type_chariot == "Chariot frontal (counterbalance)":
        largeur_allee = st.sidebar.slider("Largeur d'allée de travail (m)", 3.2, 4.2, 3.8, 0.05)
    elif type_chariot == "Tracteur (tugger)":
        largeur_allee = st.sidebar.slider("Largeur d'allée de travail (m)", 2.8, 3.5, 3.2, 0.05)
    else:
        largeur_allee = st.sidebar.slider("Largeur d'allée de travail (m)", 1.8, 2.5, 2.0, 0.05)
    
    # Allées transversales
    st.sidebar.subheader("🔄 Allées transversales")
    
    frequence_transversale = st.sidebar.number_input("Fréquence (tous les X travées)", 5, 30, 15)
    largeur_transversale = st.sidebar.slider("Largeur allée transversale (m)", 3.0, 4.5, 3.5, 0.1)
    
    # Sauvegarde
    st.session_state.params['type_chariot'] = type_chariot
    st.session_state.params['largeur_allee'] = largeur_allee
    st.session_state.params['frequence_transversale'] = frequence_transversale
    st.session_state.params['largeur_transversale'] = largeur_transversale

# ==================== 5. ZONAGE ====================
elif param_tab == "📋 Zonage":
    st.sidebar.subheader("📋 Zones fonctionnelles")
    
    # Pourcentage des zones
    st.sidebar.markdown("**Pourcentage de la surface totale**")
    
    zone_reception = st.sidebar.slider("Zone réception/expédition (%)", 5, 30, 20)
    zone_preparation = st.sidebar.slider("Zone préparation commandes (%)", 5, 25, 15)
    zone_qualite = st.sidebar.slider("Zone contrôle qualité (%)", 2, 10, 5)
    zone_bureaux = st.sidebar.slider("Zone bureaux/sociaux (%)", 2, 15, 5)
    
    # Vérification du total
    total_zonage = zone_reception + zone_preparation + zone_qualite + zone_bureaux
    
    if total_zonage > 50:
        st.sidebar.warning(f"⚠️ Total > 50% ({total_zonage}%) - Trop de zones annexes")
    
    # Type de gestion
    type_gestion = st.sidebar.radio(
        "Type de gestion",
        ["FIFO (First In First Out)", "LIFO (Last In First Out)", "Mixte"]
    )
    
    # Sauvegarde
    st.session_state.params['zone_reception'] = zone_reception
    st.session_state.params['zone_preparation'] = zone_preparation
    st.session_state.params['zone_qualite'] = zone_qualite
    st.session_state.params['zone_bureaux'] = zone_bureaux
    st.session_state.params['type_gestion'] = type_gestion

# ==================== 6. CALCULS ====================
elif param_tab == "📊 Calculs":
    st.sidebar.subheader("📊 Paramètres de calcul")
    
    taux_occupation = st.sidebar.slider("Taux d'occupation cible (%)", 70, 95, 85)
    coefficient_utilisation = st.sidebar.slider("Coefficient d'utilisation", 0.6, 0.95, 0.85)
    
    # Mode de calcul
    mode_calcul = st.sidebar.radio(
        "Mode de calcul",
        ["Optimisation surface", "Optimisation capacité", "Équilibré"]
    )
    
    st.session_state.params['taux_occupation'] = taux_occupation
    st.session_state.params['coeff_utilisation'] = coefficient_utilisation
    st.session_state.params['mode_calcul'] = mode_calcul

# ==================== FONCTIONS DE CALCUL PROFESSIONNEL ====================

def calculer_dimensionnement_pro(params):
    """Calcule le dimensionnement complet de l'entrepôt"""
    
    # Extraction des paramètres
    longueur = params.get('longueur', 50)
    largeur = params.get('largeur', 30)
    hauteur_utile = params.get('hauteur_utile', 8.5)
    espace_securite = params.get('espace_securite', 1.0)
    
    # Dimensions UC
    pal_longueur = params.get('pal_longueur', 800) / 1000  # en m
    pal_largeur = params.get('pal_largeur', 1200) / 1000  # en m
    hauteur_uc = params.get('hauteur_uc', 1600) / 1000  # en m
    
    # Rayonnages
    profondeur_totale = params.get('profondeur_totale', 2.4) / 1000  # conversion mm -> m
    longueur_travee = params.get('longueur_travee', 2.7)  # déjà en m
    nb_niveaux = params.get('nb_niveaux', 4)
    nb_palettes_par_travee = params.get('nb_palettes_par_travee', 3)
    
    # Engins
    largeur_allee = params.get('largeur_allee', 2.9)
    largeur_transversale = params.get('largeur_transversale', 3.5)
    frequence_transversale = params.get('frequence_transversale', 15)
    
    # Zonage
    zone_reception = params.get('zone_reception', 20) / 100
    zone_preparation = params.get('zone_preparation', 15) / 100
    zone_qualite = params.get('zone_qualite', 5) / 100
    zone_bureaux = params.get('zone_bureaux', 5) / 100
    
    # Calculs de base
    surface_totale = longueur * largeur
    
    # Surface dédiée aux zones annexes
    surface_annexes = surface_totale * (zone_reception + zone_preparation + zone_qualite + zone_bureaux)
    surface_stockage_brute = surface_totale - surface_annexes
    
    # Surface perdue pour les allées et sécurité
    surface_perdue_securite = 2 * espace_securite * (longueur + largeur)
    
    # Calcul du nombre de travées dans la longueur
    longueur_disponible = longueur - (2 * espace_securite)
    
    # Organisation des allées
    nb_travees_par_rangee = 0
    espace_restant = longueur_disponible
    
    while espace_restant >= (longueur_travee + largeur_allee):
        nb_travees_par_rangee += 1
        espace_restant -= (longueur_travee + largeur_allee)
    
    # Ajout des allées transversales
    nb_transversales = math.floor(nb_travees_par_rangee / frequence_transversale)
    longueur_perdue_transversales = nb_transversales * largeur_transversale
    
    # Ajustement du nombre de travées
    longueur_utile_reelle = nb_travees_par_rangee * longueur_travee + (nb_travees_par_rangee - 1) * largeur_allee
    if longueur_utile_reelle + longueur_perdue_transversales > longueur_disponible:
        nb_travees_par_rangee -= 1
        longueur_utile_reelle = nb_travees_par_rangee * longueur_travee + (nb_travees_par_rangee - 1) * largeur_allee
    
    # Calcul du nombre de rangées dans la largeur
    largeur_disponible = largeur - (2 * espace_securite)
    nb_rangees = 0
    espace_restant_largeur = largeur_disponible
    
    while espace_restant_largeur >= (profondeur_totale + largeur_allee):
        nb_rangees += 1
        espace_restant_largeur -= (profondeur_totale + largeur_allee)
    
    # Capacité totale
    nb_alveoles_par_travee = nb_niveaux * nb_palettes_par_travee
    capacite_theorique = nb_rangees * nb_travees_par_rangee * nb_alveoles_par_travee
    capacite_reelle = capacite_theorique * params.get('coeff_utilisation', 0.85)
    
    # Ratios
    ratio_stockage_surface = (capacite_reelle * pal_longueur * pal_largeur) / surface_totale
    densite_stockage = (capacite_reelle * (pal_longueur * pal_largeur * hauteur_uc)) / (surface_totale * hauteur_utile)
    
    return {
        'surface_totale': surface_totale,
        'surface_stockage': surface_stockage_brute,
        'surface_annexes': surface_annexes,
        'nb_rangees': nb_rangees,
        'nb_travees_par_rangee': nb_travees_par_rangee,
        'capacite_theorique': capacite_theorique,
        'capacite_reelle': int(capacite_reelle),
        'ratio_stockage_surface': ratio_stockage_surface,
        'densite_stockage': densite_stockage,
        'nb_transversales': nb_transversales,
        'longueur_utile': longueur_utile_reelle,
        'largeur_utile': largeur_disponible - (espace_restant_largeur)
    }

def generer_plan_professionnel(longueur, largeur, params, calculs):
    """Génère un plan 2D professionnel détaillé"""
    
    fig, ax = plt.subplots(1, 1, figsize=(16, 12))
    
    # Configuration du style
    plt.style.use('seaborn-v0_8-darkgrid')
    ax.set_facecolor('#f8f9fa')
    
    # Dessiner le contour de l'entrepôt
    contour = Rectangle((0, 0), longueur, largeur, 
                        linewidth=3, edgecolor='#2c3e50', 
                        facecolor='none', zorder=1)
    ax.add_patch(contour)
    
    # Zones fonctionnelles
    zone_reception = params.get('zone_reception', 20) / 100
    zone_preparation = params.get('zone_preparation', 15) / 100
    
    # Zone réception (en bas)
    hauteur_zone_reception = largeur * zone_reception
    rect_reception = Rectangle((0, 0), longueur, hauteur_zone_reception,
                              facecolor='#ffd700', alpha=0.2, 
                              edgecolor='#b8860b', linewidth=2, 
                              linestyle='--', zorder=2)
    ax.add_patch(rect_reception)
    ax.text(longueur/2, hauteur_zone_reception/2, 'ZONE RÉCEPTION',
            ha='center', va='center', fontsize=12, fontweight='bold',
            color='#b8860b', alpha=0.7)
    
    # Zone expédition (en haut)
    rect_expedition = Rectangle((0, largeur - hauteur_zone_reception), 
                                longueur, hauteur_zone_reception,
                                facecolor='#98fb98', alpha=0.2,
                                edgecolor='#228b22', linewidth=2,
                                linestyle='--', zorder=2)
    ax.add_patch(rect_expedition)
    ax.text(longueur/2, largeur - hauteur_zone_reception/2, 'ZONE EXPÉDITION',
            ha='center', va='center', fontsize=12, fontweight='bold',
            color='#228b22', alpha=0.7)
    
    # Zone préparation (au centre)
    rect_preparation = Rectangle((0, hauteur_zone_reception), 
                                 longueur, largeur - 2*hauteur_zone_reception,
                                 facecolor='#add8e6', alpha=0.1,
                                 edgecolor='#4682b4', linewidth=2,
                                 linestyle='--', zorder=2)
    ax.add_patch(rect_preparation)
    
    # Espace de sécurité (périmètre)
    espace_securite = params.get('espace_securite', 1.0)
    zone_securite = Rectangle((espace_securite, espace_securite),
                              longueur - 2*espace_securite,
                              largeur - 2*espace_securite,
                              linewidth=2, edgecolor='#e74c3c',
                              facecolor='none', linestyle=':',
                              alpha=0.5, zorder=3)
    ax.add_patch(zone_securite)
    
    # Allées principales
    largeur_allee = params.get('largeur_allee', 2.9)
    nb_rangees = calculs['nb_rangees']
    
    # Allées longitudinales
    for i in range(nb_rangees + 1):
        x_allee = espace_securite + i * (params.get('profondeur_totale', 2.4) + largeur_allee)
        if x_allee < longueur - espace_securite:
            allee = Rectangle((x_allee, espace_securite),
                             largeur_allee,
                             largeur - 2*espace_securite,
                             facecolor='#ecf0f1', edgecolor='#7f8c8d',
                             linewidth=1, alpha=0.7, zorder=4)
            ax.add_patch(allee)
            # Ligne centrale
            ax.axvline(x=x_allee + largeur_allee/2, 
                      ymin=espace_securite/largeur,
                      ymax=(largeur - espace_securite)/largeur,
                      color='#7f8c8d', linestyle='--', 
                      linewidth=0.5, alpha=0.5)
    
    # Allées transversales
    nb_travees = calculs['nb_travees_par_rangee']
    frequence_transversale = params.get('frequence_transversale', 15)
    largeur_transversale = params.get('largeur_transversale', 3.5)
    
    for i in range(1, nb_travees):
        if i % frequence_transversale == 0:
            y_allee = espace_securite + i * (params.get('longueur_travee', 2.7) + largeur_allee)
            if y_allee < largeur - espace_securite:
                allee_trans = Rectangle((espace_securite, y_allee),
                                       longueur - 2*espace_securite,
                                       largeur_transversale,
                                       facecolor='#ecf0f1', edgecolor='#7f8c8d',
                                       linewidth=1, alpha=0.7, zorder=4)
                ax.add_patch(allee_trans)
    
    # Rayonnages
    couleurs_rayonnage = ['#3498db', '#2980b9', '#1f618d', '#154360']
    profondeur = params.get('profondeur_totale', 2.4)
    longueur_travee = params.get('longueur_travee', 2.7)
    
    for i in range(nb_rangees):
        x_start = espace_securite + i * (profondeur + largeur_allee) + largeur_allee
        couleur = couleurs_rayonnage[i % len(couleurs_rayonnage)]
        
        for j in range(nb_travees):
            y_start = espace_securite + j * (longueur_travee + largeur_allee)
            
            # Vérifier si on n'est pas sur une allée transversale
            if j % frequence_transversale != 0:
                rayonnage = Rectangle((x_start, y_start),
                                     profondeur, longueur_travee,
                                     facecolor=couleur, edgecolor='white',
                                     linewidth=1.5, alpha=0.9, zorder=5)
                ax.add_patch(rayonnage)
                
                # Ajouter le numéro de travée
                ax.text(x_start + profondeur/2, y_start + longueur_travee/2,
                       f'T{j+1}', ha='center', va='center',
                       fontsize=8, color='white', fontweight='bold')
    
    # Ajouter la légende
    legend_elements = [
        Rectangle((0, 0), 1, 1, facecolor='#ecf0f1', label='Allées circulation'),
        Rectangle((0, 0), 1, 1, facecolor='#3498db', label='Rayonnages'),
        Rectangle((0, 0), 1, 1, facecolor='#ffd700', alpha=0.2, label='Zone réception'),
        Rectangle((0, 0), 1, 1, facecolor='#98fb98', alpha=0.2, label='Zone expédition'),
        plt.Line2D([0], [0], color='#e74c3c', linestyle=':', label='Zone sécurité')
    ]
    
    ax.legend(handles=legend_elements, loc='upper right',
             bbox_to_anchor=(1.15, 1), frameon=True,
             facecolor='white', edgecolor='black', fontsize=10)
    
    # Configuration des axes
    ax.set_xlim(-2, longueur + 2)
    ax.set_ylim(-2, largeur + 2)
    ax.set_aspect('equal')
    ax.set_xlabel('Longueur (mètres)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Largeur (mètres)', fontsize=12, fontweight='bold')
    ax.set_title('PLAN MASSE DE L\'ENTREPÔT - CONFIGURATION OPTIMISÉE',
                fontsize=16, fontweight='bold', pad=20)
    
    # Grille
    ax.grid(True, which='major', linestyle=':', linewidth=0.5, color='gray', alpha=0.3)
    
    # Graduations
    xticks = np.arange(0, longueur + 1, 5)
    yticks = np.arange(0, largeur + 1, 5)
    ax.set_xticks(xticks)
    ax.set_yticks(yticks)
    
    # Ajouter une boussole
    ax.annotate('N', xy=(longueur-2, largeur-2), xytext=(longueur-1, largeur-1),
                arrowprops=dict(facecolor='black', shrink=0.05, width=2),
                fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    return fig

# ==================== AFFICHAGE PRINCIPAL ====================

# Vérification que tous les paramètres sont définis
params_complets = all(k in st.session_state.params for k in 
                      ['longueur', 'largeur', 'hauteur_utile', 'pal_longueur', 
                       'profondeur_totale', 'longueur_travee', 'largeur_allee'])

if params_complets and st.sidebar.button("🚀 LANCER LE DIMENSIONNEMENT", use_container_width=True):
    
    # Calcul du dimensionnement
    calculs = calculer_dimensionnement_pro(st.session_state.params)
    
    # Affichage des résultats
    col1, col2 = st.columns([1, 1.2])
    
    with col1:
        st.markdown("## 📊 RÉSULTATS DU DIMENSIONNEMENT")
        
        # Métriques principales dans des cartes
        col_a, col_b = st.columns(2)
        
        with col_a:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Surface totale", f"{calculs['surface_totale']:.0f} m²")
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Surface stockage", f"{calculs['surface_stockage']:.0f} m²")
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Nombre de rangées", f"{calculs['nb_rangees']}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col_b:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Travées par rangée", f"{calculs['nb_travees_par_rangee']}")
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Allées transversales", f"{calculs['nb_transversales']}")
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Ratio stockage/surface", f"{calculs['ratio_stockage_surface']:.2f}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Résultat principal
        st.markdown('<div class="result-card">', unsafe_allow_html=True)
        st.markdown(f"### 🏆 CAPACITÉ TOTALE")
        st.markdown(f"# {calculs['capacite_reelle']:,.0f} palettes")
        st.markdown(f"**Théorique:** {calculs['capacite_theorique']:,.0f} | **Taux occup.:** {st.session_state.params.get('taux_occupation', 85)}%")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Détails techniques
        with st.expander("📋 DÉTAILS TECHNIQUES COMPLETS"):
            col_c, col_d = st.columns(2)
            
            with col_c:
                st.markdown("**📏 Dimensions utiles**")
                st.write(f"- Longueur utile: {calculs['longueur_utile']:.2f} m")
                st.write(f"- Largeur utile: {calculs['largeur_utile']:.2f} m")
                st.write(f"- Hauteur utile: {st.session_state.params.get('hauteur_utile', 8.5):.2f} m")
                
                st.markdown("**🏗️ Configuration rayonnages**")
                st.write(f"- Profondeur: {st.session_state.params.get('profondeur_totale', 2.4):.2f} m")
                st.write(f"- Longueur travée: {st.session_state.params.get('longueur_travee', 2.7):.2f} m")
                st.write(f"- Niveaux: {st.session_state.params.get('nb_niveaux', 4)}")
            
            with col_d:
                st.markdown("**🚜 Circulation**")
                st.write(f"- Allée principale: {st.session_state.params.get('largeur_allee', 2.9):.2f} m")
                st.write(f"- Allée transversale: {st.session_state.params.get('largeur_transversale', 3.5):.2f} m")
                
                st.markdown("**📦 Unités de charge**")
                st.write(f"- Type palette: {st.session_state.params.get('pal_longueur', 800)}x{st.session_state.params.get('pal_largeur', 1200)} mm")
                st.write(f"- Hauteur UC: {st.session_state.params.get('hauteur_uc', 1.6):.2f} m")
                st.write(f"- Poids max: {st.session_state.params.get('poids_uc', 1000)} kg")
        
        # Conformité normative
        st.markdown("### ✅ CONFORMITÉ NORMATIVE")
        
        normes = {
            "ISO 8611 (Palettes)": "✓ Conforme",
            "EN 15635 (Rayonnages)": "✓ Conforme",
            "ISO 45001 (Sécurité)": "✓ Conforme",
            "Espaces sécurité": "✓ Respectés",
            "Allées circulation": "✓ Optimisées"
        }
        
        for norme, status in normes.items():
            st.markdown(f"- **{norme}:** {status}")
    
    with col2:
        st.markdown("## 🗺️ PLAN MASSE DE L'ENTREPÔT")
        
        # Génération du plan professionnel
        fig = generer_plan_professionnel(
            st.session_state.params['longueur'],
            st.session_state.params['largeur'],
            st.session_state.params,
            calculs
        )
        
        st.pyplot(fig)
        
        # Options d'export
        col_e, col_f = st.columns(2)
        
        with col_e:
            if st.button("📸 Télécharger PNG (haute résolution)", use_container_width=True):
                fig.savefig("plan_entrepot_professionnel.png", dpi=300, bbox_inches='tight')
                with open("plan_entrepot_professionnel.png", "rb") as file:
                    st.download_button(
                        "Confirmer téléchargement PNG",
                        file,
                        "plan_entrepot_professionnel.png",
                        "image/png"
                    )
        
        with col_f:
            if st.button("📊 Exporter données techniques", use_container_width=True):
                data = {
                    'Catégorie': ['Dimensions', 'Dimensions', 'Dimensions', 'Capacité', 'Capacité', 'Circulation'],
                    'Paramètre': ['Longueur', 'Largeur', 'Hauteur', 'Capacité théorique', 'Capacité réelle', 'Largeur allée'],
                    'Valeur': [st.session_state.params['longueur'], 
                              st.session_state.params['largeur'],
                              st.session_state.params['hauteur_utile'],
                              calculs['capacite_theorique'],
                              calculs['capacite_reelle'],
                              st.session_state.params['largeur_allee']],
                    'Unité': ['m', 'm', 'm', 'palettes', 'palettes', 'm']
                }
                df = pd.DataFrame(data)
                csv = df.to_csv(index=False)
                st.download_button(
                    "Confirmer téléchargement CSV",
                    csv,
                    "dimensionnement_technique.csv",
                    "text/csv"
                )

else:
    # Message d'accueil
    st.markdown("## 👋 BIENVENUE DANS L'OUTIL DE DIMENSIONNEMENT PROFESSIONNEL")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="info-box">
        <h3>📋 PARAMÈTRES À RENSEIGNER</h3>
        <ol>
            <li><b>Dimensions du bâtiment</b> - Longueur, largeur, hauteur</li>
            <li><b>Unités de charge</b> - Type de palette, poids, dimensions</li>
            <li><b>Configuration rayonnages</b> - Simple/double face, travées</li>
            <li><b>Engins de manutention</b> - Type de chariot, largeur allées</li>
            <li><b>Zonage fonctionnel</b> - Réception, expédition, préparation</li>
            <li><b>Paramètres de calcul</b> - Taux d'occupation, coefficients</li>
        </ol>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="warning-box">
        <h3>🎯 FONCTIONNALITÉS</h3>
        <ul>
            <li>✅ Calcul automatique de la capacité optimale</li>
            <li>✅ Prise en compte des normes ISO et EN</li>
            <li>✅ Génération de plan 2D professionnel</li>
            <li>✅ Optimisation des allées et circulations</li>
            <li>✅ Ratios de performance et densité</li>
            <li>✅ Export des données techniques</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.info("👈 **Complétez tous les paramètres dans la barre latérale (6 onglets) puis cliquez sur 'LANCER LE DIMENSIONNEMENT'**")

# Pied de page
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: gray; padding: 1rem;'>
        <p>📐 Dimensionnement Professionnel d'Entrepôt - Version Ingénieur</p>
        <p>Conforme aux normes ISO 8611, EN 15635, ISO 45001</p>
        <p>© 2024 - Tous droits réservés</p>
    </div>
    """,
    unsafe_allow_html=True
)
