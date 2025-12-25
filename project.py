import streamlit as st
import pandas as pd
import plotly.express as px

# =========================
# Page Config
# =========================
st.set_page_config(
    page_title="Supreme Court Dashboard",
    layout="wide",
    page_icon="⚖️"
)

st.title("⚖️ Supreme Court Analytics Dashboard")
st.caption("Interactive analysis of Supreme Court cases")

# =========================
# Dark Mode Styling
# =========================
st.markdown(
    """
    <style>
    /* Page background */
    .stApp {
        background-color: #111111;
        color: #FFFFFF;
    }
    /* Sidebar background */
    .css-1d391kg {  
        background-color: #1E1E1E;
    }
    /* Headings and text */
    h1, h2, h3, h4, h5, h6, .stMarkdown p, .stMetric label {
        color: #FFFFFF;
    }
    </style>
    """, unsafe_allow_html=True
)

# =========================
# Load Data
# =========================
df = pd.read_csv(r"D:\Data science\Mid-Project\database.csv")
df.columns = df.columns.str.strip()  # Remove spaces

# Fix date columns
df['date_decision'] = pd.to_datetime(df['date_decision'], errors='coerce')
df['date_argument'] = pd.to_datetime(df['date_argument'], errors='coerce')

# =========================
# Sidebar Filters
# =========================


# =========================
# Tabs
# =========================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Overview",
    "👩‍⚖️ Chief Justices & Jurisdictions",
    "📚 Issue & Law Analysis",
    "🏛 Court Outcomes",
    "🗺 States & Case Profiles"
])

# =========================
# TAB 1 — OVERVIEW
# =========================
with tab1:
    st.subheader("Overview")

    # Sidebar filters specific to this tab
    st.sidebar.subheader("📊 Overview Filters")
    years = sorted(df['date_decision'].dt.year.dropna().unique())
    year_f = st.sidebar.multiselect("Select Year", years, default=years)

    # Filter dataframe by selected years
    df_f_tab1 = df[df['date_decision'].dt.year.isin(year_f)].copy()

    # Columns for metrics
    c1, s1, c2, s2, c3 = st.columns([2,0.3,2,0.3,2])
    c1.metric("Total Cases", f"{len(df_f_tab1):,}")
    c2.metric("Jurisdictions", f"{df_f_tab1['jurisdiction'].nunique():,}")
    c3.metric("Issue Areas", f"{df_f_tab1['issue_area'].nunique():,}")

    st.markdown("---")

    # Cases per year
    cases_per_year = df_f_tab1['date_decision'].dt.year.value_counts().sort_index().reset_index()
    cases_per_year.columns = ['Year', 'Count']

    # Line plot
    fig = px.line(
        cases_per_year,
        x='Year',
        y='Count',
        markers=True,
        color_discrete_sequence=['#4DA3FF'],
        title="Number of Cases per Year"
    )
    fig.update_layout(
        template='plotly_dark',         # Dark template
        plot_bgcolor='#111111',         # Dark plot area
        paper_bgcolor='#111111',        # Dark background around plot
        font_color='white',             # Axis titles and labels in white
        showlegend=False
    )

    st.plotly_chart(fig, use_container_width=True)



# =========================
# TAB 2 — CHIEF JUSTICES & JURISDICTIONS
# =========================
with tab2:
    st.subheader("Chief Justices & Jurisdictions")

    # =========================
    # Sidebar Filter for this tab
    # =========================
    st.sidebar.subheader("👩‍⚖️ Jurisdiction Filters")

    # Map numeric values to names
    jurisdiction_map = {1: 'Federal', 2: 'State', 9: 'Local'}
    if 'jurisdiction' in df.columns:
        df['jurisdiction'] = df['jurisdiction'].map(jurisdiction_map).fillna('Other')

    # Sidebar multiselect
    jurisdictions = sorted(df['jurisdiction'].dropna().unique())
    jur_f = st.sidebar.multiselect("Select Jurisdiction", jurisdictions, default=jurisdictions)

    # Filter dataframe for this tab
    df_f_tab2 = df[df['jurisdiction'].isin(jur_f)].copy()

    # =========================
    # Layout for charts
    # =========================
    col1, sp, col2 = st.columns([4,0.4,6])

    # Chief Justices Chart
    if 'chief_justice' in df_f_tab2.columns:
        cj = df_f_tab2['chief_justice'].value_counts().reset_index()
        cj.columns = ['Chief Justice', 'Count']
        with col1:
            fig = px.bar(
                cj,
                x='Chief Justice',
                y='Count',
                text='Count',
                color='Chief Justice',
                 color_discrete_sequence=['#4DA3FF','#7EE787','#F1C40F','#A371F7','#E5533D'],
                title="Cases per Chief Justice"
            )
            fig.update_layout(
                template='plotly_dark',
                plot_bgcolor='#111111',
                paper_bgcolor='#111111',
                font_color='white',
                xaxis_tickangle=-45,
                showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True)

    # Jurisdictions Chart
    if 'jurisdiction' in df_f_tab2.columns:
        jur = df_f_tab2['jurisdiction'].value_counts().reset_index()
        jur.columns = ['Jurisdiction', 'Count']
        with col2:
            fig = px.bar(
                jur,
                x='Jurisdiction',
                y='Count',
                color='Jurisdiction',
                text='Count',
                color_discrete_sequence=['#4DA3FF','#7EE787','#F1C40F','#A371F7','#E5533D'],
                title="Cases by Jurisdiction"
            )
            fig.update_layout(
                template='plotly_dark',
                plot_bgcolor='#111111',
                paper_bgcolor='#111111',
                font_color='white',
                xaxis_tickangle=-45,
                showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True)



# =========================
# TAB 3 — ISSUE & LAW ANALYSIS
# =========================
with tab3:
    st.subheader("Issue & Law Analysis")
    col1, sp, col2 = st.columns([5,0.4,5])

    # =========================
    # Sidebar Filter Header
    # =========================
    st.sidebar.subheader("📚 Issue & Law Type")

    # =========================
    # Map Issue Area
    # =========================
    if 'issue_area' in df.columns:
        issue_area_map = {
            1: "Workers’ rights",
            2: "Tax disputes",
            3: "Patents",
            6: "Military",
            8: "Attorney’s fees",
            9: "Bankruptcy"
        }
        df['issue_area'] = df['issue_area'].map(issue_area_map).fillna("Other")

        # Sidebar filter for issue area
        issue_options = sorted(df['issue_area'].dropna().unique())
        issue_f = st.sidebar.multiselect("Select Issue Area", issue_options, default=issue_options)

    # =========================
    # Map Law Type
    # =========================
    if 'law_type' in df.columns:
        df['law_type'] = df['law_type'].astype('Int64')
        law_type_map = {
            1: "Criminal",
            2: "Civil",
            3: "Administrative",
            4: "Economic",
            5: "Commercial",
            6: "Child",
            8: "Family"
        }
        df['law_type'] = df['law_type'].map(law_type_map).fillna("Other")

        # Sidebar filter for law type
        law_options = sorted(df['law_type'].dropna().unique())
        law_f = st.sidebar.multiselect("Select Law Type", law_options, default=law_options)

    # =========================
    # Filter dataframe using selected issue and law types
    # =========================
    df_f = df[
        (df['issue_area'].isin(issue_f)) &
        (df['law_type'].isin(law_f))
    ].copy()

    # =========================
    # Issue Area Chart
    # =========================
    issue_counts = df_f['issue_area'].value_counts().reset_index()
    issue_counts.columns = ['Issue','Count']
    with col1:
        fig = px.bar(
            issue_counts,
            x='Issue',
            y='Count',
            text='Count',
            color='Issue',
            color_discrete_sequence=['#4DA3FF','#7EE787','#F1C40F','#A371F7','#E5533D'],
            title="Cases by Issue Area"
        )
        fig.update_layout(
            template='plotly_dark',
            plot_bgcolor='#111111',
            paper_bgcolor='#111111',
            font_color='white',
            xaxis_tickangle=-45,
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)

    # =========================
    # Law Type Chart
    # =========================
    law_counts = df_f['law_type'].value_counts().reset_index()
    law_counts.columns = ['Law Type','Count']
    with col2:
        fig = px.bar(
            law_counts,
            x='Law Type',
            y='Count',
            text='Count',
            color='Law Type',
            color_discrete_sequence=['#4DA3FF','#7EE787','#F1C40F','#A371F7','#E5533D'],
            title="Cases by Law Type"
        )
        fig.update_layout(
            template='plotly_dark',
            plot_bgcolor='#111111',
            paper_bgcolor='#111111',
            font_color='white',
            xaxis_tickangle=-45,
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # =========================
    # Correlation: Precedent Alteration vs Decision Direction
    # =========================
    if {'precedent_alteration','decision_direction'}.issubset(df_f.columns):
        corr = df_f[['precedent_alteration','decision_direction']].corr()
        fig = px.imshow(
            corr,
            text_auto=True,
            color_continuous_scale=['#4DA3FF','#7EE787','#F1C40F','#A371F7','#E5533D'],
            title="Correlation: Precedent Alteration vs Decision Direction"
        )
        fig.update_layout(
            template='plotly_dark',
            plot_bgcolor='#111111',
            paper_bgcolor='#111111',
            font_color='white'
        )
        st.plotly_chart(fig, use_container_width=True)



with tab4:
    st.subheader("Court Outcomes")

    # -------------------------
    # Layout: two columns
    # -------------------------
    col1, sp, col2 = st.columns([6, 0.4, 4])

    # -------------------------
    # Party Winning Rates
    # -------------------------
    if 'party_winning' in df_f.columns:
        party_winning_map = {1: "Petitioner", 0: "Respondent", 2: "Have not finished"}
        df_f['party_winning'] = df_f['party_winning'].map(party_winning_map).fillna("Unknown")

        party_counts = df_f['party_winning'].value_counts().reset_index()
        party_counts.columns = ['Party', 'Count']

        with col1:
            fig = px.bar(
                party_counts,
                x='Party',
                y='Count',
                color='Party',
                text='Count',
                title='Party Winning Rates',
                color_discrete_sequence=['#4DA3FF', '#7EE787', '#F1C40F', '#A371F7', '#E5533D']
            )
            fig.update_layout(
                template='plotly_dark',
                plot_bgcolor='#111111',
                paper_bgcolor='#111111',
                font_color='white',
                xaxis=dict(title='Party', tickangle=-45, showgrid=False),
                yaxis=dict(title='Number of Cases', gridcolor='#30363D'),
                showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True)


    # -------------------------
    # Unconstitutional Rulings
    # -------------------------
    if 'declaration_unconstitutionality' in df_f.columns:
        declaration_map = {
            1: "Yes",
            2: "No",
            3: "Have not finished",
            4: "Unknown"
        }
        df_f['declaration_unconstitutionality'] = df_f['declaration_unconstitutionality'].map(declaration_map).fillna("Unknown")

        un_counts = df_f['declaration_unconstitutionality'].value_counts().reset_index()
        un_counts.columns = ['Declaration', 'Count']
        with col2:
            fig = px.bar(
                un_counts,
                x='Declaration',
                y='Count',
                color='Declaration',
                text='Count',
                title='Unconstitutional Rulings',
                color_discrete_map={
                    'Yes': '#4DA3FF',
                    'No':'#E74C3C',
                    'Have not finished': '#7EE787',
                    'Unknown': '#A371F7'
                }
            )
            fig.update_layout(
                template='plotly_dark',
                plot_bgcolor='#111111',
                paper_bgcolor='#111111',
                font_color='white',
                xaxis_tickangle=-45,
                showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # -------------------------
    # Heatmap: Lower Court vs Supreme Court (at the end)
    # -------------------------
    lower_court_disposition_map = {
        0: "Affirmed",
        1: "Reversed",
        2: "Modified",
        3: "Vacated",
        4: "Other"
    }

    case_disposition_map = {
        1: "Affirmed",
        2: "Reversed",
        3: "Vacated",
        4: "Remanded",
        5: "Other"
    }

    if 'lower_court_disposition' in df_f.columns:
        df_f['lower_court_disposition'] = df_f['lower_court_disposition'].map(lower_court_disposition_map).fillna("Unknown")
    if 'case_disposition' in df_f.columns:
        df_f['case_disposition'] = df_f['case_disposition'].map(case_disposition_map).fillna("Unknown")

    if {'lower_court_disposition', 'case_disposition'}.issubset(df_f.columns):
        pivot_table = df_f.groupby(
            ['lower_court_disposition', 'case_disposition']
        ).size().unstack(fill_value=0)

        fig = px.imshow(
            pivot_table,
            text_auto=True,
            color_continuous_scale=['#D0E6FF', '#4DA3FF', '#1A73E8'],
            title="Lower Court vs Supreme Court Disposition",
            labels=dict(x="Supreme Court Disposition", y="Lower Court Disposition", color="Count")
        )
        fig.update_layout(
            template='plotly_dark',
            plot_bgcolor='#111111',
            paper_bgcolor='#111111',
            font=dict(color='white')
        )
        st.plotly_chart(fig, use_container_width=True)




# =========================
# TAB 5 — STATES & CASE PROFILES
# =========================
with tab5:
    st.subheader("States & Case Profiles")
    col1, sp, col2 = st.columns([5,0.4,5])

    # --------------------------------
    # State Mapping (apply BEFORE charts)
    # --------------------------------
    petitioner_state_map = {
        6: "New York",
        1: "California",
        60: "Texas",
        0: "Alaska",
        51: "Arizona",
        2: "New Jersey",
        39: "Georgia",
        27: "Washington"
    }

    respondent_state_map = {
        6: "New York",
        1: "California",
        60: "Texas",
        0: "Alaska",
        51: "Arizona",
        2: "New Jersey",
        39: "Georgia",
        27: "Washington"
    }

    if 'petitioner_state' in df_f.columns:
        df_f['petitioner_state'] = df_f['petitioner_state'].map(petitioner_state_map).fillna("Other")

    if 'respondent_state' in df_f.columns:
        df_f['respondent_state'] = df_f['respondent_state'].map(respondent_state_map).fillna("Other")

    # -------------------------
    # Petitioner States
    # -------------------------
    if 'petitioner_state' in df_f.columns:

        petitioner_state_clean = df_f['petitioner_state'].astype(str).str.strip()
        petitioner_state_clean = petitioner_state_clean[petitioner_state_clean.str.lower() != 'other']

        pet_counts = petitioner_state_clean.value_counts().reset_index()
        pet_counts.columns = ['petitioner_state', 'Count']

        with col1:
            fig = px.bar(
                pet_counts,
                x='petitioner_state',
                y='Count',
                color='petitioner_state',
                text='Count',
                title="Petitioner States",
                color_discrete_sequence=['#4DA3FF', '#7EE787', '#F1C40F', '#A371F7', '#E5533D']
            )
            fig.update_layout(
                template='plotly_dark',
                plot_bgcolor='#111111',
                paper_bgcolor='#111111',
                font=dict(color='#E6EDF3'),
                xaxis=dict(title='Petitioner State', tickangle=-45, showgrid=False, type='category'),
                yaxis=dict(title='Number of Cases', gridcolor='#30363D'),
                showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True)

    # -------------------------
    # Respondent States
    # -------------------------
    if 'respondent_state' in df_f.columns:

        respondent_state_clean = df_f['respondent_state'].astype(str).str.strip()
        respondent_state_clean = respondent_state_clean[respondent_state_clean.str.lower() != 'other']

        resp_counts = respondent_state_clean.value_counts().reset_index()
        resp_counts.columns = ['State', 'Count']

        with col2:
            fig = px.bar(
                resp_counts,
                x='State',
                y='Count',
                color='State',
                text='Count',
                title="Respondent States",
                color_discrete_sequence=['#4DA3FF', '#7EE787', '#F1C40F', '#A371F7', '#E5533D']
            )
            fig.update_layout(
                template='plotly_dark',
                plot_bgcolor='#111111',
                paper_bgcolor='#111111',
                font=dict(color='#E6EDF3'),
                xaxis=dict(title='Respondent State', tickangle=-45, showgrid=False, type='category'),
                yaxis=dict(title='Number of Cases', gridcolor='#30363D'),
                showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # -------------------------
    # Top Case Names
    # -------------------------
    if 'case_name' in df_f.columns:
        top = df_f['case_name'].value_counts().head(5).reset_index()
        top.columns = ['Case Name','Count']
        top['Short'] = top['Case Name'].str.slice(0,25) + '...'

        fig = px.bar(
            top,
            x='Short',
            y='Count',
            text='Count',
            color='Case Name',
            color_discrete_sequence=['#4DA3FF','#7EE787','#F1C40F','#A371F7','#E5533D'],
            title="Top 5 Most Common Case Names"
        )

        fig.update_layout(
            template='plotly_dark',
            plot_bgcolor='#111111',
            paper_bgcolor='#111111',
            font_color='white',
            xaxis_tickangle=-45,
            showlegend=False
        )

        st.plotly_chart(fig, use_container_width=True)
