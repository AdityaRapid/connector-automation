#!/usr/bin/env python3
"""
Integration Page Generator for Ruh.ai
Generates integration pages using LangChain with real Ruh.ai content patterns
"""

import os
import json
import time
import argparse
from pathlib import Path
from typing import Dict, List, Optional
from langchain_simple_agent import RuhAIIntegrationAgent
from strapi_direct_client import StrapiDirectClient
from strapi_content_parser import StrapiContentParser


class IntegrationPageGenerator:
    """Main generator for integration pages"""
    
    def __init__(self, connector_file: str = "connectorList.json", output_dir: str = "integration-pages", enable_strapi: bool = True):
        self.connector_file = connector_file
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.enable_strapi = enable_strapi

        # Initialize the Ruh.ai pattern-based agent
        print("🚀 Initializing Ruh.ai Integration Agent (with real pattern analysis)...")
        self.agent = RuhAIIntegrationAgent()
        print("✅ Agent initialized successfully!\n")

        # Initialize Strapi client if enabled
        if self.enable_strapi:
            print("🚀 Initializing Strapi Direct Client...")
            self.strapi_client = StrapiDirectClient()
            self.content_parser = StrapiContentParser()
            print("✅ Strapi client initialized!\n")
        else:
            self.strapi_client = None
            self.content_parser = None

        # Load connectors
        self.connectors = self._load_connectors()
    
    def _load_connectors(self) -> List[Dict]:
        """Load connectors from JSON file"""
        try:
            with open(self.connector_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Handle both array and object formats
                if isinstance(data, list):
                    return data
                elif isinstance(data, dict) and 'connectors' in data:
                    return data['connectors']
                else:
                    return []
        except Exception as e:
            print(f"❌ Error loading connectors: {e}")
            return []

    def _save_connectors(self):
        """Save updated connectors back to JSON file"""
        try:
            # Save as array format (matching the original structure)
            with open(self.connector_file, 'w', encoding='utf-8') as f:
                json.dump(self.connectors, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"❌ Error saving connectors: {e}")
    
    def _sanitize_filename(self, name: str) -> str:
        """Convert connector name to safe filename"""
        return name.lower().replace(' ', '-').replace('/', '-').replace('\\', '-')
    
    def get_next_unpublished(self) -> Optional[Dict]:
        """Get the next unpublished connector"""
        for connector in self.connectors:
            if not connector.get('published', False):
                return connector
        return None
    
    def get_status(self) -> Dict:
        """Get current generation status"""
        total = len(self.connectors)
        published = sum(1 for c in self.connectors if c.get('published', False))
        unpublished = total - published
        
        next_connector = self.get_next_unpublished()
        next_name = next_connector['name'] if next_connector else "None"
        
        return {
            'total': total,
            'published': published,
            'unpublished': unpublished,
            'next': next_name
        }
    
    def generate_page(self, connector: Dict) -> bool:
        """Generate integration page for a single connector"""
        name = connector['name']
        filename = self._sanitize_filename(name) + '.txt'
        output_path = self.output_dir / filename

        print(f"📝 Generating page for: {name}")

        try:
            # Generate content using LangChain agent
            content = self.agent.generate_integration_page(name)

            if not content:
                print(f"❌ Failed to generate content for {name}")
                return False

            # Save to file
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content)

            print(f"✅ Saved to: {output_path}")

            # Publish to Strapi if enabled
            if self.enable_strapi and self.strapi_client and self.content_parser:
                print(f"\n📤 Publishing to Strapi CMS...")
                try:
                    # Get logo URL from connector data
                    logo_url = connector.get('logo', '')

                    # Parse content for Strapi format
                    strapi_data = self.content_parser.parse_integration_page(str(output_path), name, logo_url)

                    # Publish to Strapi
                    result = self.strapi_client.publish_integration(strapi_data)

                    if result.get('success'):
                        print(f"✅ Successfully published to Strapi!")
                    else:
                        print(f"⚠️  Strapi publishing failed: {result.get('error', 'Unknown error')}")
                        print(f"   Content saved locally, you can retry publishing later.")

                except Exception as e:
                    print(f"⚠️  Strapi publishing error: {str(e)}")
                    print(f"   Content saved locally, you can retry publishing later.")

            # Mark as published
            connector['published'] = True
            self._save_connectors()

            return True

        except Exception as e:
            print(f"❌ Error generating page for {name}: {e}")
            return False
    
    def generate_next(self) -> bool:
        """Generate the next unpublished integration page"""
        connector = self.get_next_unpublished()
        
        if not connector:
            print("🎉 All connectors have been published!")
            return False
        
        return self.generate_page(connector)
    
    def generate_batch(self, count: int, delay: int = 2):
        """Generate multiple integration pages"""
        print(f"🚀 Starting batch generation of {count} pages...\n")
        
        successful = 0
        failed = 0
        
        for i in range(count):
            connector = self.get_next_unpublished()
            
            if not connector:
                print("\n🎉 All connectors have been published!")
                break
            
            print(f"\n[{i+1}/{count}] ", end="")
            
            if self.generate_page(connector):
                successful += 1
            else:
                failed += 1
            
            # Rate limiting
            if i < count - 1:
                print(f"⏳ Waiting {delay} seconds...")
                time.sleep(delay)
        
        print(f"\n{'='*60}")
        print(f"📊 Batch Complete!")
        print(f"✅ Successful: {successful}")
        print(f"❌ Failed: {failed}")
        print(f"{'='*60}\n")
        
        self.print_status()
    
    def print_status(self):
        """Print current status"""
        status = self.get_status()
        
        print(f"\n{'='*60}")
        print(f"📊 Current Status:")
        print(f"{'='*60}")
        print(f"Total Connectors:     {status['total']}")
        print(f"Published:            {status['published']} ✅")
        print(f"Unpublished:          {status['unpublished']}")
        print(f"Next to Process:      {status['next']}")
        print(f"{'='*60}\n")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description='Generate SEO-optimized integration pages for Ruh.ai')
    parser.add_argument('command', choices=['next', 'batch', 'status'], 
                       help='Command to execute')
    parser.add_argument('count', nargs='?', type=int, default=1,
                       help='Number of pages to generate (for batch command)')
    parser.add_argument('--delay', type=int, default=2,
                       help='Delay between requests in seconds (default: 2)')
    
    args = parser.parse_args()
    
    # Initialize generator
    generator = IntegrationPageGenerator()
    
    # Execute command
    if args.command == 'status':
        generator.print_status()
    
    elif args.command == 'next':
        generator.generate_next()
        generator.print_status()
    
    elif args.command == 'batch':
        generator.generate_batch(args.count, args.delay)


if __name__ == "__main__":
    main()

