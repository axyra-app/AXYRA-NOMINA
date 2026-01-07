#!/usr/bin/env python3
"""
Script para probar los endpoints GET del backend
"""

import requests
import json
from datetime import datetime
import sys

BASE_URL = "http://localhost:8000"

# Colores para output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_test(name, passed, response=None):
    """Imprime resultado de prueba"""
    status = f"{Colors.OKGREEN}PASS{Colors.ENDC}" if passed else f"{Colors.FAIL}FAIL{Colors.ENDC}"
    print(f"[{status}] {name}")
    if response and not passed:
        print(f"     Response: {response[:200]}")

def test_health():
    """Prueba endpoint de salud"""
    try:
        resp = requests.get(f"{BASE_URL}/health")
        passed = resp.status_code == 200
        print_test("Health Check", passed, resp.text)
        return resp.json() if resp.ok else None
    except Exception as e:
        print_test("Health Check", False, str(e))
        return None

def test_api_status():
    """Prueba API status"""
    try:
        resp = requests.get(f"{BASE_URL}/api/status")
        passed = resp.status_code == 200
        print_test("API Status", passed, resp.text)
        if resp.ok:
            data = resp.json()
            print(f"     Firebase: {data.get('firebase', 'unknown')}")
            print(f"     Database: {data.get('database', 'unknown')}")
    except Exception as e:
        print_test("API Status", False, str(e))

def test_signup():
    """Test registro de usuario"""
    try:
        email = f"test_{datetime.now().timestamp()}@test.com"
        payload = {
            "email": email,
            "password": "Test123!@#",
            "nombre": "Test User"
        }
        resp = requests.post(f"{BASE_URL}/api/auth/signup", json=payload)
        passed = resp.status_code in [200, 201, 409]  # 409 si ya existe
        print_test("Signup", passed, resp.text)
        
        if resp.ok:
            data = resp.json()
            return data.get("access_token"), email
    except Exception as e:
        print_test("Signup", False, str(e))
    return None, None

def test_login(email, password="Test123!@#"):
    """Test login de usuario"""
    try:
        payload = {
            "email": email,
            "password": password
        }
        resp = requests.post(f"{BASE_URL}/api/auth/login", json=payload)
        passed = resp.status_code == 200
        print_test("Login", passed, resp.text)
        
        if resp.ok:
            data = resp.json()
            return data.get("access_token")
    except Exception as e:
        print_test("Login", False, str(e))
    return None

def test_get_endpoints(token):
    """Prueba endpoints GET con autenticacion"""
    if not token:
        print(f"{Colors.WARNING}No token available, skipping authenticated tests{Colors.ENDC}")
        return
    
    headers = {"Authorization": f"Bearer {token}"}
    client_id = "test-client"
    
    endpoints = [
        ("GET /api/employees", f"{BASE_URL}/api/employees?client_id={client_id}"),
        ("GET /api/hours", f"{BASE_URL}/api/hours?client_id={client_id}"),
        ("GET /api/payroll/history", f"{BASE_URL}/api/payroll/history?client_id={client_id}"),
        ("GET /api/config/system", f"{BASE_URL}/api/config/system?client_id={client_id}"),
    ]
    
    for name, url in endpoints:
        try:
            resp = requests.get(url, headers=headers)
            passed = resp.status_code in [200, 404]  # 404 es OK si no hay datos
            print_test(name, passed, resp.text[:100])
            if resp.ok and resp.text:
                try:
                    data = resp.json()
                    print(f"     Data type: {type(data).__name__}, Items: {len(data) if isinstance(data, (list, dict)) else 'N/A'}")
                except:
                    pass
        except Exception as e:
            print_test(name, False, str(e))

def main():
    """Main test runner"""
    print(f"\n{Colors.BOLD}{Colors.HEADER}=== Backend API Test Suite ==={Colors.ENDC}\n")
    
    print(f"{Colors.BOLD}1. Testing Server Health{Colors.ENDC}")
    health = test_health()
    if not health:
        print(f"\n{Colors.FAIL}Backend server is not running on {BASE_URL}{Colors.ENDC}")
        print(f"Please start the backend server first.")
        sys.exit(1)
    
    print(f"\n{Colors.BOLD}2. Testing API Status{Colors.ENDC}")
    test_api_status()
    
    print(f"\n{Colors.BOLD}3. Testing Authentication{Colors.ENDC}")
    token, email = test_signup()
    if not token:
        token = test_login("test@example.com")
    
    print(f"\n{Colors.BOLD}4. Testing GET Endpoints{Colors.ENDC}")
    test_get_endpoints(token)
    
    print(f"\n{Colors.BOLD}{Colors.OKGREEN}Test suite completed!{Colors.ENDC}\n")

if __name__ == "__main__":
    main()
