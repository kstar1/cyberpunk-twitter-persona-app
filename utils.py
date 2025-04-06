import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
from scipy.stats import ttest_ind
from dotenv import load_dotenv
import os
from genai import GenAI

load_dotenv()

def get_genai():
    api_key = os.getenv("OPENAI_API_KEY")
    return GenAI(api_key)

def get_engagement_string(df, top_n=10):
    genai = get_genai()

    try:
        df_sorted = df.sort_values(by='engagement', ascending=False).head(top_n)
        tweet_samples = "\n".join([
            f"Tweet: {row['text']}\nEngagement: {row['engagement']:.4f}"
            for _, row in df_sorted.iterrows()
        ])
        prompt = f"""
Here are some tweets and their engagement scores (favorites/views):

{tweet_samples}

What patterns or features seem to make tweets perform well? Give a short, insightful summary.
"""
        return genai.generate_text(prompt, instructions="You are a social media analyst AI.")
    except Exception as e:
        return f"⚠️ Failed to generate engagement summary: {e}"

def compute_keyword_engagement(df, keyword_string):
    keywords = [kw.strip().lower() for kw in keyword_string.split(",") if kw.strip()]
    results = []

    for kw in keywords:
        mask = df['text'].str.lower().str.contains(kw)
        true_vals = df[mask]['engagement']
        false_vals = df[~mask]['engagement']

        if len(true_vals) < 2 or len(false_vals) < 2:
            pval = 1.0
        else:
            _, pval = ttest_ind(true_vals, false_vals, equal_var=False, nan_policy='omit')

        results.append({
            "keyword": kw,
            "engagement_true": true_vals.mean() if not true_vals.empty else 0,
            "engagement_false": false_vals.mean() if not false_vals.empty else 0,
            "pvalue": pval
        })

    df_results = pd.DataFrame(results)
    df_results = df_results.sort_values("pvalue")
    m = len(df_results)
    df_results["rank"] = np.arange(1, m + 1)
    df_results["pvalue_bh"] = (df_results["pvalue"] * m / df_results["rank"]).clip(upper=1.0)

    return df_results[["keyword", "pvalue_bh", "engagement_false", "engagement_true"]]

def fetch_url_text(url, timeout=5):
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers, timeout=timeout)
        soup = BeautifulSoup(response.text, "html.parser")
        return soup.get_text(separator=" ", strip=True)
    except Exception as e:
        return f"[Could not extract text from {url}: {e}]"

def create_persona_tweet(topic, df, engagement_string, top_n=10):
    genai = get_genai()

    if topic.lower().startswith("http"):
        topic_text = fetch_url_text(topic)
    else:
        topic_text = topic

    try:
        top_tweets = df.sort_values(by='engagement', ascending=False).head(top_n)
        sample_tweets = "\n".join([
            f"Tweet: {row['text']}\nEngagement: {row['engagement']:.4f}"
            for _, row in top_tweets.iterrows()
        ])
        prompt = f"""
You are an AI trained to mimic the tweeting style of a user based on their most engaging tweets.

Topic: {topic_text}

User's top tweets:
{sample_tweets}

Engagement analysis: {engagement_string}

Write a new tweet on the topic above in the user's voice and style. The tweet should be concise, engaging, and formatted as a realistic tweet.
"""
        tweet_text = genai.generate_text(prompt, instructions="You are a tweet-generating AI.")
        return genai.display_tweet(text=tweet_text.strip(), screen_name="AI Persona")
    except Exception as e:
        return f"<div style='color:red'>❌ Error generating tweet: {e}</div>"

import streamlit as st

@st.cache_data(show_spinner=False)
def get_cached_engagement_summary(df):
    return get_engagement_string(df)
