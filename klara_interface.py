import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from PIL import Image
import base64

# --- Page Configuration ---
# Use a wide layout for a dashboard-style feel
st.set_page_config(
    page_title="IVF Cycle Prediction Report",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# --- Custom CSS for Styling ---
# This function injects custom CSS to style the app, creating card-like containers
# and matching the color scheme from the provided image.
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Create a dummy css file to be used by the function
with open("style.css", "w") as f:
    f.write("""
    /* General body styling */
    body {
        background-color: #F0F2F6;
    }

    /* Main container styling */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        padding-left: 3rem;
        padding-right: 3rem;
    }

    /* Card-like containers for sections */
    .st-emotion-cache-1r6slb0, .st-emotion-cache-1y4p8pa {
        border-radius: 10px;
        padding: 20px !important;
        background-color: white;
        box-shadow: 0 4px 8px 0 rgba(0,0,0,0.1);
        transition: 0.3s;
    }

    .st-emotion-cache-1r6slb0:hover, .st-emotion-cache-1y4p8pa:hover {
        box-shadow: 0 8px 16px 0 rgba(0,0,0,0.2);
    }

    /* Header styling */
    .header {
        background-color: #E83E8C;
        color: white;
        padding: 25px;
        border-radius: 10px;
        margin-bottom: 25px;
        display: flex;
        align-items: center;
        justify-content: flex-start;
    }

    .header h1 {
        font-size: 2.5em;
        margin: 0;
        padding-left: 20px;
    }

    /* Section header styling */
    h2 {
        color: #E83E8C;
        border-bottom: 2px solid #E83E8C;
        padding-bottom: 5px;
        margin-top: 10px;
        margin-bottom: 20px;
    }

    /* Metric label styling */
    .st-emotion-cache-1wivap2 {
        font-size: 1.1em;
        color: #555;
    }

    /* Metric value styling */
    .st-emotion-cache-1g6goys {
        font-size: 1.3em;
        font-weight: bold;
    }

    /* Disclaimer text styling */
    .disclaimer {
        font-size: 0.8em;
        color: #888;
        font-style: italic;
        margin-top: 20px;
    }
    """)

local_css("style.css")

# --- Logo ---
# Using a generic DNA icon as a placeholder for the logo.
# The icon is encoded in base64 to be embedded directly in the HTML.
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Create a dummy SVG file for the logo
with open("logo.svg", "w") as f:
    f.write("""
    <svg xmlns="http://www.w3.org/2000/svg" width="60" height="60" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-git-branch">
        <line x1="6" y1="3" x2="6" y2="15"></line>
        <circle cx="18" cy="6" r="3"></circle>
        <circle cx="6" cy="18" r="3"></circle>
        <path d="M18 9a9 9 0 0 1-9 9"></path>
    </svg>
    """)

logo_base64 = get_base64_of_bin_file("logo.svg")

# --- Header Section ---
st.markdown(
    f"""
    <div class="header">
        <img src="data:image/svg+xml;base64,{logo_base64}" alt="logo">
        <h1>IVF Cycle Oocyte Prediction Report</h1>
    </div>
    """,
    unsafe_allow_html=True
)


# --- Main Layout (2 columns) ---
col1, col2 = st.columns([1, 1.2])


# --- LEFT COLUMN: Clinical Summary ---
with col1:
    st.markdown("<h2>Clinical Summary</h2>", unsafe_allow_html=True)

    # --- Sample Data for Charts ---
    # Generating random data to populate the charts for demonstration purposes.
    np.random.seed(42)
    data = {
        'height': np.random.normal(1.65, 0.1, 20),
        'weight': np.random.normal(60, 5, 20),
        'age': np.random.normal(35, 4, 20),
        'ER/SAD/Cycle': np.random.normal(15, 2, 20),
        'AMH': np.random.normal(15, 3, 20),
        'FSH': np.random.normal(9, 2, 20),
        'E2': np.random.normal(200, 50, 20),
        'LH': np.random.normal(10, 2.5, 20)
    }
    df = pd.DataFrame(data)
    df.columns = ['height', 'weight', 'age', 'ER/SAD/Cycle', 'AMH', 'FSH', 'E2', 'LH']


    # --- Box Plot ---
    st.markdown("<h5>Parameter Comparison (Box Plot)</h5>", unsafe_allow_html=True)
    box_fig = go.Figure()
    for col in df.columns:
        # Changed boxpoints from 'all' to False to hide the individual data points
        box_fig.add_trace(go.Box(y=df[col], name=col, marker_color='#E83E8C', boxpoints=False))

    box_fig.update_layout(
        showlegend=False,
        yaxis_title="Value",
        xaxis_title="Parameter",
        height=350,
        margin=dict(l=20, r=20, t=30, b=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
    )
    st.plotly_chart(box_fig, use_container_width=True)


    # --- Radar Chart ---
    st.markdown("<h5>Parameter Comparison (Radar Chart)</h5>", unsafe_allow_html=True)
    categories = list(df.columns)
    # Using mean values for the radar chart
    values = df.mean().values

    radar_fig = go.Figure()
    radar_fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name='Patient Values',
        line=dict(color='#E83E8C')
    ))

    radar_fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, df.mean().max() * 1.2]),
            bgcolor='rgba(240,240,240,0.8)'
        ),
        showlegend=False,
        height=350,
        margin=dict(l=40, r=40, t=40, b=40),
        paper_bgcolor='rgba(0,0,0,0)',
    )
    st.plotly_chart(radar_fig, use_container_width=True)


# --- RIGHT COLUMN: Patient Details ---
with col2:
    # --- Patient Information Section ---
    st.markdown("<h2>Patient Information</h2>", unsafe_allow_html=True)
    info_cols = st.columns(3)
    with info_cols[0]:
        st.metric(label="Name", value="X Y")
        st.metric(label="Age", value="35 years")
    with info_cols[1]:
        st.metric(label="Postcode", value="3155")
        st.metric(label="Height", value="1.64 m")
    with info_cols[2]:
        st.metric(label="Weight", value="57.9 kg")

    st.write("---") # Visual separator

    # --- Clinical History Section ---
    st.markdown("<h2>Clinical History</h2>", unsafe_allow_html=True)
    history_cols = st.columns(2)
    with history_cols[0]:
        st.metric(label="Number of previous IVF Cycles", value="0")
        st.metric(label="Polycystic Ovary Syndrome", value="No")
        st.metric(label="Fertility Preservation", value="Yes")
        st.metric(label="Unexplained causes of infertility", value="No")
    with history_cols[1]:
        st.metric(label="Endometriosis", value="No")
        st.metric(label="Tubal Factors", value="No")
        st.metric(label="Other Infertility Factors", value="Yes")

    st.write("---")

    # --- Pathology Section ---
    st.markdown("<h2>Pathology</h2>", unsafe_allow_html=True)
    pathology_cols = st.columns(2)
    with pathology_cols[0]:
        st.metric(label="Anti-Mullerian Hormone (AMH)", value="16 ng/mL")
        st.metric(label="Follicle-Stimulating Hormone (FSH)", value="9.6 mIU/mL")
    with pathology_cols[1]:
        st.metric(label="Estradiol (E2)", value="206 pg/mL")
        st.metric(label="Luteinizing Hormone (LH)", value="10.2 mIU/mL")

    st.write("---")

    # --- Summary of Results Section ---
    st.markdown("<h2>Summary of Results</h2>", unsafe_allow_html=True)
    st.info(
        "Based on the input data, the **predicted number of oocytes is 9**.\n\n"
        "The most influential factor in this prediction is **tubal factors**.\n\n"
        "The expected range of error in this prediction is between **-5 and +5 oocytes**."
    )
    st.markdown(
        """
        <div class="disclaimer">
            Disclaimer: The predictions provided by this tool are for educational and counselling purposes only.
            The accuracy of the predictions is subject to variability, and the tool should not be used as a sole
            basis for medical decision-making.
        </div>
        """,
        unsafe_allow_html=True
    )

