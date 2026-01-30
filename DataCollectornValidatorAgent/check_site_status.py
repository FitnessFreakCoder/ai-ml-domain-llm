import requests

URL = "https://z-lib.sk/"  # Must match BASE_URL in mcp_server.py
TIMEOUT = 10  # seconds

def check_site_status() -> str:
    """
    Check if Z-Library site is accessible.
    Uses HEAD first (lightweight), falls back to GET if HEAD fails.
    """
    try:
        # Try HEAD first (faster, less bandwidth)
        response = requests.head(URL, timeout=TIMEOUT, allow_redirects=True)
        
        # Some sites block HEAD requests, try GET if we get 4xx/5xx
        if response.status_code >= 400:
            response = requests.get(URL, timeout=TIMEOUT, allow_redirects=True)
        
    except requests.exceptions.Timeout:
        return "NOT OK: Request timed out"
    except requests.exceptions.ConnectionError as e:
        return f"NOT OK: Connection failed - {str(e)}"
    except Exception as e:
        return f"NOT OK: {str(e)}"
    
    if response.status_code == 200:
        return "OK"
    elif response.status_code == 503:
        return "NOT OK: Site is temporarily unavailable (503). Try again later."
    elif response.status_code == 403:
        return "NOT OK: Access forbidden (403). Site may be blocking automated requests."
    else:
        return f"NOT OK: HTTP response code {response.status_code}"

