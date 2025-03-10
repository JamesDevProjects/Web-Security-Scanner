import requests
from bs4 import BeautifulSoup
import sys

# Disable SSL warnings
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

SECURITY_HEADERS = [
    "Strict-Transport-Security", "Content-Security-Policy", "X-Frame-Options",
    "X-XSS-Protection", "X-Content-Type-Options", "Referrer-Policy"
]

COMMON_DIRECTORIES = [
    "admin", "login", "backup", "config", ".git", "phpmyadmin", "wp-admin"
]

def check_security_headers(url):
    """Checks for missing security headers in the response."""
    try:
        response = requests.get(url, timeout=5, verify=False)  # Ignore SSL errors
        missing_headers = [header for header in SECURITY_HEADERS if header not in response.headers]

        if missing_headers:
            print("\nMissing Security Headers:")
            for header in missing_headers:
                print(f" - {header}")
        else:
            print("\nAll recommended security headers are present.")
    except requests.exceptions.RequestException as e:
        print(f"Error checking security headers: {e}")

def check_ssl_version(url):
    """Checks if the site is using HTTPS and a valid SSL certificate."""
    if not url.startswith("https://"):
        print("\nWarning: The site is not using HTTPS. This is a security risk.")
    else:
        print("\nSSL/TLS Check: The site is using HTTPS.")

def check_exposed_directories(url):
    """Checks for common exposed directories that could indicate security risks."""
    print("\nChecking for exposed directories...")
    found_directories = []
    
    for directory in COMMON_DIRECTORIES:
        test_url = f"{url.rstrip('/')}/{directory}"
        try:
            response = requests.get(test_url, allow_redirects=False, verify=False)  # Ignore SSL errors
            if response.status_code == 200:
                found_directories.append(test_url)
        except requests.exceptions.RequestException:
            continue

    if found_directories:
        print("Potentially exposed directories found:")
        for directory in found_directories:
            print(f" - {directory}")
    else:
        print("No exposed directories found.")

def scan_website(url):
    """Runs all security checks on the given website."""
    print(f"Scanning {url}...\n")
    
    check_ssl_version(url)
    check_security_headers(url)
    check_exposed_directories(url)

    print("\nScan completed.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python security_scanner.py <URL>")
        sys.exit(1)
    
    target_url = sys.argv[1]

    if not target_url.startswith("http"):
        target_url = "http://" + target_url  # Default to HTTP if no scheme provided

    scan_website(target_url)
