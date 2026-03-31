"""
Bulk Analysis Page - Analyze multiple samples at once
"""
import streamlit as st
import pandas as pd
from config import CUSTOM_CSS
from utils.api_client import APIClient
from components.ui import header, section_divider, error_box


def render():
    """Render bulk analysis page."""
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
    
    header(title="Bulk Water Analysis", subtitle="Analyze multiple samples at once", icon="📦")
    
    st.info(
        "📤 **Upload a CSV file** with Raw Water (RW) metrics to analyze multiple samples.\n\n"
        "**Expected columns:**\n"
        "RW pH, RW Tur, RW Colour, RW TDS, RW Iron, RW Hardness, RW S Solids, RW Aluminium, "
        "RW Chloride, RW Manganese, RW Conductivity, RW Calcium, RW Magnesium, RW Alkalinity, RW Ammonia as N"
    )
    
    # File uploader card
    with st.container(border=True):
        st.markdown("#### 📁 Upload Data File")
        uploaded_file = st.file_uploader(
            "Choose a CSV file",
            type=["csv"],
            label_visibility="collapsed"
        )
    
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.success(f"✅ Loaded {len(df)} samples")
            
            # Preview card
            with st.container(border=True):
                st.markdown("#### 📋 Data Preview")
                st.dataframe(df.head(), use_container_width=True)
                st.caption(f"Showing first 5 of {len(df)} rows | Columns: {', '.join(df.columns[:5])}...")
            
            # Analyze button
            col_btn, col_spacer = st.columns([1, 4])
            with col_btn:
                if st.button("🚀 Analyze Batch", type="primary", use_container_width=True):
                    with st.spinner("⏳ Processing all samples..."):
                        results = []
                        progress_bar = st.progress(0)
                        status_placeholder = st.empty()
                        
                        for idx, row in df.iterrows():
                            payload = row.to_dict()
                            try:
                                result = APIClient.analyze_water(payload)
                                result["sample_id"] = idx + 1
                                results.append(result)
                                status_placeholder.info(f"Processed: {idx + 1} / {len(df)} samples")
                            except Exception as e:
                                st.warning(f"⚠️ Sample {idx + 1} failed: {str(e)}")
                            
                            progress_bar.progress((idx + 1) / len(df))
                        
                        if results:
                            section_divider("📊 Analysis Results")
                            
                            st.success(f"✅ Analyzed {len(results)} / {len(df)} samples successfully")
                            
                            # Results table
                            results_df = pd.DataFrame([
                                {
                                    "Sample ID": r["sample_id"],
                                    "Status": "✅ Safe" if r["classification"]["status_code"] == 1 else "⚠️ Toxic",
                                    "Confidence (%)": r["classification"]["confidence_safe_percent"] 
                                        if r["classification"]["status_code"] == 1 
                                        else r["classification"]["confidence_toxic_percent"],
                                    "Message": r["classification"]["message"],
                                }
                                for r in results
                            ])
                            
                            st.dataframe(results_df, use_container_width=True)
                            
                            # Download results
                            col_dl, col_stats = st.columns([1, 3])
                            
                            with col_dl:
                                csv = results_df.to_csv(index=False)
                                st.download_button(
                                    label="📥 Download Results",
                                    data=csv,
                                    file_name="water_analysis_results.csv",
                                    mime="text/csv",
                                    use_container_width=True
                                )
                            
                            with col_stats:
                                safe_count = sum(1 for r in results if r["classification"]["status_code"] == 1)
                                toxic_count = len(results) - safe_count
                                st.metric("Safe Samples", safe_count, delta=None)
                                st.metric("Toxic Samples", toxic_count, delta=None)
                        else:
                            st.error("❌ No samples were successfully analyzed.")
        
        except Exception as e:
            error_box("File Error", f"Failed to read CSV: {str(e)}")
    else:
        # Empty state
        with st.container(border=True):
            st.markdown("#### 🎯 No File Selected")
            st.info("Upload a CSV file with Raw Water metrics to get started with bulk analysis.")
