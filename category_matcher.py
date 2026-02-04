"""
Category and Tag Matcher
Automatically assigns relevant category IDs and tag IDs to integrations based on content analysis
"""

import json
from typing import List, Dict, Any


class CategoryMatcher:
    """Matches integrations to relevant categories and tags based on content"""

    def __init__(self, categories_file: str = "categories.json", tags_file: str = "tags.json"):
        """Initialize with categories and tags from JSON files"""
        with open(categories_file, 'r', encoding='utf-8') as f:
            self.categories = json.load(f)

        with open(tags_file, 'r', encoding='utf-8') as f:
            self.tags = json.load(f)
    
    def match_categories(self, connector_name: str, content: str, max_categories: int = 3) -> List[int]:
        """
        Match integration to relevant categories based on name and content
        
        Args:
            connector_name: Name of the connector/integration
            content: Full content of the integration page
            max_categories: Maximum number of categories to return (default: 3)
        
        Returns:
            List of category IDs (e.g., [8, 12, 15])
        """
        # Combine connector name and content for analysis
        text_to_analyze = f"{connector_name.lower()} {content.lower()}"
        
        # Score each category based on keyword matches
        category_scores = []
        
        for category in self.categories:
            score = 0
            matched_keywords = []
            
            # Check each keyword for this category
            for keyword in category['keywords']:
                keyword_lower = keyword.lower()
                
                # Count occurrences of keyword in text
                count = text_to_analyze.count(keyword_lower)
                
                if count > 0:
                    # Weight by frequency and keyword importance
                    # Exact connector name match gets higher weight
                    if keyword_lower in connector_name.lower():
                        score += count * 10
                    else:
                        score += count * 2
                    
                    matched_keywords.append(keyword)
            
            if score > 0:
                category_scores.append({
                    'id': category['id'],
                    'name': category['name'],
                    'score': score,
                    'matched_keywords': matched_keywords
                })
        
        # Sort by score (highest first)
        category_scores.sort(key=lambda x: x['score'], reverse=True)
        
        # Return top N category IDs
        top_categories = category_scores[:max_categories]
        category_ids = [cat['id'] for cat in top_categories]
        
        # Log matched categories for debugging
        if category_ids:
            print(f"   📂 Matched Categories: {', '.join([cat['name'] for cat in top_categories])}")
        
        return category_ids
    
    def get_category_by_id(self, category_id: int) -> Dict[str, Any]:
        """Get category details by ID"""
        for category in self.categories:
            if category['id'] == category_id:
                return category
        return None
    
    def get_all_categories(self) -> List[Dict[str, Any]]:
        """Get all available categories"""
        return self.categories

    def match_tags(self, connector_name: str, content: str, max_tags: int = 2) -> List[int]:
        """
        Match integration to relevant tags based on name and content

        Args:
            connector_name: Name of the connector/integration
            content: Full content of the integration page
            max_tags: Maximum number of tags to return (default: 2)

        Returns:
            List of tag IDs (e.g., [1, 2])
        """
        # Combine connector name and content for analysis
        text_to_analyze = f"{connector_name.lower()} {content.lower()}"

        # Score each tag based on keyword matches
        tag_scores = []

        for tag in self.tags:
            score = 0
            matched_keywords = []

            # Check each keyword for this tag
            for keyword in tag['keywords']:
                keyword_lower = keyword.lower()

                # Count occurrences of keyword in text
                count = text_to_analyze.count(keyword_lower)

                if count > 0:
                    # Weight by frequency
                    if keyword_lower in connector_name.lower():
                        score += count * 10
                    else:
                        score += count * 2

                    matched_keywords.append(keyword)

            if score > 0:
                tag_scores.append({
                    'id': tag['id'],
                    'name': tag['name'],
                    'score': score,
                    'matched_keywords': matched_keywords
                })

        # Sort by score (highest first)
        tag_scores.sort(key=lambda x: x['score'], reverse=True)

        # Return top N tag IDs
        top_tags = tag_scores[:max_tags]
        tag_ids = [tag['id'] for tag in top_tags]

        # Log matched tags for debugging
        if tag_ids:
            print(f"   🏷️  Matched Tags: {', '.join([tag['name'] for tag in top_tags])}")

        return tag_ids

    def get_tag_by_id(self, tag_id: int) -> Dict[str, Any]:
        """Get tag details by ID"""
        for tag in self.tags:
            if tag['id'] == tag_id:
                return tag
        return None

    def get_all_tags(self) -> List[Dict[str, Any]]:
        """Get all available tags"""
        return self.tags


# Example usage
if __name__ == "__main__":
    matcher = CategoryMatcher()

    # Test with HubSpot
    test_content = """
    HubSpot is a CRM platform that helps manage customer relationships, sales pipelines,
    and marketing campaigns. It includes contact management, deal tracking, and email integration.
    The connector provides API access and webhook support for real-time sync.
    """

    categories = matcher.match_categories("HubSpot", test_content)
    tags = matcher.match_tags("HubSpot", test_content)
    print(f"HubSpot categories: {categories}")
    print(f"HubSpot tags: {tags}")

    # Test with Calendly
    test_content2 = """
    Calendly is a scheduling tool that helps you book meetings and appointments.
    It integrates with your calendar to show availability and automate scheduling.
    Native integration with Google Calendar and Outlook.
    """

    categories2 = matcher.match_categories("Calendly", test_content2)
    tags2 = matcher.match_tags("Calendly", test_content2)
    print(f"\nCalendly categories: {categories2}")
    print(f"Calendly tags: {tags2}")

