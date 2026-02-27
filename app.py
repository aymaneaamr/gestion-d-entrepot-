import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Rectangle
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
    dimensions_palette = {
        "Europe (800x1200)": (800, 1200),
        "Industrielle (1000x1200)": (1000, 1200),
        "Américaine (1200x1200)": (1200, 1200),
        "Demi-palette (600x800)": (600, 800)
    }
    palette_longueur, palette_largeur = dimensions_palette[type_palette]

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
    orientation = st.selectbox("Orientation des rayons", ["Longueur", "Largeur"])
with col2:
    profondeur_double = st.checkbox("Double profondeur", value=False)
    nb_rangees = st.number_input("Nombre de rangées", min_value=1, max_value=20, value=4)

zone_securite = st.sidebar.slider("Zone de sécurité (%)", min_value=5, max_value=20, value=10)

# Bouton de calcul
calculer = st.sidebar.button("🚀 Lancer le dimensionnement", use_container_width=True)

# ==================== FONCTIONS DE CALCUL ====================

def calculer_dimensions_rayonnage(palette_longueur, palette_largeur, nb_niveaux, profondeur_double):
    """Calcule les dimensions d'un rayonnage"""
    pal_l = palette_longueur / 1000
    pal_L = palette_largeur / 1000
    
    # Dimensions standard d'un rayonnage
    hauteur_rayonnage = nb_niveaux * (pal_L + 0.15) + 0.2
    
    if profondeur_double:
        profondeur_rayonnage = (pal_l * 2) + 0.3
    else:
        profondeur_rayonnage = pal_l + 0.15
    
    largeur_alveole = pal_L + 0.1
    
    return {
        'hauteur': hauteur_rayonnage,
        'profondeur': profondeur_rayonnage,
        'largeur_alveole': largeur_alveole,
        'pal_l': pal_l,
        'pal_L': pal_L
    }

def calculer_capacite(longueur, largeur, dimensions_ray, largeur_allee, nb_rangees, orientation):
    """Calcule la capacité de stockage"""
    
    if orientation == "Longueur":
        longueur_disponible = longueur - (2 * largeur_allee)
        nb_alveoles_par_rangee = math.floor(longueur_disponible / dimensions_ray['largeur_alveole'])
        longueur_rangee = nb_alveoles_par_rangee * dimensions_ray['largeur_alveole']
        capacite_par_rangee = nb_alveoles_par_rangee * nb_niveaux
    else:
        largeur_disponible = largeur - (2 * largeur_allee)
        nb_alveoles_par_rangee = math.floor(largeur_disponible / dimensions_ray['largeur_alveole'])
        longueur_rangee = nb_alveoles_par_rangee * dimensions_ray['largeur_alveole']
        capacite_par_rangee = nb_alveoles_par_rangee * nb_niveaux
    
    capacite_totale = capacite_par_rangee * nb_rangees
    
    return {
        'nb_alveoles_par_rangee': nb_alveoles_par_rangee,
        'longueur_rangee': longueur_rangee,
        'capacite_par_rangee': capacite_par_rangee,
        'capacite_totale': capacite_totale
    }

def generer_plan_2d_professionnel(longueur, largeur, largeur_allee, dimensions_ray, 
                                  nb_rangees, orientation, calculs):
    """Génère un plan 2D professionnel et bien structuré"""
    
    # Création de la figure avec un ratio approprié
    fig, ax = plt.subplots(1, 1, figsize=(14, 10))
    
    # Configuration du fond
    ax.set_facecolor('#f5f5f5')
    
    # Dessiner le contour de l'entrepôt avec double ligne
    contour_externe = Rectangle((0, 0), longueur, largeur, 
                                linewidth=3, edgecolor='#2c3e50', 
                                facecolor='none', zorder=1)
    contour_interne = Rectangle((0.2, 0.2), longueur-0.4, largeur-0.4, 
                                linewidth=1, edgecolor='#95a5a6', 
                                facecolor='none', linestyle='--', zorder=1)
    ax.add_patch(contour_externe)
    ax.add_patch(contour_interne)
    
    # Ajouter les dimensions sur le contour
    ax.text(longueur/2, -1.5, f'{longueur} m', ha='center', va='center', 
            fontsize=10, fontweight='bold', bbox=dict(boxstyle="round,pad=0.3", facecolor='white'))
    ax.text(-2.5, largeur/2, f'{largeur} m', ha='center', va='center', 
            fontsize=10, fontweight='bold', rotation=90, 
            bbox=dict(boxstyle="round,pad=0.3", facecolor='white'))
    
    # Dessiner les allées principales
    if orientation == "Longueur":
        # Allées longitudinales (parallèles à la longueur)
        for i in range(nb_rangees + 1):
            x_allee = i * (dimensions_ray['profondeur'] + largeur_allee)
            if x_allee < longueur:
                allee = Rectangle((x_allee, 0), largeur_allee, largeur,
                                 facecolor='#ecf0f1', edgecolor='#7f8c8d', 
                                 linewidth=1, alpha=0.8, zorder=2)
                ax.add_patch(allee)
                # Ajouter des pointillés au centre de l'allée
                ax.plot([x_allee + largeur_allee/2, x_allee + largeur_allee/2], 
                       [0, largeur], '--', color='#7f8c8d', linewidth=0.5, alpha=0.5)
    else:
        # Allées transversales (parallèles à la largeur)
        for i in range(nb_rangees + 1):
            y_allee = i * (dimensions_ray['profondeur'] + largeur_allee)
            if y_allee < largeur:
                allee = Rectangle((0, y_allee), longueur, largeur_allee,
                                 facecolor='#ecf0f1', edgecolor='#7f8c8d', 
                                 linewidth=1, alpha=0.8, zorder=2)
                ax.add_patch(allee)
                ax.plot([0, longueur], 
                       [y_allee + largeur_allee/2, y_allee + largeur_allee/2], 
                       '--', color='#7f8c8d', linewidth=0.5, alpha=0.5)
    
    # Dessiner les zones de sécurité (bordures)
    zone_securite_couleur = '#fff3cd'
    # Bande de sécurité en haut
    ax.add_patch(Rectangle((0, largeur-1), longueur, 1, 
                          facecolor=zone_securite_couleur, alpha=0.3, 
                          edgecolor='none', zorder=1))
    # Bande de sécurité en bas
    ax.add_patch(Rectangle((0, 0), longueur, 1, 
                          facecolor=zone_securite_couleur, alpha=0.3, 
                          edgecolor='none', zorder=1))
    # Bande de sécurité à gauche
    ax.add_patch(Rectangle((0, 0), 1, largeur, 
                          facecolor=zone_securite_couleur, alpha=0.3, 
                          edgecolor='none', zorder=1))
    # Bande de sécurité à droite
    ax.add_patch(Rectangle((longueur-1, 0), 1, largeur, 
                          facecolor=zone_securite_couleur, alpha=0.3, 
                          edgecolor='none', zorder=1))
    
    # Dessiner les rayonnages
    couleurs_rayonnage = ['#3498db', '#2980b9', '#1f618d', '#154360']
    
    if orientation == "Longueur":
        for i in range(nb_rangees):
            x_start = i * (dimensions_ray['profondeur'] + largeur_allee) + largeur_allee
            
            # Vérifier que le rayonnage reste dans l'entrepôt
            if x_start + dimensions_ray['profondeur'] <= longueur:
                # Rayonnage
                couleur = couleurs_rayonnage[i % len(couleurs_rayonnage)]
                rayonnage = Rectangle((x_start, 2), 
                                     dimensions_ray['profondeur'], 
                                     largeur - 4,
                                     facecolor=couleur, edgecolor='white',
                                     linewidth=2, alpha=0.9, zorder=3)
                ax.add_patch(rayonnage)
                
                # Ajouter un dégradé pour l'effet 3D
                for j in range(3):
                    ax.add_patch(Rectangle((x_start + j*0.1, 2), 0.05, largeur-4,
                                          facecolor='white', alpha=0.2, zorder=4))
                
                # Ajouter les alvéoles (représentation)
                nb_alveoles = min(calculs['nb_alveoles_par_rangee'], 10)  # Max 10 pour lisibilité
                espacement = (largeur - 4) / (nb_alveoles + 1)
                
                for k in range(nb_alveoles):
                    y_pos = 2 + (k + 1) * espacement
                    # Rectangle représentant une palette
                    pal = Rectangle((x_start + 0.2, y_pos - dimensions_ray['pal_L']/2),
                                   dimensions_ray['profondeur'] - 0.4,
                                   dimensions_ray['pal_L'] - 0.1,
                                   facecolor='#f1c40f', edgecolor='#e67e22',
                                   linewidth=1, alpha=0.7, zorder=5)
                    ax.add_patch(pal)
                    
                    # Ajouter le texte du niveau
                    ax.text(x_start + dimensions_ray['profondeur']/2, y_pos,
                           f'N{1}', ha='center', va='center',
                           fontsize=6, color='black', fontweight='bold')
                
                # Ajouter le numéro de la rangée
                ax.text(x_start + dimensions_ray['profondeur']/2, largeur/2,
                       f'R{i+1}', ha='center', va='center',
                       fontsize=12, color='white', fontweight='bold', zorder=6)
    
    else:  # Orientation Largeur
        for i in range(nb_rangees):
            y_start = i * (dimensions_ray['profondeur'] + largeur_allee) + largeur_allee
            
            if y_start + dimensions_ray['profondeur'] <= largeur:
                couleur = couleurs_rayonnage[i % len(couleurs_rayonnage)]
                rayonnage = Rectangle((2, y_start), 
                                     longueur - 4,
                                     dimensions_ray['profondeur'],
                                     facecolor=couleur, edgecolor='white',
                                     linewidth=2, alpha=0.9, zorder=3)
                ax.add_patch(rayonnage)
                
                # Ajouter les alvéoles
                nb_alveoles = min(calculs['nb_alveoles_par_rangee'], 10)
                espacement = (longueur - 4) / (nb_alveoles + 1)
                
                for k in range(nb_alveoles):
                    x_pos = 2 + (k + 1) * espacement
                    pal = Rectangle((x_pos - dimensions_ray['pal_L']/2, y_start + 0.2),
                                   dimensions_ray['pal_L'] - 0.1,
                                   dimensions_ray['profondeur'] - 0.4,
                                   facecolor='#f1c40f', edgecolor='#e67e22',
                                   linewidth=1, alpha=0.7, zorder=5)
                    ax.add_patch(pal)
                
                ax.text(longueur/2, y_start + dimensions_ray['profondeur']/2,
                       f'R{i+1}', ha='center', va='center',
                       fontsize=12, color='white', fontweight='bold', zorder=6)
    
    # Ajouter la légende
    legend_elements = [
        Rectangle((0, 0), 1, 1, facecolor='#ecf0f1', edgecolor='#7f8c8d', label='Allées de circulation'),
        Rectangle((0, 0), 1, 1, facecolor='#3498db', label='Rayonnages'),
        Rectangle((0, 0), 1, 1, facecolor='#f1c40f', label='Emplacements palettes'),
        Rectangle((0, 0), 1, 1, facecolor='#fff3cd', alpha=0.3, label='Zone de sécurité'),
        plt.Line2D([0], [0], color='#2c3e50', linewidth=3, label='Contour entrepôt')
    ]
    
    ax.legend(handles=legend_elements, loc='upper right', 
             bbox_to_anchor=(1.15, 1), frameon=True, 
             facecolor='white', edgecolor='black', fontsize=10)
    
    # Ajouter un titre et des labels
    ax.set_title('🗺️ PLAN 2D DE L\'ENTREPÔT - VUE DE DESSUS', 
                fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel('Longueur (mètres)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Largeur (mètres)', fontsize=12, fontweight='bold')
    
    # Configurer les axes
    ax.set_xlim(-3, longueur + 3)
    ax.set_ylim(-3, largeur + 3)
    ax.set_aspect('equal')
    
    # Grille plus professionnelle
    ax.grid(True, which='major', linestyle=':', linewidth=0.5, color='gray', alpha=0.3)
    
    # Graduations personnalisées
    xticks = np.arange(0, longueur + 1, 5)
    yticks = np.arange(0, largeur + 1, 5)
    ax.set_xticks(xticks)
    ax.set_yticks(yticks)
    ax.set_xticklabels([f'{int(x)}' for x in xticks])
    ax.set_yticklabels([f'{int(y)}' for y in yticks])
    
    # Ajouter une boussole (indication du nord)
    ax.annotate('N', xy=(longueur+1, largeur-2), xytext=(longueur+2, largeur-2),
                arrowprops=dict(facecolor='black', shrink=0.05, width=2),
                fontsize=14, fontweight='bold')
    
    # Ajouter un cartouche d'informations
    info_text = f"""INFORMATIONS:
    • Surface: {longueur*largeur:.0f} m²
    • Capacité: {calculs['capacite_totale']} palettes
    • Rangées: {nb_rangees}
    • Allées: {largeur_allee}m
    • Niveaux: {nb_niveaux}"""
    
    ax.text(0.02, 0.98, info_text, transform=ax.transAxes,
           fontsize=9, verticalalignment='top',
           bbox=dict(boxstyle='round', facecolor='white', alpha=0.9, edgecolor='black'))
    
    plt.tight_layout()
    return fig

# ==================== AFFICHAGE PRINCIPAL ====================

# Création de deux colonnes
col_gauche, col_droite = st.columns([1, 1.2])

with col_gauche:
    st.markdown("## 📋 Paramètres actuels")
    
    # Affichage des paramètres
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
        longueur, largeur, dimensions_ray, largeur_allee, nb_rangees, orientation
    )
    
    with col_gauche:
        st.markdown("---")
        st.markdown("## 📊 Résultats du dimensionnement")
        
        # Résultats
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<div class="result-card">', unsafe_allow_html=True)
            st.metric("Surface totale", f"{longueur * largeur:.1f} m²")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="result-card">', unsafe_allow_html=True)
            st.metric("Alvéoles par rangée", f"{calculs['nb_alveoles_par_rangee']}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Capacité totale
        st.markdown('<div class="result-card" style="background-color: #c3e6cb;">', unsafe_allow_html=True)
        st.metric("🏆 CAPACITÉ TOTALE DE STOCKAGE", 
                 f"{calculs['capacite_totale']} palettes",
                 delta=f"{nb_niveaux} niveaux")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Détails techniques
        with st.expander("📐 Voir les détails techniques"):
            st.write(f"**Hauteur rayonnage:** {dimensions_ray['hauteur']:.2f} m")
            st.write(f"**Profondeur rayonnage:** {dimensions_ray['profondeur']:.2f} m")
            st.write(f"**Largeur alvéole:** {dimensions_ray['largeur_alveole']:.2f} m")
            st.write(f"**Nombre de rangées:** {nb_rangees}")
            st.write(f"**Orientation:** {orientation}")
            st.write(f"**Type d'allée:** {type_allee} ({largeur_allee} m)")
        
        # Téléchargement des données
        if st.button("📥 Télécharger les données", use_container_width=True):
            data = {
                'Paramètre': ['Longueur', 'Largeur', 'Hauteur', 'Surface', 'Capacité', 
                             'Nb rangées', 'Alvéoles/rangée', 'Type palette'],
                'Valeur': [longueur, largeur, hauteur, longueur*largeur, 
                          calculs['capacite_totale'], nb_rangees, 
                          calculs['nb_alveoles_par_rangee'], type_palette],
                'Unité': ['m', 'm', 'm', 'm²', 'palettes', '-', '-', '-']
            }
            df = pd.DataFrame(data)
            csv = df.to_csv(index=False)
            st.download_button(
                "Confirmer téléchargement CSV",
                csv,
                "dimensionnement_entrepot.csv",
                "text/csv"
            )
    
    with col_droite:
        st.markdown("## 🗺️ Plan 2D professionnel")
        
        # Génération du plan amélioré
        fig = generer_plan_2d_professionnel(
            longueur, largeur, largeur_allee, dimensions_ray, 
            nb_rangees, orientation, calculs
        )
        st.pyplot(fig)
        
        # Options de téléchargement du plan
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📸 Télécharger le plan (PNG)", use_container_width=True):
                fig.savefig("plan_entrepot_professionnel.png", dpi=300, bbox_inches='tight')
                with open("plan_entrepot_professionnel.png", "rb") as file:
                    st.download_button(
                        "Confirmer PNG",
                        file,
                        "plan_entrepot_professionnel.png",
                        "image/png"
                    )
        
        with col2:
            if st.button("📊 Télécharger le plan (PDF)", use_container_width=True):
                fig.savefig("plan_entrepot_professionnel.pdf", format='pdf', bbox_inches='tight')
                with open("plan_entrepot_professionnel.pdf", "rb") as file:
                    st.download_button(
                        "Confirmer PDF",
                        file,
                        "plan_entrepot_professionnel.pdf",
                        "application/pdf"
                    )

else:
    with col_gauche:
        st.info("👈 Ajustez les paramètres dans la barre latérale et cliquez sur 'Lancer le dimensionnement'")
    
    with col_droite:
        st.markdown("## 🗺️ Aperçu du plan")
        st.info("Configurez les paramètres et lancez le calcul pour générer un plan professionnel")

# Pied de page
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: gray; padding: 1rem;'>
        <p>📐 Dimensionnement automatique d'entrepôt - Version Professionnelle</p>
        <p>Plan 2D structuré avec allées, rayonnages et emplacements de palettes</p>
    </div>
    """,
    unsafe_allow_html=True
)
