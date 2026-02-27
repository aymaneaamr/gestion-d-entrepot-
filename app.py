import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# Configuration de la page
st.set_page_config(
    page_title="Gestion d'Entrepôt ISO",
    page_icon="🏭",
    layout="wide"
)

# Style CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        color: #2c3e50;
        text-align: center;
        margin-bottom: 2rem;
    }
    .stApp {
        background-color: #f5f5f5;
    }
    </style>
""", unsafe_allow_html=True)

# Titre principal
st.markdown('<h1 class="main-header">🏭 Gestion d\'Entrepôt Intelligente</h1>', 
            unsafe_allow_html=True)
st.markdown("### Conforme aux normes ISO 50001 & 90001")

# Sidebar
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Menu",
    ["Accueil", "Gestion de Stock", "Dimensionnement", "Normes ISO", "Rapports"]
)

# Contenu principal
if page == "Accueil":
    st.header("🏠 Tableau de Bord")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Taux d'occupation", "78%", "+5%")
    with col2:
        st.metric("Efficacité énergétique", "92%", "+3%")
    with col3:
        st.metric("Qualité processus", "95%", "+2%")
    with col4:
        st.metric("Conformité ISO", "100%", "0%")

elif page == "Gestion de Stock":
    st.header("📦 Gestion de Stock")
    
    # Données exemple
    data = {
        'Produit': ['Produit A', 'Produit B', 'Produit C', 'Produit D'],
        'Catégorie': ['Électronique', 'Mécanique', 'Emballage', 'Électronique'],
        'Quantité': [150, 45, 200, 80],
        'Seuil min': [50, 60, 100, 50],
        'Emplacement': ['A1', 'B2', 'C3', 'A4']
    }
    df = pd.DataFrame(data)
    
    # Filtre
    categorie = st.selectbox("Filtrer par catégorie", ["Toutes", "Électronique", "Mécanique", "Emballage"])
    
    if categorie != "Toutes":
        df = df[df['Catégorie'] == categorie]
    
    st.dataframe(df, use_container_width=True)

elif page == "Dimensionnement":
    st.header("📐 Dimensionnement d'Entrepôt")
    
    col1, col2 = st.columns(2)
    
    with col1:
        longueur = st.number_input("Longueur (m)", 10, 200, 50)
        largeur = st.number_input("Largeur (m)", 10, 100, 30)
        hauteur = st.number_input("Hauteur (m)", 3, 20, 8)
    
    with col2:
        surface = longueur * largeur
        volume = surface * hauteur
        
        st.metric("Surface totale", f"{surface} m²")
        st.metric("Volume total", f"{volume} m³")
        st.metric("Capacité estimée", f"{int(volume/1.5)} palettes")

elif page == "Normes ISO":
    st.header("✅ Normes ISO")
    
    tab1, tab2 = st.tabs(["ISO 50001 (Énergie)", "ISO 90001 (Qualité)"])
    
    with tab1:
        st.subheader("Performance énergétique")
        
        data_energie = pd.DataFrame({
            'Mois': ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Juin'],
            'Consommation': [4500, 4200, 4300, 4100, 4400, 4300]
        })
        st.line_chart(data_energie.set_index('Mois'))
        
        st.success("✅ Conforme aux exigences ISO 50001")
    
    with tab2:
        st.subheader("Indicateurs qualité")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Taux de conformité", "98.5%", "+1.2%")
        with col2:
            st.metric("Satisfaction client", "4.8/5", "+0.3")

elif page == "Rapports":
    st.header("📊 Rapports")
    
    type_rapport = st.selectbox(
        "Type de rapport",
        ["Performance", "Stock", "Énergie", "Qualité"]
    )
    
    if st.button("Générer le rapport"):
        st.info("Rapport généré avec succès!")
        st.download_button(
            "Télécharger le rapport",
            "Contenu du rapport...",
            "rapport.txt"
        )
