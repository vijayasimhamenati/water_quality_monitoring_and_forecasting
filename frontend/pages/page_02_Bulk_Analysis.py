"""
Bulk Analysis Page - Analyze multiple samples at once
"""
import streamlit as st
import pandas as pd
from frontend.config import CUSTOM_CSS
from frontend.utils.api_client import APIClient
from frontend.components.ui import header, section_divider, error_box


def render():
    """Render bulk analysis page."""
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
    
    header(title="Bulk Water Analysis", subtitle="Analyze multiple samples", icon="📦")
    
    st.info(
        "📤 **Upload a CSV file** with Raw Water (RW) metrics to analyze multiple samples.\n\n"
        "Expected columns: RW pH, RW Tur, RW Colour, RW TDS, RW Iron, RW Hardness, "
        "RW S Solids, RW Aluminium, RW Chloride, RW Manganese, RW Conductivity, "
        "RW Calcium, RW Magnesium, RW Alkalinity, RW Ammonia as N"
    )
    
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.success(f"✅ Loaded {len(df)} samples")
            
            st.markdown("### 📋 Preview")
            st.dataframe(df.head(), use_container_width=True)
            
            if st.button("🚀 Analyze All Samples", type="primary"):
                with st.spinner("Processing..."):
                    results = []
                    progress_bar = st.progress(0)
                    
                    for idx, row in df.iterrows():
                        payload = row.to_dict()
                        try:
                            result = APIClient.analyze_water(payload)
                            result["sample_id"] = idx + 1
                            results.append(result)
                        except Exception as e:
                            st.warning(f"⚠️ Sample {idx + 1} failed: {str(e)}")
                        
                        progress_bar.progress((idx + 1) / len(df))
                    
                    if results:
                        st.success(f"✅ Analyzed {len(results)} / {len(df)} samples")
                        
                        # Display results table
                        results_df = pd.DataFrame([
                            {
                                "Sample ID": r["sample_id"],
                                "Status": "Safe" if r["classification"]["status_code"] == 1 else "Toxic",
                                "Confidence (%)": r["classification"]["confidence_safe_percent"] 
                                    if r["classification"]["status_code"] == 1 
                                    else r["classification"]["confidence_toxic_percent"],
                            }
                            for r in results
                        ])
                        
                        st.markdown("### 📊 Results Summary")
                        st.dataframe(results_df, use_container_width=True)
                        
                        # Download results
                        csv = results_df.to_csv(index=False)
                        st.download_button(
                            label="📥 Download Results as CSV",
                            data=csv,
                            file_name="water_analysis_results.csv",
                            mime="text/csv"
                        )
        
        except Exception as e:
            error_box("File Error", f"Failed to read CSV: {str(e)}")
    else:
        st.info("🎯 No file selected. Upload a CSV to get started.")
