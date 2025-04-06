import streamlit as st
import pandas as pd
from utils import get_engagement_string
from utils import get_cached_engagement_summary

st.title("📊 Top Tweet Analyzer")
st.markdown("<div class='cyber-box'>Upload a CSV of tweets and we'll analyze engagement patterns.</div>", unsafe_allow_html=True)

df = st.session_state.get("tweet_df")
if df is not None:
    with st.spinner("Analyzing engagement ..."):
        engagement_string = get_cached_engagement_summary(df)

    st.subheader("Top Tweets")
    st.dataframe(df[['text', 'engagement']].sort_values(by='engagement', ascending=False), use_container_width=True)

    st.subheader("Engagement Summary")
    st.markdown(f"<div class='highlight-box'>{engagement_string}</div>", unsafe_allow_html=True)
else:
    st.markdown("<div style='color:#00bfff;font-weight:bold;'>⚠️ Please upload a CSV in the sidebar to begin.</div>", unsafe_allow_html=True)
