# 🏦 Regulation Tracker Dashboard


**[🚀 Live Dashboard](https://regulationnews-khvu3dtti5pz8f2gr5dw9f.streamlit.app/)** | **[📊 GitHub Repository](https://github.com/Dhruv-baner/regulation_news)**


## **What Is This?**

- The goal of this project was to essentially come up woith some kind of AI-enabled tracker, which would collect data on regulatory changes in NBIM's 5 biggest markets, and then give some insights into those. 

- Step one was to of course **identify the relevant markets**. This project focuses on: USA, UK, France, Germany, and Japan. Certainly a good mix, with differing approaches to regulation 

| Country        | Value (NOK)           | Investments | % of Portfolio |
|----------------|-----------------------|-------------|----------------|
| USA            | 10,488,258,386,469   | 2,901       | 52.4%          |
| Japan          | 1,207,846,613,870    | 1,410       | 6.0%           |
| United Kingdom | 1,100,973,152,288    | 1,036       | 5.5%           |
| Germany        | 916,292,718,569      | 295         | 4.6%           |
| France         | 708,716,940,392      | 263         | 3.5%           |

- Then came the **data collection**, using multi-source aggregation from sources such as NewsAPI and Google News. This got us a pretty decent set of articles for each of the markets ove the last few days.

- Then the **LLM** bit. I got an OpenAI API key and prompted GPT to go through each article and give me their relevance scores, categorise them based on type of regulation, and identify key regulators invoved. I also asked for brief summaries. 

- Finally, **visualisation** was done with one eye on storytelling. I have a range of 5 visualisations,showing different aspects of the analysis. I worked on them meticulously to make sure they are visually aesthetic, thematically conistent, and highly informative. 
---

## 📸 Dashboard Preview

### **Note: The visualisations are all INTERACTIVE**. These are merely screenshots of what they look like.


### Geographic Intelligence View
![Geographic View](assets\screenshots\plot_1.png)

### Market Overview & Distribution
![Market Overview](assets\screenshots\plot_2.png)
![Market Distribution](assets\screenshots\plot_3.png)

### Regulation Type by Market
![Regulation Categories]()



---

## 🎯 Project Overview

This system automatically:
- Fetches regulatory news from multiple sources (NewsAPI, Google News RSS)
- Analyzes relevance using GPT-3.5-turbo with custom prompts
- Categorizes articles by regulation type and impact level
- Visualizes insights through interactive dashboards

**Target Markets** (covering 72% of Norges Bank's equity portfolio):
- 🇺🇸 United States (52.4%)
- 🇯🇵 Japan (6.0%)
- 🇬🇧 United Kingdom (5.5%)
- 🇩🇪 Germany (4.6%)
- 🇫🇷 France (3.5%)

---

## ✨ Key Features

### Intelligent Data Collection
- Multi-source aggregation from NewsAPI and Google News
- Market-specific keyword targeting for regulatory authorities
- Automated deduplication and quality filtering

### GPT-Powered Analysis
- Custom prompt engineering for institutional investor perspective
- Structured outputs: relevance scores (0-10), impact levels, categories
- Identification of key regulators and policy implications

### Interactive Visualizations
- **Geographic Intelligence Map**: Hover-enabled country view with regulatory metrics
- **Market Comparison**: Dual-axis charts showing volume vs. relevance
- **Category Distribution**: Regulatory focus areas by market
- **Curated Articles**: Top 25 most relevant developments with filtering

### Real-Time Filtering
- Dynamic filters by market, category, impact level, and relevance threshold
- Instant dashboard updates based on user selections

---

## 🛠️ Tech Stack

**Backend & Analysis:**
- Python 3.12
- pandas (data manipulation)
- OpenAI API (GPT-3.5-turbo for analysis)

**Data Sources:**
- NewsAPI
- Google News RSS

**Visualization & Dashboard:**
- Streamlit (web framework)
- Plotly (interactive charts)

**Deployment:**
- Streamlit Community Cloud
- GitHub version control

---

## 📊 Data Pipeline
```
┌─────────────────┐
│  Data Sources   │
│ NewsAPI + RSS   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Collection    │
│ Market-specific │
│   queries       │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ LLM Analysis    │
│ GPT-3.5 scoring │
│ Categorization  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Dashboard      │
│ Interactive viz │
│   + Filters     │
└─────────────────┘
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- API Keys: [NewsAPI](https://newsapi.org/), [OpenAI](https://platform.openai.com/)

### Installation
```bash
# Clone repository
git clone https://github.com/Dhruv-baner/regulation_news.git
cd regulation_news

# Install dependencies
pip install -r requirements.txt

# Configure API keys
cp .env.example .env
# Edit .env with your API keys

# Run dashboard
streamlit run app.py
```

Dashboard opens at `http://localhost:8501`

---

## 📁 Project Structure
```
regulation_news/
│
├── notebooks/
│   ├── 01_data_collection.ipynb      # Multi-source news fetching
│   ├── 02_llm_analysis.ipynb         # GPT-based relevance scoring
│   └── 03_visualization_dashboard.ipynb  # Chart prototyping
│
├── src/
│   ├── news_fetcher.py               # NewsAPI wrapper
│   ├── llm_analyzer.py               # OpenAI integration
│   └── data_processor.py             # Data cleaning
│
├── data/
│   ├── raw/                          # Collected news (gitignored)
│   └── processed/                    # Analyzed articles (gitignored)
│
├── app.py                            # Streamlit dashboard
├── config.yaml                       # Configuration parameters
└── requirements.txt                  # Dependencies
```

---

## 🧠 Methodology

### Data Collection
- **Coverage**: 30-day lookback period across 5 markets
- **Volume**: ~650 unique articles after deduplication
- **Sources**: Financial news outlets and regulatory authority press releases

### LLM Analysis Approach

**System Prompt Strategy:**
- Role: Regulatory analyst for sovereign wealth fund
- Focus: Portfolio impact, systemic risk, early warning signals

**Structured Outputs:**
```json
{
  "relevance_score": "0-10 scale",
  "impact_level": "high/medium/low",
  "category": "monetary_policy | banking_regulation | securities_regulation | ...",
  "key_regulators": ["identified authorities"],
  "what_happened": "event description",
  "why_relevant": "investor implications"
}
```

### Quality Controls
- Deduplication by normalized titles
- Exclusion of crypto-focused sources
- Manual curation of top articles per market

---

## 📈 Sample Insights

From current data (as of Nov 2025):
- **652 total articles** analyzed across 5 markets
- **Average relevance score**: 5.5/10
- **34% high-impact articles** requiring immediate attention
- **Top categories**: Securities regulation (30%), Monetary policy (24%)

---

## 🔮 Future Enhancements

- **Automated Scheduling**: Daily data refresh and email digests
- **Sentiment Analysis**: Track regulatory tone shifts over time
- **Historical Trends**: Long-term pattern analysis and predictive signals
- **Alert System**: Notifications for high-impact developments
- **Multi-language Support**: Expand to non-English regulatory sources
- **API Endpoint**: REST API for programmatic access

---

## 👤 Author

Dhruv Baner
- MSc Data Science, LSE
 [GitHub](https://github.com/Dhruv-baner)




