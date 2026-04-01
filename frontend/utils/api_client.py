"""
API Client - Centralized API communication layer
"""
import requests
from typing import Dict, Any, Optional
from frontend.config import API_HEALTH, API_ANALYZE, API_LIVE_DASHBOARD


class APIClient:
    """Handles all backend API requests with error handling."""
    
    @staticmethod
    def check_health() -> bool:
        """Check if API is alive."""
        try:
            response = requests.get(API_HEALTH, timeout=2)
            return response.status_code == 200
        except Exception:
            return False
    
    @staticmethod
    def analyze_water(payload: Dict[str, float]) -> Optional[Dict[str, Any]]:
        """
        Send water analysis request to backend.
        
        Args:
            payload: Dictionary of RW metrics with aliases
            
        Returns:
            Response JSON or None on error
            
        Raises:
            ConnectionError: If API is unreachable
            ValueError: If payload validation fails
        """
        try:
            response = requests.post(API_ANALYZE, json=payload, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.ConnectionError as e:
            raise ConnectionError(
                f"Cannot reach API at {API_ANALYZE}. Ensure backend is running."
            ) from e
        except requests.exceptions.HTTPError as e:
            raise ValueError(f"API error: {response.text}") from e
        except Exception as e:
            raise Exception(f"Unexpected error: {str(e)}") from e
    
    @staticmethod
    def get_live_dashboard_data() -> Optional[Dict[str, Any]]:
        """
        Get live dashboard data from backend.
        
        Returns:
            Response JSON or None on error
            
        Raises:
            ConnectionError: If API is unreachable
            ValueError: If API returns error
        """
        try:
            response = requests.get(API_LIVE_DASHBOARD, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.ConnectionError as e:
            raise ConnectionError(
                f"Cannot reach API at {API_LIVE_DASHBOARD}. Ensure backend is running."
            ) from e
        except requests.exceptions.HTTPError as e:
            raise ValueError(f"API error: {response.text}") from e
        except Exception as e:
            raise Exception(f"Unexpected error: {str(e)}") from e
