#!/usr/bin/env python3

import requests
import sys
import time

def check_api_server():
    """Check if the Flask API server is running"""
    try:
        response = requests.get("http://localhost:5000/api/status", timeout=5)
        if response.status_code == 200:
            print("✅ API server is running")
            return True
        else:
            print(f"❌ API server returned status code {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to API server at http://localhost:5000")
        return False
    except Exception as e:
        print(f"❌ Error checking API server: {e}")
        return False

def check_frontend_server():
    """Check if the Next.js frontend server is running"""
    try:
        response = requests.get("http://localhost:3000", timeout=5)
        if response.status_code == 200:
            print("✅ Frontend server is running")
            return True
        else:
            print(f"❌ Frontend server returned status code {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to frontend server at http://localhost:3000")
        return False
    except Exception as e:
        print(f"❌ Error checking frontend server: {e}")
        return False

if __name__ == "__main__":
    print("Checking server connectivity...")
    
    api_status = check_api_server()
    frontend_status = check_frontend_server()
    
    if api_status and frontend_status:
        print("\n✅ All systems ready! You can access the application at http://localhost:3000")
        sys.exit(0)
    else:
        print("\n❌ Some services are not running:")
        if not api_status:
            print("  - Make sure the API server is running: python cryptoreason/api_wrapper.py")
        if not frontend_status:
            print("  - Make sure the Next.js server is running: npm run dev")
        print("\nYou can use ./start.sh to start both servers automatically.")
        sys.exit(1) 