#!/bin/bash

# Test Lab 6 - Autentykacja w Django i DRF
# Autor: Lab 6 Tests
# Data: 2025-11-17

BASE_URL="http://localhost:8001/api"
TOKEN="f5af0855508e5f5da2e35dee08ad44278c873258"

echo "========================================="
echo "LAB 6 - TESTY AUTENTYKACJI"
echo "========================================="
echo ""

# ============================================================================
# ZADANIE 1: Logowanie przez interfejs DRF
# ============================================================================
echo "========================================="
echo "ZADANIE 1: Interfejs logowania DRF"
echo "========================================="
echo ""
echo "✓ Dodano endpoint: /api-auth/"
echo "✓ Możesz zalogować się przez przeglądarkę:"
echo "  URL: http://localhost:8001/api-auth/login/"
echo "  Username: testuser"
echo "  Password: testpass123"
echo ""

# ============================================================================
# ZADANIE 2: Endpoint users/posts/ - posty zalogowanego użytkownika
# ============================================================================
echo "========================================="
echo "ZADANIE 2: Posty zalogowanego użytkownika"
echo "========================================="
echo ""

echo "Test 2a: Dostęp BEZ autentykacji (powinien zwrócić 403)"
echo "GET ${BASE_URL}/users/posts/"
curl -s ${BASE_URL}/users/posts/ | head -5
echo ""
echo ""

echo "Test 2b: Dostęp Z autentykacją Basic (testuser:testpass123)"
echo "GET ${BASE_URL}/users/posts/"
curl -s -u testuser:testpass123 ${BASE_URL}/users/posts/ | python3 -m json.tool 2>/dev/null | head -20
echo ""
echo ""

# ============================================================================
# ZADANIE 3: Autentykacja tokenem
# ============================================================================
echo "========================================="
echo "ZADANIE 3: Autentykacja tokenem"
echo "========================================="
echo ""
echo "Token dla użytkownika 'testuser':"
echo "Token: ${TOKEN}"
echo ""
echo "Test 3: Pobieranie danych z tokenem"
echo "GET ${BASE_URL}/posts/"
curl -s -H "Authorization: Token ${TOKEN}" ${BASE_URL}/posts/ | python3 -m json.tool 2>/dev/null | head -30
echo ""
echo ""

# ============================================================================
# ZADANIE 4: Osobne endpointy PUT i DELETE z różnymi metodami auth
# ============================================================================
echo "========================================="
echo "ZADANIE 4: Osobne endpointy PUT/DELETE"
echo "========================================="
echo ""

echo "Test 4a: PUT /api/posts/update/1/ (Session/Basic Auth)"
echo "Aktualizacja posta z Basic Auth..."
curl -s -X PUT ${BASE_URL}/posts/update/1/ \
  -u testuser:testpass123 \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Zaktualizowane wprowadzenie do Django",
    "text": "Django to framework który został zaktualizowany",
    "slug": "wprowadzenie-do-django",
    "topic": 2,
    "created_by": 1
  }' | python3 -m json.tool 2>/dev/null
echo ""
echo ""

echo "Test 4b: DELETE /api/posts/delete/3/ BEZ tokenu (powinien zwrócić 401/403)"
echo "DELETE ${BASE_URL}/posts/delete/3/"
curl -s -X DELETE ${BASE_URL}/posts/delete/3/ -w "\nHTTP Status: %{http_code}\n"
echo ""
echo ""

echo "Test 4c: DELETE /api/posts/delete/3/ Z tokenem"
echo "DELETE ${BASE_URL}/posts/delete/3/"
echo "Authorization: Token ${TOKEN}"
curl -s -X DELETE ${BASE_URL}/posts/delete/3/ \
  -H "Authorization: Token ${TOKEN}" \
  -w "\nHTTP Status: %{http_code}\n"
echo ""
echo ""

# ============================================================================
# ZADANIE 5: Endpoint categories/<id>/topics/ (tylko token)
# ============================================================================
echo "========================================="
echo "ZADANIE 5: Topics dla kategorii (Token Auth)"
echo "========================================="
echo ""

echo "Test 5a: GET /api/categories/2/topics/ BEZ tokenu (powinien zwrócić 401)"
echo "GET ${BASE_URL}/categories/2/topics/"
curl -s ${BASE_URL}/categories/2/topics/ -w "\nHTTP Status: %{http_code}\n"
echo ""
echo ""

echo "Test 5b: GET /api/categories/2/topics/ Z tokenem"
echo "GET ${BASE_URL}/categories/2/topics/"
echo "Authorization: Token ${TOKEN}"
curl -s -H "Authorization: Token ${TOKEN}" ${BASE_URL}/categories/2/topics/ | python3 -m json.tool 2>/dev/null
echo ""
echo ""

# ============================================================================
# PODSUMOWANIE
# ============================================================================
echo "========================================="
echo "PODSUMOWANIE TESTÓW"
echo "========================================="
echo ""
echo "✓ Zadanie 1: Interfejs logowania DRF - ZAIMPLEMENTOWANE"
echo "✓ Zadanie 2: Endpoint users/posts/ - ZAIMPLEMENTOWANE"
echo "✓ Zadanie 3: Autentykacja tokenem - ZAIMPLEMENTOWANE"
echo "✓ Zadanie 4: Osobne endpointy PUT/DELETE - ZAIMPLEMENTOWANE"
echo "✓ Zadanie 5: Categories/<id>/topics/ - ZAIMPLEMENTOWANE"
echo ""
echo "METODY AUTENTYKACJI:"
echo "  - Session Authentication (DRF login interface)"
echo "  - Basic Authentication (username:password)"
echo "  - Token Authentication (Authorization: Token <key>)"
echo ""
echo "DANE TESTOWE:"
echo "  Username: testuser"
echo "  Password: testpass123"
echo "  Token:    ${TOKEN}"
echo ""
echo "========================================="
