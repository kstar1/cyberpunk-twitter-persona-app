# 💫 Cyberpunk Twitter Persona App

A Streamlit app that analyzes tweet engagement, visualizes keyword performance, and generates AI-persona tweets — all wrapped in a vibrant cyberpunk aesthetic.

![screenshot](lucy-cyberpunk-cityscape.jpg)

## 🚀 Features

- 📊 **Top Tweet Analyzer** — View and summarize your most engaging tweets
- 🧠 **Keyword Engagement Explorer** — Analyze how specific keywords affect engagement
- 🖊️ **Persona Tweet Generator** — Create new tweets in the voice of your top-performing style
- 🎨 **Cyberpunk Styling** — Neon UI powered by `styles.css`
- ⚡ **Fast & Efficient** — OpenAI calls are cached for reuse

## 🗂️ Project Structure
```
cyberpunk-twitter-persona-app/
│
├── app.py                      # Main entry — sets theme, loads background, navigation
├── utils.py                   # Helper functions
├── genai.py                   # Provided class
├── styles.css                 # Cyberpunk styling (optional)
├── lucy-cyberpunk-cityscape.jpg
├── requirements.txt
│
├── pages/
│   ├── 1_Homepage.py
│   ├── 2_Keyword_Engagement.py
│   └── 3_Persona_Tweet.py

```

## 🛠️ Setup Instructions

# Create environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Optional (for auto-reload on save)
pip install watchdog

# Run the app
streamlit run app.py --server.runOnSave=true
⚠️ Be sure to set your OpenAI API key in a .env file:
```
OPENAI_API_KEY=your_key_here
```
# 📥 Sample Tweet Files
You can use included CSVs like:
* TwExportly_elonmusk_tweets_2025_03_27.csv
* TwExportly_aoc_tweets_2025_01_30.csv

# ✅ Status
* ✅ All major features implemented
* ✅ Instructor feedback integrated
* 🚧 More polish ideas in issues (tooltips, light mode, export, etc.)

Made with 💻 + 💜 by Kshitij