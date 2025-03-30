import requests
import streamlit as st
from datetime import datetime

# Cache the customizations for 1 hour to reduce API calls
@st.cache_data(ttl=3600)
def get_ui_customizations():
    api_key = st.secrets.get("ADMIN_API_KEY")
    api_url = st.secrets.get("ADMIN_API_URL")
    
    if not api_key or not api_url:
        return None
        
    headers = {"Authorization": f"Bearer {api_key}"}
    
    try:
        response = requests.get(api_url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error fetching customizations: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error fetching customizations: {e}")
        return None

# Apply customizations to the UI
def apply_customizations():
    customizations = get_ui_customizations()
    
    if customizations:
        # Set page title and favicon
        app_title = customizations.get("app_title", "NLP Sentiment Analyzer")
        st.set_page_config(
            page_title=app_title,
            page_icon="📊",
            layout="wide"
        )
        
        # Apply theme color
        theme_color = customizations.get("theme_color", "#1E88E5")
        st.markdown(f"""
        <style>
        :root {{
            --primary-color: {theme_color};
        }}
        .stApp {{
            color: {theme_color};
        }}
        </style>
        """, unsafe_allow_html=True)
        
        # Return customizations for further use
        return customizations
    
    return None