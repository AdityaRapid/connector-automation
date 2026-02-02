"""
SerpAPI Client for SEO Keyword Research
FREE tier: 250 searches/month, no credit card required
Get your API key at: https://serpapi.com/manage-api-key
"""

import os
import json
import asyncio
import httpx
from typing import Dict, Any, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv('.env.python')


class SerpAPIClient:
    """Client for SerpAPI - FREE tier with 250 searches/month"""

    def __init__(self):
        self.api_key = os.getenv('SERPAPI_API_KEY')
        self.base_url = 'https://serpapi.com/search'

    async def get_keyword_data(self, keyword: str, country: str = "us") -> Dict[str, Any]:
        """
        Get keyword data from SerpAPI

        Args:
            keyword: The keyword to research
            country: Country code (default: us)

        Returns:
            Dictionary with keyword metrics
        """
        if not self.api_key or self.api_key == 'your_serpapi_api_key_here':
            print("⚠️  No SerpAPI key found - using estimation")
            print("   Get your FREE API key at: https://serpapi.com/manage-api-key")
            print("   FREE tier: 250 searches/month, no credit card required!")
            return self._fallback_keyword_data(keyword)

        try:
            print(f"🔍 Searching SerpAPI for: {keyword}")
            
            # Make API request to SerpAPI
            async with httpx.AsyncClient(timeout=30.0) as client:
                params = {
                    'q': keyword,
                    'api_key': self.api_key,
                    'engine': 'google',
                    'gl': country,
                    'hl': 'en',
                    'num': 10
                }
                
                response = await client.get(self.base_url, params=params)
                response.raise_for_status()
                
                data = response.json()
                
                # Extract keyword insights from SERP data
                keyword_data = self._extract_keyword_insights(keyword, data)
                
                print(f"✅ SerpAPI data retrieved successfully")
                return keyword_data

        except httpx.HTTPStatusError as e:
            print(f"❌ SerpAPI HTTP error: {e.response.status_code} - {e.response.text}")
            return self._fallback_keyword_data(keyword)
        except Exception as e:
            print(f"❌ Error calling SerpAPI: {str(e)}")
            return self._fallback_keyword_data(keyword)

    def _extract_keyword_insights(self, keyword: str, serp_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract keyword insights from SERP data"""

        # Get organic results count
        organic_results = serp_data.get('organic_results', [])
        num_results = len(organic_results)

        # Extract factual snippets from top organic results
        factual_snippets = []
        for result in organic_results[:5]:  # Top 5 results
            snippet = result.get('snippet', '')
            title = result.get('title', '')
            if snippet:
                factual_snippets.append({
                    'title': title,
                    'snippet': snippet,
                    'link': result.get('link', '')
                })

        # Get related searches
        related_searches = serp_data.get('related_searches', [])
        related_keywords = [r.get('query', '') for r in related_searches[:5]]

        # Get "People also ask" questions
        people_also_ask = serp_data.get('related_questions', [])
        long_tail_keywords = [q.get('question', '') for q in people_also_ask[:5]]

        # Estimate search volume based on number of results and competition
        # More results = higher search volume (rough estimation)
        estimated_volume = min(max(num_results * 10, 500), 5000)

        # Determine competition based on ads and organic results
        ads_count = len(serp_data.get('ads', []))
        if ads_count >= 3:
            competition = "high"
            estimated_cpc = 3.5
        elif ads_count >= 1:
            competition = "medium"
            estimated_cpc = 2.5
        else:
            competition = "low"
            estimated_cpc = 1.5

        return {
            "keyword": keyword,
            "search_volume": estimated_volume,
            "cpc": estimated_cpc,
            "competition": competition,
            "related_keywords": related_keywords if related_keywords else [
                f"{keyword} software",
                f"{keyword} platform",
                f"{keyword} tool",
                f"best {keyword}",
                f"top {keyword}"
            ],
            "long_tail_keywords": long_tail_keywords if long_tail_keywords else [
                f"how to use {keyword}",
                f"{keyword} integration guide",
                f"best {keyword} for business",
                f"{keyword} automation workflow",
                f"{keyword} vs alternatives"
            ],
            "factual_snippets": factual_snippets,  # NEW: Real facts from search results
            "source": "serpapi",
            "num_organic_results": num_results,
            "num_ads": ads_count
        }

    def _fallback_keyword_data(self, keyword: str) -> Dict[str, Any]:
        """Fallback estimation when API is not available"""
        # Simple hash-based estimation for consistency
        keyword_hash = sum(ord(c) for c in keyword.lower())
        base_volume = 500 + (keyword_hash % 1000)
        
        return {
            "keyword": keyword,
            "search_volume": base_volume,
            "cpc": 2.5,
            "competition": "medium",
            "related_keywords": [
                f"{keyword} software",
                f"{keyword} platform",
                f"{keyword} tool",
                f"best {keyword}",
                f"top {keyword}"
            ],
            "long_tail_keywords": [
                f"how to use {keyword}",
                f"{keyword} integration guide",
                f"best {keyword} for business",
                f"{keyword} automation workflow",
                f"{keyword} vs alternatives"
            ],
            "source": "estimated"
        }


class SerpAPISync:
    """Synchronous wrapper for SerpAPIClient"""

    def __init__(self):
        self.client = SerpAPIClient()

    def get_keyword_data(self, keyword: str, country: str = "us") -> Dict[str, Any]:
        """Synchronous wrapper for get_keyword_data"""
        return asyncio.run(self.client.get_keyword_data(keyword, country))


# Test the client
if __name__ == "__main__":
    print("🚀 Testing SerpAPI Client (FREE - 250 searches/month)...")
    print(f"✅ API Key: {'Set' if os.getenv('SERPAPI_API_KEY') and os.getenv('SERPAPI_API_KEY') != 'your_serpapi_api_key_here' else 'Not set'}")
    print()
    
    client = SerpAPISync()
    result = client.get_keyword_data("project management software")
    
    print("\n📊 Result:")
    print(json.dumps(result, indent=2))

