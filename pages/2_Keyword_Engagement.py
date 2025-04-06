import streamlit as st
import altair as alt
from utils import compute_keyword_engagement

st.title("🧠 Keyword Engagement Explorer")
st.markdown("<div class='cyber-box'>Enter comma-separated keywords to analyze their engagement patterns.</div>", unsafe_allow_html=True)

df = st.session_state.get("tweet_df")
if df is not None:
    keywords_string = st.text_input("Keywords (comma-separated)", placeholder="e.g. ai, space, mars")
    if st.button("Analyze"):
        with st.spinner("Crunching keyword engagement ..."):
            df_keywords = compute_keyword_engagement(df, keywords_string)

        melted = df_keywords.melt(
            id_vars=["keyword", "pvalue_bh"],
            value_vars=["engagement_false", "engagement_true"],
            var_name="Has Keyword",
            value_name="Engagement"
        )
        melted["Has Keyword"] = melted["Has Keyword"].map({
            "engagement_false": "False", "engagement_true": "True"
        })

        bar = alt.Chart(melted).mark_bar().encode(
            x=alt.X("keyword:N", title="Keyword"),
            y=alt.Y("Engagement:Q"),
            color=alt.Color("Has Keyword:N", scale=alt.Scale(range=["#ff0090", "#00ffe7"])),
            tooltip=["keyword", "Has Keyword", "Engagement"]
        ).properties(width=500, height=400)

        text_layer = alt.Chart(melted[melted["Has Keyword"] == "True"]).mark_text(
            dy=-10,
            color="#00ff99",
            fontWeight="bold"
        ).encode(
            x="keyword:N",
            y="Engagement:Q",
            text=alt.Text("pvalue_bh:Q", format=".3f")
        )

        st.altair_chart(bar + text_layer, use_container_width=True)
else:
    st.markdown("<div style='color:#00bfff;font-weight:bold;'>⚠️ Please upload a CSV in the sidebar to begin.</div>", unsafe_allow_html=True)
