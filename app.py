import streamlit as st
import base64
import pandas as pd

# Set Streamlit page config
st.set_page_config(page_title="💫 Cyberpunk Twitter Persona App", layout="wide")

# Load background image
def get_base64_img(img_path):
    with open(img_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

# Load custom CSS
def load_styles():
    with open("style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    # Background image
    bg_image = get_base64_img("lucy-cyberpunk-cityscape.jpg")
    st.markdown(f"""
        <style>
        html, body, .stApp {{
            background-image: url("data:image/jpg;base64,{bg_image}");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
            background-position: center;
        }}
        </style>
    """, unsafe_allow_html=True)

# Apply styles
load_styles()

# Header shown on all pages
st.sidebar.title("🧭 Navigation")

uploaded_file = st.sidebar.file_uploader("Upload Tweet CSV", type=["csv"])

if uploaded_file:
    st.sidebar.write("📂 File uploaded:", uploaded_file.name)
    df = pd.read_csv(uploaded_file)

    if 'favorite_count' in df.columns and 'view_count' in df.columns:
        df['engagement'] = df['favorite_count'] / df['view_count']
        st.session_state["tweet_df"] = df
        st.sidebar.success("✅ Loaded favorites / views into engagement.")
    elif 'engagement' in df.columns:
        st.session_state["tweet_df"] = df
        st.sidebar.success("✅ Loaded precomputed engagement scores.")
    else:
        st.sidebar.error("❌ CSV must have either 'engagement' or both 'favorite_count' and 'view_count'.")
else:
    st.sidebar.info("📄 Upload a CSV to begin.")

