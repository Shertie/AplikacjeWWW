#!/bin/bash

# Test API - skrypt do szybkiego testowania endpointów
# Użycie: ./test_api.sh

BASE_URL="http://localhost:8000/api"

echo "========================================="
echo "TESTY API - Blog Application"
echo "========================================="
echo ""

# Kolory dla lepszej czytelności
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}1. Tworzenie kategorii${NC}"
echo "POST ${BASE_URL}/categories/"
curl -X POST ${BASE_URL}/categories/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Technologia",
    "description": "Artykuły o technologii"
  }' -s | python3 -m json.tool
echo -e "\n"

echo -e "${BLUE}2. Pobieranie listy kategorii${NC}"
echo "GET ${BASE_URL}/categories/"
curl -X GET ${BASE_URL}/categories/ -s | python3 -m json.tool
echo -e "\n"

echo -e "${BLUE}3. Tworzenie tematu${NC}"
echo "POST ${BASE_URL}/topics/"
curl -X POST ${BASE_URL}/topics/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Python i Django",
    "content": "Wszystko o frameworku Django",
    "category": 1
  }' -s | python3 -m json.tool
echo -e "\n"

echo -e "${BLUE}4. DODAWANIE PIERWSZEGO POSTA (z prawidłowym tytułem)${NC}"
echo "POST ${BASE_URL}/posts/"
curl -X POST ${BASE_URL}/posts/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Mój pierwszy artykuł o Django",
    "text": "Django to potężny framework Pythona do tworzenia aplikacji webowych. Pozwala na szybkie tworzenie bezpiecznych i skalowalnych aplikacji.",
    "slug": "moj-pierwszy-artykul",
    "topic": 1,
    "created_by": 1
  }' -s | python3 -m json.tool
echo -e "\n"

echo -e "${BLUE}5. DODAWANIE DRUGIEGO POSTA (z datą z przeszłości)${NC}"
echo "POST ${BASE_URL}/posts/"
curl -X POST ${BASE_URL}/posts/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Analiza danych w Python",
    "text": "Python oferuje wiele bibliotek do analizy danych takich jak Pandas NumPy i Matplotlib które znacząco ułatwiają pracę z dużymi zbiorami danych.",
    "slug": "analiza-danych",
    "topic": 1,
    "created_by": 1,
    "created_at": "2024-01-15T10:30:00Z"
  }' -s | python3 -m json.tool
echo -e "\n"

echo -e "${RED}6. TEST WALIDACJI - Tytuł z cyframi (powinien zwrócić błąd)${NC}"
echo "POST ${BASE_URL}/posts/"
curl -X POST ${BASE_URL}/posts/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Python 3.11 nowości",
    "text": "Nowości w Python 3.11",
    "slug": "python-311",
    "topic": 1,
    "created_by": 1
  }' -s | python3 -m json.tool
echo -e "\n"

echo -e "${RED}7. TEST WALIDACJI - Data z przyszłości (powinien zwrócić błąd)${NC}"
echo "POST ${BASE_URL}/posts/"
curl -X POST ${BASE_URL}/posts/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Przyszły artykuł",
    "text": "Treść artykułu z przyszłości",
    "slug": "przyszly-artykul",
    "topic": 1,
    "created_by": 1,
    "created_at": "2026-12-31T23:59:59Z"
  }' -s | python3 -m json.tool
echo -e "\n"

echo -e "${BLUE}8. Wyświetlanie wszystkich postów${NC}"
echo "GET ${BASE_URL}/posts/"
curl -X GET ${BASE_URL}/posts/ -s | python3 -m json.tool
echo -e "\n"

echo -e "${BLUE}9. MODYFIKACJA PIERWSZEGO POSTA (ID=1)${NC}"
echo "PUT ${BASE_URL}/posts/1/"
curl -X PUT ${BASE_URL}/posts/1/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Zaktualizowany artykuł o Django",
    "text": "Django to świetny framework który został zaktualizowany o nowe funkcje. REST Framework ułatwia tworzenie API.",
    "slug": "zaktualizowany-artykul",
    "topic": 1,
    "created_by": 1
  }' -s | python3 -m json.tool
echo -e "\n"

echo -e "${BLUE}10. Wyświetlanie szczegółów posta (ID=1)${NC}"
echo "GET ${BASE_URL}/posts/1/"
curl -X GET ${BASE_URL}/posts/1/ -s | python3 -m json.tool
echo -e "\n"

echo -e "${BLUE}11. WYSZUKIWANIE POSTÓW Z LITERĄ 'a' W TYTULE${NC}"
echo "GET ${BASE_URL}/posts/search/?name=a"
curl -X GET "${BASE_URL}/posts/search/?name=a" -s | python3 -m json.tool
echo -e "\n"

echo -e "${BLUE}12. Wyszukiwanie kategorii zawierających 'tech'${NC}"
echo "GET ${BASE_URL}/categories/search/?name=tech"
curl -X GET "${BASE_URL}/categories/search/?name=tech" -s | python3 -m json.tool
echo -e "\n"

echo -e "${RED}13. USUWANIE DRUGIEGO POSTA (ID=2)${NC}"
echo "DELETE ${BASE_URL}/posts/2/"
curl -X DELETE ${BASE_URL}/posts/2/ -s -w "\nStatus Code: %{http_code}\n"
echo -e "\n"

echo -e "${BLUE}14. Weryfikacja - wyświetlanie wszystkich postów po usunięciu${NC}"
echo "GET ${BASE_URL}/posts/"
curl -X GET ${BASE_URL}/posts/ -s | python3 -m json.tool
echo -e "\n"

echo "========================================="
echo "TESTY ZAKOŃCZONE"
echo "========================================="
