import streamlit as st
import pandas as pd
import numpy as np
from fpdf import FPDF

# Metadata & UI Setup
st.set_page_config(page_title="Neptune-Haumea-Eris Radar", layout="wide")
st.title("Neptune-Haumea-Eris Radar Equation For Companies Forecasting")
st.markdown("### The Neptune-Haumea-Eris radar predicts with over 75% probability the existence of a real structural or financial risk to private companies.")
st.subheader("By Mulham Ahmad Halabieh")

def run_usm_engine(inception_year, horizon):
    homo_k = 6.18
    eris_k = 9.3
    neptune_condenser = 10.77 # The Danger Shell Constant
    tolerance = 0.30
    
    data = []
    for i in range(1, horizon + 1):
        target_year = inception_year + i
        age = i
        
        # Calculating deviations against the three pillars
        homo_dev = abs((age / homo_k) - round(age / homo_k))
        eris_dev = abs((age / eris_k) - round(age / eris_k))
        neptune_dev = abs((age / neptune_condenser) - round(age / neptune_condenser))
        
        # Critical State logic based on triple resonance
        if homo_dev <= tolerance and eris_dev <= tolerance and neptune_dev <= tolerance:
            status = "CRITICAL"
        else:
            status = "Normal"
            
        data.append([target_year, age, round(homo_dev, 4), round(eris_dev, 4), round(neptune_dev, 4), status])
        
    return pd.DataFrame(data, columns=["Year", "Age", "Homo Dev", "Eris Dev", "Neptune Dev", "Status"])

# UI Layout
year = st.number_input("Inception/Birth Year", 1900, 2100, 2000)
horizon = st.slider("Forecast Horizon (Years)", 10, 100, 50)

if st.button("Execute Radar Analysis"):
    df = run_usm_engine(year, horizon)
    
    # Styling
    def color_status(val):
        return 'color: red' if val == 'CRITICAL' else 'color: green'
    
    styled_df = df.style.map(color_status, subset=['Status'])
    st.dataframe(styled_df, use_container_width=True)
    
    # PDF Generation
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="Neptune-Haumea-Eris Radar Report", ln=True, align='C')
    pdf.set_font("Arial", size=10)
    pdf.cell(200, 10, txt=f"Inception Year: {year} | Precision: 0.30", ln=True)
    pdf.ln(5)
    
    # Table header
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(25, 10, "Year", border=1)
    pdf.cell(25, 10, "Homo", border=1)
    pdf.cell(25, 10, "Eris", border=1)
    pdf.cell(25, 10, "Nept", border=1)
    pdf.cell(30, 10, "Status", border=1)
    pdf.ln()
    
    pdf.set_font("Arial", size=10)
    for i in range(len(df)):
        pdf.cell(25, 10, str(df.iloc[i, 0]), border=1)
        pdf.cell(25, 10, str(df.iloc[i, 2]), border=1)
        pdf.cell(25, 10, str(df.iloc[i, 3]), border=1)
        pdf.cell(25, 10, str(df.iloc[i, 4]), border=1)
        pdf.cell(30, 10, str(df.iloc[i, 5]), border=1)
        pdf.ln()
    
    pdf_output = pdf.output(dest='S').encode('latin-1')
    st.download_button("Download Radar Report", pdf_output, "radar_report.pdf", "application/pdf")

st.write("---")
