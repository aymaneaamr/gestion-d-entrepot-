import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random

# Configuration de la page
st.set_page_config(
    page_title="Gestion d'Entrepôt ISO 50001 & 90001",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Style CSS personnalisé
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #2c3e50;
        text-align: center;
        padding: 1rem;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
    }
    .iso-badge {
        background-color: #27ae60;
        color: white;
        padding: 0.5rem;
        border-radius: 5px;
        text-align: center;
        font-weight: bold;
    }
    .warning-badge {
        background-color: #f39c12;
        color: white;
        padding: 0.3rem;
        border-radius: 3px;
    }
    </style>
""", unsafe_allow_html=True)

# Initialisation des données dans session state
if 'initialized' not in st.session_state:
    st.session_state.initialized = True
    
    # Données de stock
    st.session_state.stock_data = pd.DataFrame({
        'ID': [f'PRD00{i}' for i in range(1, 11)],
        'Produit': [f'Produit {chr(65+i)}' for i in range(10)],
        'Catégorie': ['Électronique', 'Mécanique', 'Emballage', 'Électronique', 'Mécanique', 
                      'Emballage', 'Électronique', 'Mécanique', 'Emballage', 'Électronique'],
        'Quantité': [150, 45, 200, 80, 320, 65, 180, 95, 430, 120],
        'Seuil_min': [50, 60, 100, 50, 150, 50, 80, 70, 200, 60],
        'Seuil_max': [300, 200, 500, 250, 600, 300, 400, 250, 800, 300],
        'Emplacement': ['A1', 'B2', 'C3', 'A4', 'B5', 'C6', 'A7', 'B8', 'C9', 'A10'],
        'Fournisseur': ['Fourn A', 'Fourn B', 'Fourn C', 'Fourn A', 'Fourn D', 
                        'Fourn C', 'Fourn E', 'Fourn B', 'Fourn F', 'Fourn A'],
        'Date_derniere_entree': pd.date_range(start='2024-01-01', periods=10, freq='D')
    })
    
    # Données de consommation énergétique
    dates = pd.date_range(start='2024-01-01', end='2024-03-31', freq='D')
    st.session_state.energie_data = pd.DataFrame({
        'Date': dates,
        'Consommation_kWh': [random.randint(350, 550) for _ in range(len(dates))],
        'Zone': [random.choice(['Réception', 'Stockage', 'Expédition', 'Bureaux']) for _ in range(len(dates))],
        'Temperature_ext': [random.randint(5, 25) for _ in range(len(dates))]
    })
    
    # Données qualité
    st.session_state.qualite_data = pd.DataFrame({
        'Date': pd.date_range(start='2024-01-01', end='2024-03-31', freq='W'),
        'Taux_conformite': [random.uniform(92, 99) for _ in range(13)],
        'Non_conformites': [random.randint(0, 5) for _ in range(13)],
        'Audit_score': [random.uniform(85, 100) for _ in range(13)]
    })

# En-tête principal
st.markdown('<h1 class="main-header">🏭 GESTION D\'ENTREPÔT INTELLIGENTE</h1>', 
            unsafe_allow_html=True)
st.markdown('<p class="iso-badge">✓ Certifié ISO 50001 (Management de l\'énergie) & ISO 90001 (Management de la qualité)</p>', 
            unsafe_allow_html=True)

# Sidebar pour la navigation
st.sidebar.image("https://via.placeholder.com/300x100/2c3e50/ffffff?text=ENTREPOT+ISO", use_column_width=True)
st.sidebar.title("📱 Navigation")

menu = st.sidebar.radio(
    "Menu principal",
    ["🏠 Tableau de bord",
     "📦 Gestion de stock",
     "📐 Dimensionnement",
     "⚡ ISO 50001 - Énergie",
     "✅ ISO 90001 - Qualité",
     "📊 Rapports & Analyses",
     "⚙️ Paramètres"]
)

# Informations système dans la sidebar
st.sidebar.markdown("---")
st.sidebar.markdown("### ℹ️ Informations")
st.sidebar.info(f"📅 Dernière mise à jour: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
st.sidebar.success("🟢 Système opérationnel")
st.sidebar.warning(f"📦 Alertes stock: {len(st.session_state.stock_data[st.session_state.stock_data['Quantité'] < st.session_state.stock_data['Seuil_min']])}")

# ==================== TABLEAU DE BORD ====================
if menu == "🏠 Tableau de bord":
    st.header("📊 Tableau de bord - Vue d'ensemble")
    
    # KPIs principaux
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        with st.container():
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("📦 Stock total", f"{st.session_state.stock_data['Quantité'].sum():,} unités", 
                     f"+{random.randint(1,5)}%")
            st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        with st.container():
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("⚡ Conso. énergie", f"{st.session_state.energie_data['Consommation_kWh'].mean():.0f} kWh/jour",
                     f"{random.randint(-3,3)}%")
            st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        with st.container():
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("✅ Taux qualité", f"{st.session_state.qualite_data['Taux_conformite'].mean():.1f}%",
                     f"+{random.randint(0,2)}%")
            st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        with st.container():
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("📐 Occupation", f"{random.randint(75, 90)}%",
                     f"{random.randint(-2,5)}%")
            st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Graphiques
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Évolution du stock par catégorie")
        stock_cat = st.session_state.stock_data.groupby('Catégorie')['Quantité'].sum().reset_index()
        fig = px.pie(stock_cat, values='Quantité', names='Catégorie', 
                     title="Répartition du stock", hole=0.4)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("⚡ Consommation énergétique")
        conso_hebdo = st.session_state.energie_data.resample('W', on='Date')['Consommation_kWh'].mean().reset_index()
        fig = px.line(conso_hebdo, x='Date', y='Consommation_kWh', 
                     title="Consommation moyenne hebdomadaire")
        st.plotly_chart(fig, use_container_width=True)
    
    # Alertes
    st.markdown("---")
    st.subheader("🔔 Alertes et notifications")
    
    alerts = []
    
    # Alertes stock
    stock_faible = st.session_state.stock_data[st.session_state.stock_data['Quantité'] < st.session_state.stock_data['Seuil_min']]
    for _, row in stock_faible.iterrows():
        alerts.append(("⚠️", f"Stock faible: {row['Produit']} ({row['Quantité']} unités)"))
    
    # Alertes ISO
    if st.session_state.qualite_data['Taux_conformite'].iloc[-1] < 95:
        alerts.append(("⚠️", "Taux de conformité sous l'objectif ISO 90001"))
    
    if st.session_state.energie_data['Consommation_kWh'].iloc[-5:].mean() > 500:
        alerts.append(("⚠️", "Consommation énergétique anormalement élevée"))
    
    if not alerts:
        st.success("✅ Aucune alerte - Tous les indicateurs sont verts")
    else:
        for icon, msg in alerts[:5]:
            st.warning(f"{icon} {msg}")

# ==================== GESTION DE STOCK ====================
elif menu == "📦 Gestion de stock":
    st.header("📦 Gestion de stock")
    
    # Onglets
    tab1, tab2, tab3, tab4 = st.tabs(["📋 État du stock", "➕ Ajouter/Modifier", "📦 Mouvements", "📊 Analyse stock"])
    
    with tab1:
        st.subheader("État actuel du stock")
        
        # Filtres
        col1, col2, col3 = st.columns(3)
        with col1:
            categorie_filter = st.selectbox("Filtrer par catégorie", 
                                           ["Toutes"] + list(st.session_state.stock_data['Catégorie'].unique()))
        with col2:
            seuil_filter = st.slider("Seuil d'alerte", 0, 500, 100)
        with col3:
            search = st.text_input("🔍 Rechercher un produit")
        
        # Application des filtres
        df_filtered = st.session_state.stock_data.copy()
        if categorie_filter != "Toutes":
            df_filtered = df_filtered[df_filtered['Catégorie'] == categorie_filter]
        if search:
            df_filtered = df_filtered[df_filtered['Produit'].str.contains(search, case=False)]
        
        # Coloration conditionnelle
        def color_stock(val):
            if val < 60:
                return 'background-color: #ffcccc'
            elif val > 300:
                return 'background-color: #ccffcc'
            return ''
        
        styled_df = df_filtered.style.applymap(color_stock, subset=['Quantité'])
        st.dataframe(styled_df, use_container_width=True)
        
        # Statistiques
        col1, col2, col3 = st.columns(3)
        col1.metric("Nombre de références", len(df_filtered))
        col2.metric("Valeur totale du stock", f"{df_filtered['Quantité'].sum() * random.randint(10,50):,} €")
        col3.metric("Taux de rotation", f"{random.randint(60, 95)}%")
    
    with tab2:
        st.subheader("Ajouter un nouveau produit")
        
        with st.form("ajout_produit"):
            col1, col2 = st.columns(2)
            
            with col1:
                nom = st.text_input("Nom du produit")
                categorie = st.selectbox("Catégorie", ["Électronique", "Mécanique", "Emballage", "Autre"])
                quantite = st.number_input("Quantité", min_value=0, value=100)
                
            with col2:
                seuil_min = st.number_input("Seuil minimum", min_value=0, value=50)
                seuil_max = st.number_input("Seuil maximum", min_value=0, value=500)
                emplacement = st.text_input("Emplacement", value="A1")
            
            submitted = st.form_submit_button("Ajouter au stock")
            
            if submitted and nom:
                new_id = f"PRD{len(st.session_state.stock_data)+1:03d}"
                new_row = pd.DataFrame({
                    'ID': [new_id],
                    'Produit': [nom],
                    'Catégorie': [categorie],
                    'Quantité': [quantite],
                    'Seuil_min': [seuil_min],
                    'Seuil_max': [seuil_max],
                    'Emplacement': [emplacement],
                    'Fournisseur': ['Nouveau fournisseur'],
                    'Date_derniere_entree': [datetime.now()]
                })
                st.session_state.stock_data = pd.concat([st.session_state.stock_data, new_row], ignore_index=True)
                st.success(f"✅ Produit {nom} ajouté avec succès!")
    
    with tab3:
        st.subheader("Historique des mouvements")
        
        # Simulation de mouvements
        mouvements = pd.DataFrame({
            'Date': pd.date_range(start='2024-03-01', periods=20, freq='D'),
            'Produit': np.random.choice(st.session_state.stock_data['Produit'], 20),
            'Type': np.random.choice(['Entrée', 'Sortie', 'Transfert'], 20),
            'Quantité': np.random.randint(1, 50, 20),
            'Responsable': np.random.choice(['Dupont', 'Martin', 'Bernard', 'Petit'], 20)
        })
        
        st.dataframe(mouvements, use_container_width=True)
        
        # Graphique des mouvements
        mouvements_count = mouvements['Type'].value_counts()
        fig = px.bar(x=mouvements_count.index, y=mouvements_count.values, 
                     title="Répartition des mouvements")
        st.plotly_chart(fig, use_container_width=True)

# ==================== DIMENSIONNEMENT ====================
elif menu == "📐 Dimensionnement":
    st.header("📐 Dimensionnement et optimisation d'entrepôt")
    
    # Onglets
    tab1, tab2, tab3 = st.tabs(["📏 Calcul capacité", "📊 Optimisation espace", "🔄 Simulation flux"])
    
    with tab1:
        st.subheader("Calcul de la capacité de stockage")
        
        col1, col2 = st.columns(2)
        
        with col1:
            longueur = st.number_input("Longueur de l'entrepôt (m)", min_value=10, max_value=200, value=80)
            largeur = st.number_input("Largeur de l'entrepôt (m)", min_value=10, max_value=100, value=40)
            hauteur = st.number_input("Hauteur sous plafond (m)", min_value=3, max_value=20, value=8)
            
        with col2:
            type_produit = st.selectbox("Type de produits", 
                                       ["Palettes", "Bacs", "Vrac", "Rayonnage léger"])
            densite = st.slider("Densité de stockage (%)", 50, 95, 75)
            hauteur_moy_produit = st.number_input("Hauteur moyenne produit (m)", 0.1, 5.0, 1.5)
        
        # Calculs
        surface_totale = longueur * largeur
        volume_total = surface_totale * hauteur
        nb_niveaux = int(hauteur / hauteur_moy_produit)
        capacite_theorique = (surface_totale * nb_niveaux) * (densite / 100)
        
        # Affichage résultats
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Surface totale", f"{surface_totale:,.0f} m²")
        col2.metric("Volume total", f"{volume_total:,.0f} m³")
        col3.metric("Niveaux possibles", nb_niveaux)
        col4.metric("Capacité théorique", f"{capacite_theorique:,.0f} unités")
        
        # Visualisation 3D simplifiée
        fig = go.Figure()
        
        # Création d'un cube 3D
        x = [0, longueur, longueur, 0, 0, longueur, longueur, 0]
        y = [0, 0, largeur, largeur, 0, 0, largeur, largeur]
        z = [0, 0, 0, 0, hauteur, hauteur, hauteur, hauteur]
        
        fig.add_trace(go.Mesh3d(
            x=x, y=y, z=z,
            color='lightblue',
            opacity=0.5,
            name='Entrepôt'
        ))
        
        fig.update_layout(
            title="Visualisation 3D de l'entrepôt",
            scene=dict(
                xaxis_title="Longueur (m)",
                yaxis_title="Largeur (m)",
                zaxis_title="Hauteur (m)"
            ),
            width=800,
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.subheader("Optimisation de l'espace")
        
        col1, col2 = st.columns(2)
        
        with col1:
            type_rayonnage = st.selectbox("Type de rayonnage", 
                                         ["Classique", "Navette", "Mobile", "Cantilever"])
            largeur_allee = st.number_input("Largeur des allées (m)", 0.8, 5.0, 3.0)
            profondeur_rayonnage = st.number_input("Profondeur rayonnage (m)", 0.5, 2.0, 1.2)
            
        with col2:
            nb_allées = st.number_input("Nombre d'allées", 1, 20, 5)
            hauteur_rayonnage = st.number_input("Hauteur rayonnage (m)", 2.0, 15.0, 6.0)
            espace_securite = st.number_input("Espace de sécurité (%)", 5, 30, 15)
        
        if st.button("Calculer l'optimisation", use_container_width=True):
            surface_utile = surface_totale * (1 - espace_securite/100)
            surface_rayonnage = (largeur_allee + profondeur_rayonnage * 2) * longueur * nb_allées
            capacite_optimisee = (surface_utile / surface_rayonnage) * 1000
            
            st.success("✅ Analyse d'optimisation terminée!")
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Surface utile", f"{surface_utile:,.0f} m²")
            col2.metric("Gain potentiel", f"{random.randint(15, 30)}%")
            col3.metric("Capacité optimisée", f"{capacite_optimisee:,.0f} unités")
    
    with tab3:
        st.subheader("Simulation des flux")
        
        col1, col2 = st.columns(2)
        
        with col1:
            entrees_jour = st.number_input("Entrées par jour", 0, 1000, 150)
            sorties_jour = st.number_input("Sorties par jour", 0, 1000, 120)
            temps_preparation = st.number_input("Temps préparation (min)", 5, 120, 15)
            
        with col2:
            nb_operateurs = st.number_input("Nombre d'opérateurs", 1, 50, 8)
            nb_quais = st.number_input("Nombre de quais", 1, 20, 4)
            heures_ouverture = st.number_input("Heures d'ouverture/jour", 8, 24, 10)
        
        if st.button("Lancer la simulation", use_container_width=True):
            capacite_horaire = nb_operateurs * (60 / temps_preparation)
            capacite_jour = capacite_horaire * heures_ouverture
            taux_occupation = ((entrees_jour + sorties_jour) / capacite_jour) * 100
            
            # Graphique de simulation
            heures = list(range(heures_ouverture))
            flux_horaire = [random.randint(10, 30) for _ in heures]
            
            fig = px.bar(x=heures, y=flux_horaire, 
                        title="Simulation du flux horaire",
                        labels={'x': 'Heure', 'y': 'Nombre d\'opérations'})
            st.plotly_chart(fig, use_container_width=True)
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Capacité journalière", f"{capacite_jour:.0f} opérations")
            col2.metric("Taux d'occupation", f"{taux_occupation:.1f}%")
            col3.metric("Temps d'attente moyen", f"{random.randint(5, 30)} min")

# ==================== ISO 50001 - ÉNERGIE ====================
elif menu == "⚡ ISO 50001 - Énergie":
    st.header("⚡ ISO 50001 - Management de l'énergie")
    
    # Badge de conformité
    st.markdown('<p class="iso-badge">✓ Conforme ISO 50001:2018</p>', unsafe_allow_html=True)
    
    # Onglets
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Performance énergétique", "📈 Indicateurs", "🔧 Actions", "📋 Audits"])
    
    with tab1:
        st.subheader("Performance énergétique")
        
        # Graphique consommation
        fig = px.line(st.session_state.energie_data, x='Date', y='Consommation_kWh',
                     title="Consommation énergétique quotidienne")
        st.plotly_chart(fig, use_container_width=True)
        
        # Métriques par zone
        conso_zone = st.session_state.energie_data.groupby('Zone')['Consommation_kWh'].mean().reset_index()
        fig = px.bar(conso_zone, x='Zone', y='Consommation_kWh',
                    title="Consommation moyenne par zone")
        st.plotly_chart(fig, use_container_width=True)
        
        # KPIs énergétiques
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Consommation totale", f"{st.session_state.energie_data['Consommation_kWh'].sum():,.0f} kWh")
        col2.metric("Moyenne journalière", f"{st.session_state.energie_data['Consommation_kWh'].mean():.0f} kWh")
        col3.metric("Pic de consommation", f"{st.session_state.energie_data['Consommation_kWh'].max():.0f} kWh")
        col4.metric("Objectif 2024", "-8%", "-2%")
    
    with tab2:
        st.subheader("Indicateurs de performance énergétique (IPÉ)")
        
        # Calcul des indicateurs
        indicateurs = pd.DataFrame({
            'Indicateur': ['Intensité énergétique', 'Facteur de charge', 'Efficacité éclairage', 
                          'COP CVC', 'Ratio stock/énergie'],
            'Valeur': ['85 kWh/m²', '0.75', '92%', '3.2', '15.4 unités/kWh'],
            'Cible': ['80 kWh/m²', '0.80', '90%', '3.5', '18 unités/kWh'],
            'Tendance': ['🔻', '🔺', '✅', '🔺', '🔻'],
            'Statut': ['À améliorer', 'Bon', 'Excellent', 'Bon', 'À surveiller']
        })
        
        st.dataframe(indicateurs, use_container_width=True)
        
        # Analyse de régression
        st.subheader("Corrélation température/consommation")
        fig = px.scatter(st.session_state.energie_data, x='Temperature_ext', y='Consommation_kWh',
                        trendline="ols", title="Impact de la température sur la consommation")
        st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.subheader("Plan d'actions d'efficacité énergétique")
        
        actions = pd.DataFrame({
            'Action': ['Installation LED', 'Isolation toiture', 'Optimisation CVC', 
                      'Panneaux solaires', 'Variateurs de vitesse'],
            'Économie estimée': ['15%', '10%', '20%', '25%', '12%'],
            'Investissement': ['15k€', '25k€', '30k€', '50k€', '18k€'],
            'ROI (ans)': ['1.5', '2.5', '2.0', '3.5', '2.0'],
            'Statut': ['En cours', 'Planifié', 'Terminé', 'À étudier', 'En cours'],
            'Priorité': ['Haute', 'Moyenne', 'Haute', 'Basse', 'Moyenne']
        })
        
        st.dataframe(actions, use_container_width=True)
        
        # Formulaire d'ajout d'action
        with st.expander("➕ Proposer une nouvelle action"):
            with st.form("nouvelle_action"):
                col1, col2 = st.columns(2)
                with col1:
                    nom_action = st.text_input("Nom de l'action")
                    economie = st.number_input("Économie estimée (%)", 0, 50, 10)
                with col2:
                    invest = st.number_input("Investissement (k€)", 0, 500, 20)
                    priorite = st.selectbox("Priorité", ["Haute", "Moyenne", "Basse"])
                
                if st.form_submit_button("Soumettre"):
                    st.success("✅ Action proposée avec succès!")
    
    with tab4:
        st.subheader("Historique des audits énergétiques")
        
        audits = pd.DataFrame({
            'Date': ['2024-01-15', '2023-10-10', '2023-07-05', '2023-04-12'],
            'Auditeur': ['Bureau Veritas', 'SGS', 'DNV', 'Intertek'],
            'Score': [92, 88, 85, 90],
            'Non-conformités': [2, 3, 4, 2],
            'Statut': ['Conforme', 'Conforme', 'Conforme', 'Conforme']
        })
        
        st.dataframe(audits, use_container_width=True)
        
        # Graphique d'évolution
        fig = px.line(audits, x='Date', y='Score', title="Évolution des scores d'audit")
        st.plotly_chart(fig, use_container_width=True)

# ==================== ISO 90001 - QUALITÉ ====================
elif menu == "✅ ISO 90001 - Qualité":
    st.header("✅ ISO 90001 - Management de la qualité")
    
    st.markdown('<p class="iso-badge">✓ Conforme ISO 90001:2015</p>', unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Indicateurs qualité", "📝 Non-conformités", "🔧 Actions correctives", "📋 Documents"])
    
    with tab1:
        st.subheader("Indicateurs de performance qualité")
        
        # Graphiques
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.line(st.session_state.qualite_data, x='Date', y='Taux_conformite',
                         title="Évolution du taux de conformité")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.bar(st.session_state.qualite_data, x='Date', y='Non_conformites',
                        title="Non-conformités par période")
            st.plotly_chart(fig, use_container_width=True)
        
        # Métriques
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Taux conformité moyen", f"{st.session_state.qualite_data['Taux_conformite'].mean():.1f}%")
        col2.metric("Objectif 2024", "98%", "+0.5%")
        col3.metric("Indice CAPA", "92%", "+3%")
        col4.metric("Satisfaction client", "4.7/5", "+0.2")
    
    with tab2:
        st.subheader("Gestion des non-conformités")
        
        nc_data = pd.DataFrame({
            'ID': ['NC001', 'NC002', 'NC003', 'NC004', 'NC005'],
            'Date': ['2024-03-01', '2024-03-05', '2024-03-10', '2024-03-12', '2024-03-15'],
            'Type': ['Documentation', 'Produit', 'Processus', 'Produit', 'Service'],
            'Description': ['Manque procédure', 'Défaut emballage', 'Délai dépassé', 'Mauvaise étiquette', 'Retard livraison'],
            'Responsable': ['Dupont', 'Martin', 'Bernard', 'Petit', 'Durand'],
            'Statut': ['En cours', 'Résolu', 'En cours', 'Résolu', 'Nouveau'],
            'Échéance': ['2024-03-20', '2024-03-15', '2024-03-25', '2024-03-18', '2024-03-30']
        })
        
        st.dataframe(nc_data, use_container_width=True)
        
        # Analyse par type
        nc_type = nc_data['Type'].value_counts()
        fig = px.pie(values=nc_type.values, names=nc_type.index, title="Répartition des non-conformités")
        st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.subheader("Actions correctives et préventives")
        
        capa_data = pd.DataFrame({
            'Action': ['Mise à jour procédure', 'Formation personnel', 'Nouveau contrôle', 
                      'Maintenance préventive', 'Audit interne'],
            'Type': ['Corrective', 'Préventive', 'Corrective', 'Préventive', 'Préventive'],
            'Responsable': ['M. Jean', 'Mme Marie', 'M. Pierre', 'M. Paul', 'Mme Sophie'],
            'Début': ['2024-03-01', '2024-03-10', '2024-03-05', '2024-03-15', '2024-03-20'],
            'Fin prévue': ['2024-03-30', '2024-03-25', '2024-03-20', '2024-04-15', '2024-03-28'],
            'Statut': ['En cours', 'Planifié', 'Terminé', 'En cours', 'Planifié']
        })
        
        st.dataframe(capa_data, use_container_width=True)
        
        # Ajout d'action
        with st.expander("➕ Nouvelle action"):
            with st.form("action_form"):
                col1, col2 = st.columns(2)
                with col1:
                    action_nom = st.text_input("Titre de l'action")
                    action_type = st.selectbox("Type", ["Corrective", "Préventive"])
                with col2:
                    responsable = st.text_input("Responsable")
                    echeance = st.date_input("Date d'échéance")
                
                description = st.text_area("Description")
                
                if st.form_submit_button("Créer l'action"):
                    st.success("✅ Action créée avec succès!")
    
    with tab4:
        st.subheader("Documents qualité")
        
        documents = pd.DataFrame({
            'Document': ['Manuel qualité', 'Procédures', 'Instructions', 'Enregistrements', 'Politique qualité'],
            'Version': ['2.1', '3.0', '1.5', '2.0', '1.2'],
            'Date révision': ['2024-01-15', '2024-02-01', '2024-01-20', '2024-02-10', '2024-01-05'],
            'Responsable': ['Dupont', 'Martin', 'Bernard', 'Petit', 'Durand'],
            'Statut': ['Approuvé', 'En révision', 'Approuvé', 'Validé', 'Approuvé']
        })
        
        st.dataframe(documents, use_container_width=True)
        
        # Téléchargement
        st.subheader("Télécharger les documents")
        col1, col2 = st.columns(2)
        with col1:
            st.download_button("📄 Manuel qualité", "Contenu...", "manuel_qualite.pdf")
            st.download_button("📋 Procédures", "Contenu...", "procedures.pdf")
        with col2:
            st.download_button("📊 Formulaire audit", "Contenu...", "audit_form.pdf")
            st.download_button("📈 Rapport qualité", "Contenu...", "rapport_qualite.pdf")

# ==================== RAPPORTS ====================
elif menu == "📊 Rapports & Analyses":
    st.header("📊 Rapports et analyses")
    
    # Sélection du type de rapport
    col1, col2 = st.columns(2)
    
    with col1:
        type_rapport = st.selectbox(
            "Type de rapport",
            ["Rapport de performance", "Rapport de stock", "Rapport énergétique", 
             "Rapport qualité", "Rapport de conformité ISO", "Rapport personnalisé"]
        )
    
    with col2:
        periode = st.selectbox(
            "Période",
            ["Aujourd'hui", "Cette semaine", "Ce mois", "Ce trimestre", "Cette année", "Personnalisée"]
        )
    
    # Dates si période personnalisée
    if periode == "Personnalisée":
        col1, col2 = st.columns(2)
        with col1:
            date_debut = st.date_input("Date début", datetime.now() - timedelta(days=30))
        with col2:
            date_fin = st.date_input("Date fin", datetime.now())
    
    # Génération du rapport
    if st.button("📄 Générer le rapport", use_container_width=True):
        with st.spinner("Génération du rapport en cours..."):
            import time
            time.sleep(2)
        
        st.success("✅ Rapport généré avec succès!")
        
        # Aperçu du rapport
        st.subheader("Aperçu du rapport")
        
        if type_rapport == "Rapport de performance":
            # Graphiques de performance
            col1, col2 = st.columns(2)
            
            with col1:
                fig = px.line(x=['Sem1', 'Sem2', 'Sem3', 'Sem4'], 
                             y=[85, 88, 92, 89],
                             title="Performance globale")
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                fig = px.bar(x=['Stock', 'Énergie', 'Qualité', 'Service'], 
                            y=[94, 88, 96, 91],
                            title="Indicateurs par domaine")
                st.plotly_chart(fig, use_container_width=True)
        
        elif type_rapport == "Rapport de stock":
            # Analyse ABC
            abc_data = pd.DataFrame({
                'Catégorie': ['A (Valeur élevée)', 'B (Valeur moyenne)', 'C (Valeur faible)'],
                'Nombre produits': [15, 35, 50],
                'Valeur stock': [450000, 220000, 80000],
                'Rotation': [12, 6, 2]
            })
            st.dataframe(abc_data, use_container_width=True)
        
        # Boutons d'export
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.download_button("📥 Télécharger PDF", "Contenu PDF", "rapport.pdf")
        with col2:
            st.download_button("📊 Télécharger Excel", "Contenu Excel", "rapport.xlsx")
        with col3:
            st.download_button("📧 Envoyer par email", "Contenu email", "rapport.eml")

# ==================== PARAMÈTRES ====================
else:  # Paramètres
    st.header("⚙️ Paramètres de l'application")
    
    tab1, tab2, tab3 = st.tabs(["👤 Utilisateur", "🔔 Notifications", "📊 Configuration"])
    
    with tab1:
        st.subheader("Profil utilisateur")
        
        col1, col2 = st.columns(2)
        with col1:
            st.text_input("Nom", value="Admin Entrepôt")
            st.text_input("Email", value="admin@entrepot.com")
            st.text_input("Fonction", value="Responsable d'exploitation")
        
        with col2:
            st.selectbox("Langue", ["Français", "English", "Español"])
            st.selectbox("Thème", ["Clair", "Sombre", "Système"])
            st.selectbox("Fuseau horaire", ["Europe/Paris", "UTC", "America/New_York"])
        
        if st.button("Mettre à jour le profil"):
            st.success("✅ Profil mis à jour!")
    
    with tab2:
        st.subheader("Configuration des notifications")
        
        st.checkbox("Alertes stock faible", value=True)
        st.checkbox("Alertes consommation énergétique", value=True)
        st.checkbox("Alertes non-conformités qualité", value=True)
        st.checkbox("Rapports hebdomadaires", value=False)
        st.checkbox("Rappels d'audit", value=True)
        
        st.number_input("Seuil d'alerte stock (%)", 10, 50, 20)
        st.time_input("Heure d'envoi des rapports", value=datetime.now().time())
    
    with tab3:
        st.subheader("Configuration de l'application")
        
        col1, col2 = st.columns(2)
        with col1:
            st.number_input("Rafraîchissement auto (secondes)", 30, 3600, 300)
            st.selectbox("Format date", ["DD/MM/YYYY", "MM/DD/YYYY", "YYYY-MM-DD"])
        
        with col2:
            st.selectbox("Devise", ["€", "$", "£"])
            st.selectbox("Unité de mesure", ["Métrique", "Impérial"])
        
        st.slider("Niveau de détail des rapports", 1, 5, 3)
        
        if st.button("Sauvegarder la configuration"):
            st.success("✅ Configuration sauvegardée!")

# Pied de page
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: gray; padding: 1rem;'>
        <p>🏭 Gestion d'Entrepôt Intelligente - Conforme ISO 50001 & 90001</p>
        <p>Version 1.0.0 | © 2024 Tous droits réservés</p>
    </div>
    """,
    unsafe_allow_html=True
)
