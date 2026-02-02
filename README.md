# 🚀 Ruh.ai Integration Page Generator

AI-powered content generation automation system for creating SEO-optimized integration pages for 1,181+ third-party connectors.

## 📋 Features

- ✅ **SEO Optimization** - Researches keywords using SerpAPI before content generation
- ✅ **Factual Research** - Verifies tool capabilities with real search data (85-90% accuracy)
- ✅ **Automated Publishing** - Direct integration with Strapi CMS
- ✅ **Batch Processing** - Generate hundreds of pages automatically
- ✅ **Cost Effective** - ~$0.009-0.011 per page
- ✅ **100% Success Rate** - Simplified LLM-based approach

## 🛠️ Tech Stack

- **Python 3.9+**
- **LangChain** - AI framework for content generation
- **OpenRouter API** - GPT-4o-mini for content writing
- **SerpAPI** - SEO keyword research & factual verification
- **Strapi CMS** - Content management system

## 📊 Current Status

- **Total Connectors:** 1,181
- **Published:** 46 (4%)
- **Remaining:** 1,135 (96%)

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd connector-automation
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env.python` file:

```bash
# OpenRouter API (GPT-4o-mini)
OPENAI_API_KEY=your_openrouter_api_key
OPENAI_API_BASE=https://openrouter.ai/api/v1

# SerpAPI (for SEO & research)
SERPAPI_API_KEY=your_serpapi_key

# Strapi CMS
STRAPI_API_URL=http://127.0.0.1:8083
STRAPI_API_TOKEN=your_strapi_token
```

### 4. Run the Generator

```bash
# Generate next connector
python3 generate_integration_pages.py next

# Generate batch of 10
python3 generate_integration_pages.py batch 10

# Check status
python3 generate_integration_pages.py status
```

## 📁 Project Structure

```
connector-automation/
├── generate_integration_pages.py  # Main entry point
├── langchain_simple_agent.py      # Content generation agent
├── serpapi_client.py              # SerpAPI client
├── strapi_direct_client.py        # Strapi API client
├── strapi_content_parser.py       # Content parser
├── connectorList.json             # 1,181 connectors data
├── requirements.txt               # Python dependencies
├── .env.python                    # Environment variables (not in git)
└── integration-pages/             # Generated content output
```

## 💰 Cost Breakdown

**Per Page:**
- SerpAPI: $0.008 (4 searches)
- OpenRouter: $0.001-0.003 (GPT-4o-mini)
- **Total:** $0.009-0.011

**For All 1,135 Pages:**
- **Total Cost:** ~$10-12

## 🔑 API Keys Required

1. **OpenRouter** - https://openrouter.ai/
2. **SerpAPI** - https://serpapi.com/ (250 free searches/month)
3. **Strapi** - Your local/hosted Strapi instance

## 📖 Usage Examples

### Generate Single Page
```bash
python3 generate_integration_pages.py next
```

### Generate Batch
```bash
python3 generate_integration_pages.py batch 50
```

### Generate All Remaining
```bash
python3 generate_integration_pages.py batch 1135
```

## 🎯 Content Quality

- **SEO Optimized** - Natural keyword incorporation
- **Factually Accurate** - 85-90% accuracy with real research
- **Ruh.ai Style** - Conversational tone, no metrics
- **Strapi Ready** - HTML formatted with semi-bold labels

## 📝 License

MIT License

## 🤝 Contributing

Contributions welcome! Please open an issue or PR.

## 📧 Contact

For questions or support, please open an issue.

