import pytest

def run_backend_tests():
    print("🧪 Lancement des tests backend...")
    result = pytest.main(["backend/tests/test_api.py", "-v"])
    if result != 0:
        raise Exception("❌ Échec des tests backend.")
    print("✅ Tous les tests backend sont passés avec succès.")

def run_frontend_tests():
    print("🧪 Lancement des tests frontend...")
    result = pytest.main(["frontend/test_frontend.py", "-v"])
    if result != 0:
        raise Exception("❌ Échec des tests frontend.")
    print("✅ Tous les tests frontend sont passés avec succès.")
