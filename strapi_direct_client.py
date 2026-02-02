"""
Direct Strapi API Client (No MCP)
Publishes integration pages directly to Strapi REST API
"""

import os
import requests
from typing import Dict, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv('.env.python')


class StrapiDirectClient:
    """Direct HTTP client for Strapi API (bypasses MCP)"""

    def __init__(self):
        self.strapi_url = os.getenv('STRAPI_API_URL', 'http://127.0.0.1:8083')
        self.strapi_token = os.getenv('STRAPI_API_TOKEN', '')
        self.api_endpoint = f"{self.strapi_url}/api/v1/integrations"
        
    def publish_integration(self, integration_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Publish integration directly to Strapi REST API
        
        Args:
            integration_data: Dictionary with integration fields
            
        Returns:
            Response from Strapi API
        """
        try:
            # Prepare headers
            headers = {
                'Content-Type': 'application/json',
            }
            
            # Add authentication if token is available
            if self.strapi_token:
                headers['Authorization'] = f'Bearer {self.strapi_token}'
                print("🔑 Using Strapi API token for authentication")
            else:
                print("⚠️  No Strapi API token found - publishing without authentication")
                print("   Set STRAPI_API_TOKEN in .env.python if your Strapi requires auth")
            
            print(f"📤 Publishing to Strapi: {self.api_endpoint}")
            print(f"📝 Integration: {integration_data.get('name', 'Unknown')}")

            # Make POST request (send data directly, not wrapped in {"data": ...})
            response = requests.post(
                self.api_endpoint,
                json=integration_data,
                headers=headers,
                timeout=30
            )
            
            # Check response
            if response.status_code in [200, 201]:
                print(f"✅ Successfully published to Strapi!")
                return {
                    "success": True,
                    "data": response.json(),
                    "status_code": response.status_code
                }
            else:
                print(f"⚠️  Strapi returned status {response.status_code}")
                print(f"   Response: {response.text[:200]}")
                return {
                    "success": False,
                    "error": f"HTTP {response.status_code}: {response.text[:200]}",
                    "status_code": response.status_code
                }
                
        except requests.exceptions.ConnectionError:
            print(f"❌ Cannot connect to Strapi at {self.strapi_url}")
            print(f"   Make sure Strapi is running locally")
            return {
                "success": False,
                "error": "Connection refused - Strapi server not running"
            }
        except requests.exceptions.Timeout:
            print(f"❌ Request to Strapi timed out")
            return {
                "success": False,
                "error": "Request timeout"
            }
        except Exception as e:
            print(f"❌ Error publishing to Strapi: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }


if __name__ == "__main__":
    # Test the client
    print("Testing Direct Strapi Client...")
    print(f"Strapi URL: {os.getenv('STRAPI_API_URL', 'http://127.0.0.1:1337')}")
    print(f"API Token: {'✅ Set' if os.getenv('STRAPI_API_TOKEN') else '❌ Not set'}")
    print()
    
    client = StrapiDirectClient()
    
    # Test data
    test_data = {
        "name": "Test Integration",
        "description": "This is a test integration",
        "content": "Test content for integration page"
    }
    
    result = client.publish_integration(test_data)
    print(f"\nResult: {result}")

