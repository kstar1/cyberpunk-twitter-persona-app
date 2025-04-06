import streamlit as st
from utils import create_persona_tweet, get_engagement_string

st.title("🖊️ Persona Tweet Generator")
st.markdown("<div class='cyber-box'>Enter a topic or paste a URL. We'll generate a tweet in the style of the uploaded user.</div>", unsafe_allow_html=True)

df = st.session_state.get("tweet_df")
if df is not None:
    topic = st.text_input("Topic or URL", placeholder="e.g. AI regulation or https://www.nytimes.com/...")
    if st.button("Create Tweet"):
        with st.spinner("Generating tweet in user's voice ..."):
            engagement_summary = get_engagement_string(df)
            tweet_html = create_persona_tweet(topic, df, engagement_summary)

        st.subheader("AI-Generated Persona Tweet")
        st.components.v1.html(tweet_html, height=300)
else:
    st.markdown("<div style='color:#00bfff;font-weight:bold;'>⚠️ Please upload a CSV in the sidebar to begin.</div>", unsafe_allow_html=True)
