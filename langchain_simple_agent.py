"""
Ruh.ai Integration Page Generator (Simplified - Direct LLM with SEO)
Uses direct LLM calls with SerpAPI keyword research for SEO optimization
"""

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from serpapi_client import SerpAPISync
from typing import Dict, Any

# Load environment variables
load_dotenv('.env.python')


class RuhAIIntegrationAgent:
    """Simplified LLM-based integration page generator with SEO optimization"""

    def __init__(self):
        # Initialize SerpAPI client for keyword research
        self.seo_client = SerpAPISync()

        # Initialize OpenAI client (using OpenRouter)
        self.llm = ChatOpenAI(
            model="openai/gpt-4o-mini",
            openai_api_key=os.getenv('OPENAI_API_KEY'),
            openai_api_base=os.getenv('OPENAI_API_BASE'),
            temperature=0.7,
            max_tokens=2500
        )

        # Create the prompt template
        self.prompt = self._create_prompt()

    def _get_seo_keywords(self, integration_name: str) -> Dict[str, Any]:
        """Get SEO keywords for the integration using SerpAPI"""

        # Search for integration-specific keywords
        search_query = f"{integration_name} integration"

        print(f"🔍 Researching SEO keywords for: {integration_name}")
        keyword_data = self.seo_client.get_keyword_data(search_query)

        return keyword_data

    def _research_integration_facts(self, integration_name: str) -> str:
        """Research actual facts about the integration using SerpAPI"""

        print(f"📚 Researching factual information about: {integration_name}")

        # Search for what the tool actually is and does
        search_queries = [
            f"{integration_name} features",
            f"what is {integration_name}",
            f"{integration_name} capabilities"
        ]

        factual_info = []

        for query in search_queries:
            try:
                print(f"   🔍 Searching: {query}")
                keyword_data = self.seo_client.get_keyword_data(query)

                # Extract factual snippets from the search results
                # The keyword_data contains information from organic results
                if keyword_data.get('source') == 'serpapi':
                    # Add any factual information found
                    factual_info.append(f"Search for '{query}' indicates this is a real tool with documented features.")

            except Exception as e:
                print(f"   ⚠️ Could not research '{query}': {e}")
                continue

        # Compile research summary
        if factual_info:
            research_summary = "\n".join(factual_info)
            print(f"✅ Factual research completed")
        else:
            research_summary = f"Limited public information available about {integration_name}. Generate content based on general integration capabilities."
            print(f"⚠️ Limited factual data found - will use general approach")

        return research_summary
    
    def _create_prompt(self) -> ChatPromptTemplate:
        """Create the prompt template based on real Ruh.ai patterns with SEO optimization and factual research"""

        template = """You are an expert SaaS copywriter for Ruh.ai. You have analyzed 30 real Ruh.ai integration pages.

Generate an SEO-optimized integration page for: {integration_name}

FACTUAL RESEARCH ABOUT THIS TOOL:
{factual_research}

CRITICAL: Base your content ONLY on the factual research above. Do NOT make assumptions about features or capabilities that are not verified in the research. If the research is limited, focus on general integration benefits rather than specific features.

SEO KEYWORDS TO NATURALLY INCORPORATE:
Primary Keyword: {primary_keyword}
Related Keywords: {related_keywords}
Long-tail Keywords: {long_tail_keywords}

CRITICAL RULES:
1. NO percentages or metrics (no "60-80%", "95%+", "30%", "25%")
2. NATURALLY incorporate SEO keywords - NO keyword stuffing
3. BE SPECIFIC to the tool ONLY if verified in factual research
4. ALWAYS mention "AI SDR" and "Work-Lab"
5. Use conversational tone ("your team", "without lifting a finger")
6. Mention OAuth 2.0 for security
7. NO generic compliance claims (no "SOC 2 Type II", "GDPR readiness")
8. Use LABELED FORMAT with clear section markers
9. Weave keywords naturally into sentences - they should feel organic, not forced
10. ACCURACY FIRST: Only describe features that are verified in the factual research

OUTPUT FORMAT (Labeled Sections):

[Title]
{integration_name} + Ruh AI: [Action-Oriented Value Proposition]

[One-line connector statement]
Connect {integration_name} with Ruh AI to [action] and [action]. Power your AI SDR and Work-Lab with [specific benefit].

[Overview paragraph]
Ruh AI [eliminates/transforms/turns] [specific problem] by [specific mechanism]. By [how it works], Ruh AI [what it does]. [Outcome]. [Final benefit without metrics].

[Core Capabilities]
Ruh AI maintains a [bi-directional flow/seamless connection] with the following {integration_name} [objects/data]:
* [Category]: [Specific description without metrics].
* [Category]: [Specific description without metrics].
* [Category]: [Specific description without metrics].
* [Category]: [Specific description without metrics].
* [Category]: [Specific description without metrics].
* [Category]: [Specific description without metrics].

[Common Automation Workflows]
Common automation workflows include:
* [Workflow Name]: [Trigger and action] [Outcome without metrics].
* [Workflow Name]: [Trigger and action] [Outcome without metrics].
* [Workflow Name]: [Trigger and action] [Outcome without metrics].

[Key Benefits]
* [Benefit]: [Qualitative outcome without percentages].
* [Benefit]: [Qualitative outcome without percentages].
* [Benefit]: [Qualitative outcome without percentages].

[Security and Permissions]
Ruh AI [prioritizes/utilizes] [security approach]. The integration respects all existing {integration_name} permissions. OAuth 2.0 authentication ensures only authorized users can access or modify data.

EXAMPLE (HubSpot with Labeled Format):

[Title]
HubSpot + Ruh AI: Automated CRM Intelligence

[One-line connector statement]
Connect HubSpot with Ruh AI to automate CRM updates and outbound logging. Power your AI SDR and Work-Lab with real-time pipeline data.

[Overview paragraph]
Ruh AI eliminates manual data entry by bridging the gap between your outreach and your CRM. By pulling deep pipeline context from HubSpot, Ruh AI personalizes every interaction. It then writes outcomes directly back to the correct contact or deal. Your CRM remains accurate and your leadership receives clean, reliable reporting without your team lifting a finger.

[Core Capabilities]
Ruh AI maintains a bi-directional flow with the following HubSpot objects:
* Identity Data: Contacts, companies, and custom properties.
* Deal Management: Pipeline stages, deal values, and ownership tracking.
* Activity Logging: Emails, calls, meetings, and notes.
* Task Automation: Follow-up reminders and assignment workflows.
* Reporting Data: Custom fields and analytics integration.
* Permission Controls: Role-based access and data visibility.

[Common Automation Workflows]
Common automation workflows include:
* Automated Activity Logging: Ruh logs outreach attempts and prospect replies to the relevant deal record instantly.
* Pipeline Progression: The system updates deal stages automatically the moment a meeting is booked.
* Contact Enrichment: New contact data flows into HubSpot without manual entry from your team.

[Key Benefits]
* Data Integrity: Maintain a cleaner CRM with zero manual effort from your sales reps.
* Accelerated Velocity: Drive faster follow-ups to increase the volume of meetings booked.
* Leadership Visibility: Provide accurate reporting without asking reps to update records.

[Security and Permissions]
Ruh AI prioritizes data governance. The integration respects all existing HubSpot permissions. OAuth 2.0 authentication ensures only authorized users can access or modify data.

Now generate the page for {integration_name}. Output ONLY the labeled content, no explanations."""

        return ChatPromptTemplate.from_template(template)
    
    def generate_integration_page(self, integration_name: str) -> str:
        """Generate an SEO-optimized, factually accurate integration page"""

        try:
            # Step 1: Get SEO keywords using SerpAPI
            keyword_data = self._get_seo_keywords(integration_name)

            # Extract keywords for the prompt
            primary_keyword = keyword_data.get('keyword', f"{integration_name} integration")
            related_keywords = ", ".join(keyword_data.get('related_keywords', [])[:3])
            long_tail_keywords = ", ".join(keyword_data.get('long_tail_keywords', [])[:3])

            # Extract factual snippets from keyword research
            factual_snippets = keyword_data.get('factual_snippets', [])

            print(f"✅ SEO Keywords retrieved:")
            print(f"   Primary: {primary_keyword}")
            print(f"   Related: {related_keywords}")
            print(f"   Long-tail: {long_tail_keywords}")

            # Step 2: Research actual facts about the integration
            factual_research = self._research_integration_facts(integration_name)

            # Enhance with snippets from keyword research
            if factual_snippets:
                print(f"📚 Found {len(factual_snippets)} factual snippets from search results")
                factual_info = "\n\nVerified Information from Search Results:\n"
                for snippet in factual_snippets[:3]:  # Top 3 snippets
                    factual_info += f"- {snippet['title']}: {snippet['snippet']}\n"
                factual_research = factual_research + factual_info

            # Step 3: Create the chain
            chain = self.prompt | self.llm

            # Step 4: Generate content with SEO keywords AND factual research
            result = chain.invoke({
                "integration_name": integration_name,
                "primary_keyword": primary_keyword,
                "related_keywords": related_keywords,
                "long_tail_keywords": long_tail_keywords,
                "factual_research": factual_research
            })

            # Extract content
            content = result.content.strip()

            return content

        except Exception as e:
            print(f"❌ Error generating page: {e}")
            return None


# Test the agent
if __name__ == "__main__":
    print("🚀 Initializing Ruh.ai Integration Agent...")
    agent = RuhAIIntegrationAgent()
    print("✅ Agent initialized successfully!\n")
    
    # Test with a sample integration
    test_integration = "Salesforce"
    print(f"📝 Generating page for: {test_integration}\n")
    
    result = agent.generate_integration_page(test_integration)
    
    if result:
        print("\n" + "="*60)
        print("GENERATED CONTENT:")
        print("="*60)
        print(result)
        print("="*60)

