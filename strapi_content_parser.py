"""
Strapi Content Parser
Parses generated integration pages and formats them for Strapi API
"""

import re
from typing import Dict, Any, List, Optional
from datetime import datetime
from category_matcher import CategoryMatcher


class StrapiContentParser:
    """Parser for converting generated integration pages to Strapi format"""

    @staticmethod
    def parse_integration_page(file_path: str, connector_name: str, logo_url: str = "") -> Dict[str, Any]:
        """
        Parse integration page and format for Strapi API

        Args:
            file_path: Path to the generated integration page
            connector_name: Name of the connector
            logo_url: URL of the connector logo (optional)

        Returns:
            Dictionary formatted for Strapi API with all fields populated
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extract sections
        title = StrapiContentParser._extract_section(content, r'\[Title\]\s*\n(.+?)(?:\n\n|\n\[)', multiline=False)
        one_liner = StrapiContentParser._extract_section(content, r'\[One-line connector statement\]\s*\n(.+?)(?:\n\n|\n\[)', multiline=False)
        overview = StrapiContentParser._extract_section(content, r'\[Overview paragraph\]\s*\n(.+?)(?:\n\n|\n\[)', multiline=False)
        capabilities = StrapiContentParser._extract_section(content, r'\[Core Capabilities\]\s*\n(.+?)(?:\n\n|\n\[)', multiline=True)
        workflows = StrapiContentParser._extract_section(content, r'\[Common Automation Workflows\]\s*\n(.+?)(?:\n\n|\n\[)', multiline=True)
        benefits = StrapiContentParser._extract_section(content, r'\[Key Benefits\]\s*\n(.+?)(?:\n\n|\n\[)', multiline=True)
        security = StrapiContentParser._extract_section(content, r'\[Security and Permissions\]\s*\n(.+?)(?:\n\n|\n\[)', multiline=True)
        faqs_text = StrapiContentParser._extract_section(content, r'\[FAQs\]\s*\n(.+?)$', multiline=True)

        # Build full HTML content
        html_content = StrapiContentParser._build_html_content(
            title, one_liner, overview, capabilities, workflows, benefits, security
        )

        # Fallback: if no content was extracted, convert entire file to HTML
        if not html_content or html_content.strip() == "":
            # Convert the entire content to basic HTML
            html_content = f"<div>{content.replace(chr(10), '<br>')}</div>"

        # Generate slug from connector name
        slug = connector_name.lower().replace(' ', '-').replace('(', '').replace(')', '').replace('.', '-')

        # Extract keywords from title and content
        keywords = StrapiContentParser._extract_keywords(title, one_liner, overview)

        # Parse FAQs from generated content, or use fallback
        faqs = StrapiContentParser._parse_faqs(faqs_text)
        if not faqs or len(faqs) < 3:
            # Use fallback FAQs if parsing failed or too few FAQs
            faqs = StrapiContentParser._generate_faqs(connector_name, capabilities, workflows)

        # Match categories and tags based on content
        try:
            matcher = CategoryMatcher()
            category_ids = matcher.match_categories(connector_name, content)
            tag_ids = matcher.match_tags(connector_name, content)
        except Exception as e:
            print(f"   ⚠️  Category/Tag matching failed: {e}")
            category_ids = []
            tag_ids = []

        # Build Strapi API payload matching user's exact JSON structure
        strapi_data = {
            "name": connector_name,
            "heroTitle": title or f"{connector_name} + Ruh AI Integration",
            "description": one_liner or f"Integration between {connector_name} and Ruh AI",
            "slug": slug,
            "icon": logo_url,
            "content": html_content,
            "category": category_ids,
            "tags": tag_ids,
            "faqs": faqs,
            "seo": {
                "metaTitle": (title or f"{connector_name} Integration - Ruh AI")[:60],  # Max 60 chars
                "metaDescription": (one_liner or f"Integrate {connector_name} with Ruh AI for intelligent automation and seamless workflows.")[:160],  # Max 160 chars
                "metaImage": logo_url,
                "keywords": keywords,
                "metaRobots": "index follow",  # NO COMMA - regex validation [^,]+
                "metaViewport": "width=device-width initial-scale=1",  # NO COMMA
                "canonicalURL": f"https://ruh.ai/integrations/{slug}",
                "structuredData": {
                    "@context": "https://schema.org",
                    "@type": "SoftwareApplication",
                    "name": f"{connector_name} + Ruh AI Integration",
                    "description": (one_liner or f"Integrate {connector_name} with Ruh AI")[:200]
                },
                "openGraph": {
                    "ogTitle": (title or f"{connector_name} + Ruh AI Integration")[:70],  # Required, max 70 chars
                    "ogDescription": (one_liner or f"Integrate {connector_name} with Ruh AI for intelligent automation.")[:200],  # Required, max 200 chars
                    "ogImage": logo_url,
                    "ogUrl": f"https://ruh.ai/integrations/{slug}",
                    "ogType": "website"
                },
                "twitterCard": {
                    "twitterCard": "summary_large_image",
                    "twitterTitle": (title or f"{connector_name} + Ruh AI")[:70],
                    "twitterDescription": (one_liner or f"Integrate {connector_name} with Ruh AI for intelligent automation.")[:200],
                    "twitterImage": logo_url,
                    "twitterSite": "@ruh_ai",
                    "twitterCreator": "@ruh_ai"
                }
            },
            "publishedAt": datetime.utcnow().isoformat() + "Z"
        }

        return strapi_data

    @staticmethod
    def _extract_section(content: str, pattern: str, multiline: bool = False) -> Optional[str]:
        """Extract a section from the content using regex"""
        flags = re.DOTALL if multiline else 0
        match = re.search(pattern, content, flags)
        if match:
            return match.group(1).strip()
        return None

    @staticmethod
    def _build_html_content(title, one_liner, overview, capabilities, workflows, benefits, security) -> str:
        """Build full HTML content from sections (excluding title and one-liner to avoid duplication)"""
        html_parts = []

        # Skip title and one_liner as they're sent separately in heroTitle and description
        # Start content from Overview section

        if overview:
            html_parts.append(f"<h2>Overview</h2><p>{overview}</p>")
        
        if capabilities:
            html_parts.append("<h2>Core Capabilities</h2>")
            html_parts.append(StrapiContentParser._convert_bullets_to_html(capabilities))
        
        if workflows:
            html_parts.append("<h2>Common Automation Workflows</h2>")
            html_parts.append(StrapiContentParser._convert_bullets_to_html(workflows))
        
        if benefits:
            html_parts.append("<h2>Key Benefits</h2>")
            html_parts.append(StrapiContentParser._convert_bullets_to_html(benefits))
        
        if security:
            html_parts.append(f"<h2>Security and Permissions</h2><p>{security}</p>")

        return "\n".join(html_parts)

    @staticmethod
    def _convert_bullets_to_html(text: str) -> str:
        """Convert bullet points to HTML list with semi-bold labels wrapped in <p>"""
        lines = text.split('\n')
        html_items = []

        for line in lines:
            line = line.strip()
            if line.startswith('*'):
                item = line[1:].strip()

                # Check if item has a colon (label: description format)
                if ':' in item:
                    # Split at first colon
                    parts = item.split(':', 1)
                    label = parts[0].strip()
                    description = parts[1].strip()
                    # Make label semi-bold with font-weight: 600, wrapped in <p>
                    html_items.append(f"<li><p><span style='font-weight: 600;'>{label}:</span> {description}</p></li>")
                else:
                    # No colon, just regular list item wrapped in <p>
                    html_items.append(f"<li><p>{item}</p></li>")

        if html_items:
            return "<ul>\n" + "\n".join(html_items) + "\n</ul>"
        return f"<p>{text}</p>"

    @staticmethod
    def _extract_keywords(title: str, one_liner: str, overview: str) -> str:
        """Extract keywords from content"""
        keywords = set()
        
        # Common words to exclude
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
        
        # Extract from title
        if title:
            words = re.findall(r'\b[a-zA-Z]{4,}\b', title.lower())
            keywords.update([w for w in words if w not in stop_words])
        
        # Add common integration keywords
        keywords.update(['integration', 'automation', 'workflow', 'ruh ai'])
        
        return ', '.join(sorted(keywords)[:15])  # Limit to 15 keywords

    @staticmethod
    def _parse_faqs(faqs_text: str) -> List[Dict[str, str]]:
        """Parse FAQs from generated content"""
        faqs = []

        if not faqs_text:
            return faqs

        # Split by Q: to find individual FAQs
        faq_blocks = re.split(r'\n(?=Q:)', faqs_text.strip())

        for block in faq_blocks:
            block = block.strip()
            if not block:
                continue

            # Extract question and answer
            q_match = re.search(r'Q:\s*(.+?)(?=\nA:)', block, re.DOTALL)
            a_match = re.search(r'A:\s*(.+?)$', block, re.DOTALL)

            if q_match and a_match:
                question = q_match.group(1).strip()
                answer = a_match.group(1).strip()

                faqs.append({
                    "question": question,
                    "answer": answer
                })

        return faqs

    @staticmethod
    def _generate_faqs(connector_name: str, capabilities: str, workflows: str) -> List[Dict[str, str]]:
        """Generate fallback FAQ entries if none were extracted from content"""
        faqs = [
            {
                "question": f"What is {connector_name} integration with Ruh AI?",
                "answer": f"{connector_name} integration with Ruh AI enables seamless automation and data synchronization between {connector_name} and your enterprise systems."
            },
            {
                "question": f"How does {connector_name} integration work?",
                "answer": "The integration uses bi-directional data flow to automatically sync information between systems, reducing manual entry and improving accuracy."
            },
            {
                "question": "Is the integration secure?",
                "answer": "Yes, all data transfers are encrypted in transit and at rest, with OAuth 2.0 authentication ensuring only authorized users can access or modify data."
            },
            {
                "question": f"Can I customize the {connector_name} integration?",
                "answer": "Yes, you can configure which data fields sync, set up custom automation workflows, and control permissions based on your team's needs."
            },
            {
                "question": f"How quickly does data sync between Ruh AI and {connector_name}?",
                "answer": "Data syncs in real-time, ensuring your team always has the most up-to-date information across both platforms."
            }
        ]

        return faqs


# Test the parser
if __name__ == "__main__":
    import json
    
    print("🚀 Testing Strapi Content Parser...")
    
    # Test with a sample file
    test_file = "integration-pages/autobound.txt"
    connector_name = "Autobound"
    
    parser = StrapiContentParser()
    result = parser.parse_integration_page(test_file, connector_name)
    
    print("\n📊 Parsed Data:")
    print(json.dumps(result, indent=2))
    
    print("\n✅ Parser test complete!")

