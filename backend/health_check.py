#!/usr/bin/env python3
"""
Health Check Script for AXYRA NOMINA
Monitorea la salud de la API en producción
"""

import requests
import json
from datetime import datetime
from typing import Dict, List

class HealthChecker:
    def __init__(self, backend_url: str):
        self.backend_url = backend_url
        self.results = []
    
    def check_api_status(self) -> bool:
        """Verifica que la API esté funcionando"""
        try:
            response = requests.get(f"{self.backend_url}/api/status", timeout=5)
            return response.status_code == 200
        except Exception as e:
            print(f"❌ Error conectando a API: {e}")
            return False
    
    def check_health(self) -> bool:
        """Verifica el health check"""
        try:
            response = requests.get(f"{self.backend_url}/health", timeout=5)
            return response.status_code == 200
        except Exception as e:
            print(f"❌ Error en health check: {e}")
            return False
    
    def check_endpoints(self) -> Dict[str, bool]:
        """Verifica todos los endpoints principales"""
        endpoints = {
            "GET /": (requests.get, f"{self.backend_url}/"),
            "GET /health": (requests.get, f"{self.backend_url}/health"),
            "GET /api/status": (requests.get, f"{self.backend_url}/api/status"),
        }
        
        results = {}
        for name, (method, url) in endpoints.items():
            try:
                response = method(url, timeout=5)
                results[name] = response.status_code == 200
                status = "✅" if results[name] else "⚠️"
                print(f"{status} {name}: {response.status_code}")
            except Exception as e:
                results[name] = False
                print(f"❌ {name}: {str(e)}")
        
        return results
    
    def generate_report(self) -> str:
        """Genera un reporte de salud"""
        timestamp = datetime.now().isoformat()
        api_ok = self.check_api_status()
        health_ok = self.check_health()
        endpoints = self.check_endpoints()
        
        report = f"""
╔════════════════════════════════════════════════════════════╗
║           AXYRA NOMINA - HEALTH CHECK REPORT               ║
╚════════════════════════════════════════════════════════════╝

📅 Timestamp: {timestamp}
🌐 Backend URL: {self.backend_url}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔍 VERIFICACIONES:

API Status:    {'✅ OK' if api_ok else '❌ FAIL'}
Health Check:  {'✅ OK' if health_ok else '❌ FAIL'}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 ENDPOINTS:
"""
        for endpoint, ok in endpoints.items():
            status = "✅" if ok else "❌"
            report += f"\n{status} {endpoint}"
        
        overall = all([api_ok, health_ok] + list(endpoints.values()))
        report += f"\n\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        report += f"\n\n{'🟢 SISTEMA OPERACIONAL' if overall else '🔴 SISTEMA CON PROBLEMAS'}"
        report += f"\n\nTiempo de verificación: {datetime.now().isoformat()}"
        
        return report
    
    def continuous_monitoring(self, interval: int = 300):
        """Monitoreo continuo cada X segundos"""
        print(f"📊 Iniciando monitoreo continuo cada {interval} segundos...")
        try:
            while True:
                import time
                print(self.generate_report())
                time.sleep(interval)
        except KeyboardInterrupt:
            print("\n👋 Monitoreo detenido")

if __name__ == "__main__":
    import sys
    
    # Usar URL de producción
    backend_url = sys.argv[1] if len(sys.argv) > 1 else "https://tu-backend-vercel.vercel.app"
    
    checker = HealthChecker(backend_url)
    print(checker.generate_report())
    
    # Descomentar para monitoreo continuo
    # checker.continuous_monitoring(interval=300)
