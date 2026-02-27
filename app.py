import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Rectangle, FancyBboxPatch
import math

# Configuration de la page
st.set_page_config(
    page_title="Dimensionnement d'Entrepôt",
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
        padding: 1rem;
        background: linear-gradient(90deg, #3498db 0%, #2980b9 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
    }
    .result-card {
        background-color: #d4edda;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #28a745;
    }
    </style>
""", unsafe_allow_html=True)

# Titre principal
st.markdown('<h1 class="main-header">📐 DIMENSIONNEMENT AUTOMATIQUE D\'ENTREPÔT</h1>', 
            unsafe_allow_html=True)

# Initialisation des paramètres dans session state
if 'params' not in st.session_state:
    st.session_state.params = {
        'longueur': 50.0,
        'largeur': 30.0,
        'hauteur': 8.0,
        'type_palette': 'Europe (800x1200)',
        'type_rayonnage': 'Classique',
        'largeur_allee': 3.0,
        'nb_niveaux': 3,
        'profondeur_double': False,
        'zone_securite': 10
    }

# Sidebar pour les paramètres d'entrée
st.sidebar.image("https://via.placeholder.com/300x100/3498db/ffffff?text=DIMENSIONNEMENT", use_column_width=True)
st.sidebar.title("📏 Paramètres d'entrée")

# Dimensions de l'entrepôt
st.sidebar.subheader("🏢 Dimensions de l'entrepôt")
longueur = st.sidebar.number_input("Longueur (m)", min_value=5.0, max_value=200.0, value=50.0, step=1.0)
largeur = st.sidebar.number_input("Largeur (m)", min_value=5.0, max_value=100.0, value=30.0, step=1.0)
hauteur = st.sidebar.number_input("Hauteur sous plafond (m)", min_value=3.0, max_value=20.0, value=8.0, step=0.5)

# Type de palette
st.sidebar.subheader("📦 Type de palette")
type_palette = st.sidebar.selectbox(
    "Dimensions palette",
    ["Europe (800x1200)", "Industrielle (1000x1200)", "Américaine (1200x1200)", "Demi-palette (600x800)", "Personnalisée"]
)

if type_palette == "Personnalisée":
    col1, col2 = st.sidebar.columns(2)
    with col1:
        palette_longueur = st.number_input("Longueur palette (mm)", min_value=400, max_value=2000, value=800, step=50)
    with col2:
        palette_largeur = st.number_input("Largeur palette (mm)", min_value=400, max_value=2000, value=1200, step=50)
else:
    # Dimensions standards
    dimensions_palette = {
        "Europe (800x1200)": (800, 1200),
        "Industrielle (1000x1200)": (1000, 1200),
        "Américaine (1200x1200)": (1200, 1200),
        "Demi-palette (600x800)": (600, 800)
    }
    palette_longueur, palette_largeur = dimensions_palette[type_palette]

# Type de rayonnage
st.sidebar.subheader("🏗️ Type de rayonnage")
type_rayonnage = st.sidebar.selectbox(
    "Configuration",
    ["Classique", "Navette", "Mobile", "Cantilever", "Drive-in"]
)

# Configuration des allées
st.sidebar.subheader("🚶 Configuration des allées")
type_allee = st.sidebar.selectbox(
    "Type d'allée",
    ["Simple (chariot manuel)", "Double (chariot élévateur)", "Large (tracteur)", "Très large (semi-remorque)"]
)

largeurs_allee = {
    "Simple (chariot manuel)": 1.8,
    "Double (chariot élévateur)": 3.0,
    "Large (tracteur)": 3.5,
    "Très large (semi-remorque)": 4.5
}
largeur_allee = st.sidebar.slider(
    "Largeur d'allée (m)", 
    min_value=1.5, 
    max_value=6.0, 
    value=largeurs_allee[type_allee],
    step=0.1
)

# Configuration des rayonnages
st.sidebar.subheader("📊 Configuration des rayonnages")
col1, col2 = st.sidebar.columns(2)
with col1:
    nb_niveaux = st.number_input("Nombre de niveaux", min_value=1, max_value=10, value=3)
with col2:
    profondeur_double = st.checkbox("Double profondeur", value=False)

zone_securite = st.sidebar.slider("Zone de sécurité (%)", min_value=5, max_value=20, value=10)

# Bouton de calcul
calculer = st.sidebar.button("🚀 Lancer le dimensionnement", use_container_width=True)

# ==================== FONCTIONS DE CALCUL ====================

def calculer_dimensions_rayonnage(palette_longueur, palette_largeur, nb_niveaux, profondeur_double):
    """Calcule les dimensions d'un rayonnage"""
    # Conversion mm -> m
    pal_l = palette_longueur / 1000
    pal_L = palette_largeur / 1000
    
    # Épaisseur des montants (m)
    epaisseur_montant = 0.1
    
    # Hauteur du rayonnage
    hauteur_rayonnage = nb_niveaux * (pal_L + 0.15) + 0.2  # 15cm d'espace par niveau + 20cm de base
    
    # Profondeur du rayonnage
    if profondeur_double:
        profondeur_rayonnage = (pal_l * 2) + 0.3  # Double profondeur + espace
    else:
        profondeur_rayonnage = pal_l + 0.15  # Simple profondeur
    
    # Longueur d'un alvéole
    longueur_alveole = pal_L + 0.1  # 10cm d'espace
    
    return {
        'hauteur': hauteur_rayonnage,
        'profondeur': profondeur_rayonnage,
        'longueur_alveole': longueur_alveole,
        'pal_l': pal_l,
        'pal_L': pal_L
    }

def calculer_capacite(longueur, largeur, hauteur, largeur_allee, dimensions_ray, zone_securite):
    """Calcule la capacité de stockage"""
    
    # Surface utile (enlevant zone de sécurité)
    surface_totale = longueur * largeur
    surface_utile = surface_totale * (1 - zone_securite/100)
    
    # Organisation des allées
    nb_rangees_longueur = math.floor((longueur - largeur_allee) / (dimensions_ray['profondeur'] + largeur_allee/2))
    nb_rangees_largeur = math.floor((largeur - largeur_allee) / (dimensions_ray['profondeur'] + largeur_allee/2))
    
    # Nombre d'alvéoles par rangée
    nb_alveoles_par_rangee = math.floor(longueur / dimensions_ray['longueur_alveole'])
    
    # Calculs
    nb_total_rangees = nb_rangees_longueur + nb_rangees_largeur
    nb_total_alveoles = nb_total_rangees * nb_alveoles_par_rangee
    capacite_totale = nb_total_alveoles * nb_niveaux
    
    return {
        'surface_totale': surface_totale,
        'surface_utile': surface_utile,
        'nb_rangees': nb_total_rangees,
        'nb_alveoles_par_rangee': nb_alveoles_par_rangee,
        'capacite': capacite_totale,
        'nb_rangees_longueur': nb_rangees_longueur,
        'nb_rangees_largeur': nb_rangees_largeur
    }

def generer_plan_2d(longueur, largeur, largeur_allee, dimensions_ray, calculs):
    """Génère un plan 2D de l'entrepôt"""
    
    fig, ax = plt.subplots(1, 1, figsize=(14, 10))
    
    # Dessiner le contour de l'entrepôt
    entrepot = Rectangle((0, 0), longueur, largeur, linewidth=3, 
                        edgecolor='black', facecolor='none', alpha=1)
    ax.add_patch(entrepot)
    
    # Couleurs pour les différents éléments
    couleur_allee = '#d3d3d3'  # Gris clair
    couleur_rayonnage = '#87CEEB'  # Bleu ciel
    couleur_rayonnage_fonce = '#4682B4'  # Bleu acier
    
    # Dessiner les allées principales
    # Allée centrale longitudinale
    ax.add_patch(Rectangle((longueur/2 - largeur_allee/2, 0), 
                           largeur_allee, largeur, 
                           facecolor=couleur_allee, alpha=0.3, edgecolor='gray', linewidth=1))
    
    # Allée transversale
    ax.add_patch(Rectangle((0, largeur/2 - largeur_allee/2), 
                           longueur, largeur_allee, 
                           facecolor=couleur_allee, alpha=0.3, edgecolor='gray', linewidth=1))
    
    # Dessiner les rayonnages
    # Rayonnages sur la longueur
    for i in range(calculs['nb_rangees_longueur']):
        x = (i * (dimensions_ray['profondeur'] + largeur_allee/2)) + 1
        y = 2
        # Rayonnage de gauche
        ax.add_patch(Rectangle((x, y), 
                               dimensions_ray['profondeur'], 
                               largeur/2 - largeur_allee/2 - 4,
                               facecolor=couleur_rayonnage, edgecolor='blue', alpha=0.7))
        # Ajouter des lignes pour représenter les alvéoles
        for j in range(0, int(largeur/2 - largeur_allee/2 - 4), 
                      int(dimensions_ray['longueur_alveole']*2)):
            ax.axhline(y=y+j, xmin=x/longueur, 
                      xmax=(x+dimensions_ray['profondeur'])/longueur, 
                      color='white', linewidth=0.5)
        
        # Rayonnage de droite
        ax.add_patch(Rectangle((x, largeur/2 + largeur_allee/2 + 2), 
                               dimensions_ray['profondeur'], 
                               largeur/2 - largeur_allee/2 - 4,
                               facecolor=couleur_rayonnage_fonce, edgecolor='darkblue', alpha=0.7))
    
    # Rayonnages sur la largeur
    for i in range(calculs['nb_rangees_largeur']):
        y = (i * (dimensions_ray['profondeur'] + largeur_allee/2)) + 1
        x = 2
        # Rayonnage du bas
        ax.add_patch(Rectangle((x, y), 
                               longueur/2 - largeur_allee/2 - 4, 
                               dimensions_ray['profondeur'],
                               facecolor=couleur_rayonnage, edgecolor='blue', alpha=0.7))
        # Rayonnage du haut
        ax.add_patch(Rectangle((longueur/2 + largeur_allee/2 + 2, y), 
                               longueur/2 - largeur_allee/2 - 4, 
                               dimensions_ray['profondeur'],
                               facecolor=couleur_rayonnage_fonce, edgecolor='darkblue', alpha=0.7))
    
    # Ajouter des étiquettes pour les zones
    ax.text(2, largeur-2, 'Zone A', fontsize=12, fontweight='bold', color='darkblue')
    ax.text(longueur-10, largeur-2, 'Zone B', fontsize=12, fontweight='bold', color='darkblue')
    ax.text(2, 2, 'Zone C', fontsize=12, fontweight='bold', color='darkblue')
    ax.text(longueur-10, 2, 'Zone D', fontsize=12, fontweight='bold', color='darkblue')
    
    # Légende
    legend_elements = [
        Rectangle((0, 0), 1, 1, facecolor=couleur_allee, alpha=0.3, label='Allées'),
        Rectangle((0, 0), 1, 1, facecolor=couleur_rayonnage, label='Rayonnages'),
        Rectangle((0, 0), 1, 1, facecolor='white', edgecolor='black', label='Contour entrepôt')
    ]
    ax.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(1.15, 1))
    
    # Configuration du graphique
    ax.set_xlim(-2, longueur + 2)
    ax.set_ylim(-2, largeur + 2)
    ax.set_aspect('equal')
    ax.set_xlabel('Longueur (m)', fontsize=12)
    ax.set_ylabel('Largeur (m)', fontsize=12)
    ax.set_title('📐 Plan 2D de l\'entrepôt - Vue de dessus', fontsize=16, fontweight='bold')
    ax.grid(True, alpha=0.3)
    
    # Ajouter une échelle
    ax.plot([longueur-20, longueur-10], [largeur+1, largeur+1], 'k-', linewidth=3)
    ax.text(longueur-15, largeur+1.5, '10 m', ha='center')
    
    return fig

# ==================== AFFICHAGE PRINCIPAL ====================

# Création de deux colonnes
col_gauche, col_droite = st.columns([1, 1])

with col_gauche:
    st.markdown("## 📋 Paramètres actuels")
    
    # Affichage des paramètres dans des métriques
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Longueur", f"{longueur} m")
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Largeur", f"{largeur} m")
        st.markdown('</div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Hauteur", f"{hauteur} m")
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Informations sur la palette
    st.markdown("### 📦 Dimensions palette")
    col1, col2 = st.columns(2)
    with col1:
        st.info(f"Longueur: {palette_longueur} mm")
    with col2:
        st.info(f"Largeur: {palette_largeur} mm")

if calculer:
    # Calcul des dimensions des rayonnages
    dimensions_ray = calculer_dimensions_rayonnage(
        palette_longueur, palette_largeur, nb_niveaux, profondeur_double
    )
    
    # Calcul de la capacité
    calculs = calculer_capacite(
        longueur, largeur, hauteur, largeur_allee, dimensions_ray, zone_securite
    )
    
    with col_gauche:
        st.markdown("---")
        st.markdown("## 📊 Résultats du dimensionnement")
        
        # Résultats dans des métriques
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<div class="result-card">', unsafe_allow_html=True)
            st.metric("Surface totale", f"{calculs['surface_totale']:.1f} m²")
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="result-card">', unsafe_allow_html=True)
            st.metric("Surface utile", f"{calculs['surface_utile']:.1f} m²")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="result-card">', unsafe_allow_html=True)
            st.metric("Nombre de rangées", f"{calculs['nb_rangees']}")
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="result-card">', unsafe_allow_html=True)
            st.metric("Alvéoles par rangée", f"{calculs['nb_alveoles_par_rangee']}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Capacité totale
        st.markdown('<div class="result-card" style="background-color: #c3e6cb;">', unsafe_allow_html=True)
        st.metric("🏆 CAPACITÉ TOTALE DE STOCKAGE", 
                 f"{calculs['capacite'] * nb_niveaux} palettes",
                 delta=f"{nb_niveaux} niveaux")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Détails techniques
        with st.expander("📐 Voir les détails techniques"):
            st.write(f"**Hauteur rayonnage:** {dimensions_ray['hauteur']:.2f} m")
            st.write(f"**Profondeur rayonnage:** {dimensions_ray['profondeur']:.2f} m")
            st.write(f"**Longueur alvéole:** {dimensions_ray['longueur_alveole']:.2f} m")
            st.write(f"**Taux d'occupation max:** {100 - zone_securite}%")
            st.write(f"**Nombre de niveaux:** {nb_niveaux}")
            st.write(f"**Type d'allée:** {type_allee} ({largeur_allee} m)")
        
        # Optimisation possible
        taux_occupation = (calculs['capacite'] * nb_niveaux * 1.5) / (longueur * largeur * hauteur) * 100
        st.progress(min(taux_occupation/100, 1.0))
        st.caption(f"Taux d'optimisation: {taux_occupation:.1f}%")
    
    with col_droite:
        st.markdown("## 🗺️ Plan 2D de l'entrepôt")
        
        # Génération du plan
        fig = generer_plan_2d(longueur, largeur, largeur_allee, dimensions_ray, calculs)
        st.pyplot(fig)
        
        # Options de téléchargement
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📥 Télécharger le plan PNG", use_container_width=True):
                fig.savefig("plan_entrepot.png", dpi=300, bbox_inches='tight')
                with open("plan_entrepot.png", "rb") as file:
                    st.download_button(
                        "Confirmer téléchargement",
                        file,
                        "plan_entrepot.png",
                        "image/png"
                    )
        
        with col2:
            if st.button("📊 Exporter les données", use_container_width=True):
                data = {
                    'Paramètre': ['Longueur', 'Largeur', 'Hauteur', 'Surface', 'Capacité', 'Nb rangées'],
                    'Valeur': [longueur, largeur, hauteur, calculs['surface_totale'], 
                              calculs['capacite'] * nb_niveaux, calculs['nb_rangees']],
                    'Unité': ['m', 'm', 'm', 'm²', 'palettes', '-']
                }
                df = pd.DataFrame(data)
                csv = df.to_csv(index=False)
                st.download_button(
                    "Confirmer téléchargement",
                    csv,
                    "dimensionnement.csv",
                    "text/csv"
                )

else:
    with col_gauche:
        st.info("👈 Ajustez les paramètres dans la barre latérale et cliquez sur 'Lancer le dimensionnement'")
        
        # Exemple d'illustration
        st.markdown("### 🎯 Fonctionnalités")
        st.markdown("""
        - **Dimensions personnalisables** de l'entrepôt
        - **Différents types de palettes** (Europe, Industrielle, etc.)
        - **Configuration des allées** selon l'équipement
        - **Rayonnages simple ou double profondeur**
        - **Calcul automatique** de la capacité
        - **Génération d'un plan 2D** avec disposition
        - **Export des résultats** en PNG et CSV
        """)
    
    with col_droite:
        st.markdown("## 🗺️ Aperçu du plan")
        
        # Plan par défaut pour illustration
        fig, ax = plt.subplots(1, 1, figsize=(12, 8))
        
        # Dessiner un entrepôt exemple
        entrepot = Rectangle((0, 0), 50, 30, linewidth=3, edgecolor='black', facecolor='none')
        ax.add_patch(entrepot)
        
        # Allées
        ax.add_patch(Rectangle((23.5, 0), 3, 30, facecolor='lightgray', alpha=0.5))
        ax.add_patch(Rectangle((0, 13.5), 50, 3, facecolor='lightgray', alpha=0.5))
        
        # Rayonnages simplifiés
        for i in range(3):
            ax.add_patch(Rectangle((2 + i*8, 2), 1.5, 10, facecolor='skyblue', alpha=0.8))
            ax.add_patch(Rectangle((2 + i*8, 18), 1.5, 10, facecolor='steelblue', alpha=0.8))
        
        ax.set_xlim(-2, 52)
        ax.set_ylim(-2, 32)
        ax.set_aspect('equal')
        ax.set_xlabel('Longueur (m)')
        ax.set_ylabel('Largeur (m)')
        ax.set_title('Exemple de plan 2D (avec paramètres par défaut)')
        ax.grid(True, alpha=0.3)
        
        st.pyplot(fig)
        st.caption("Plan illustratif - Utilisez les paramètres pour générer votre plan personnalisé")

# Pied de page
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: gray; padding: 1rem;'>
        <p>📐 Dimensionnement automatique d'entrepôt - Version 2.0</p>
        <p>Prend en compte les allées, types de transport et disposition optimale des rayonnages</p>
    </div>
    """,
    unsafe_allow_html=True
)
