#!/usr/bin/env python3
"""
SIMPLE TEST VERSION - NO DATA DEPENDENCIES
This file tests basic Streamlit functionality without requiring data files.
Use this to verify Streamlit Cloud deployment works.
"""

import streamlit as st
import pandas as pd
import numpy as np

# Page configuration
st.set_page_config(
    page_title="MusiPy Test - Basic Functionality",
    page_icon="🎵",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

def main():
    """Simple test function"""
    st.markdown('<h1 class="main-header">🎵 MusiPy Test</h1>', unsafe_allow_html=True)
    st.markdown("### Basic Functionality Test")
    
    st.success("✅ Streamlit is working!")
    
    # Test basic functionality
    st.markdown("### 🧪 Testing Components")
    
    # Test sliders
    st.markdown("#### Slider Test")
    test_value = st.slider("Test Slider", 1, 10, 5)
    st.write(f"Slider value: {test_value}")
    
    # Test buttons
    st.markdown("#### Button Test")
    if st.button("Test Button"):
        st.success("Button clicked!")
    
    # Test data display
    st.markdown("#### Data Display Test")
    test_data = pd.DataFrame({
        'Trait': ['Openness', 'Conscientiousness', 'Extraversion'],
        'Score': [3.5, 4.2, 2.8]
    })
    st.dataframe(test_data)
    
    # Test columns
    st.markdown("#### Layout Test")
    col1, col2 = st.columns(2)
    with col1:
        st.info("Left column")
    with col2:
        st.warning("Right column")
    
    st.markdown("### 🎉 All Tests Passed!")
    st.markdown("""
    If you can see this page, Streamlit Cloud deployment is working correctly.
    
    **Next Steps:**
    1. Deploy the full `streamlit_standalone.py` app
    2. Ensure all data files are in the repository
    3. Check file paths are correct
    """)

if __name__ == "__main__":
    main()
