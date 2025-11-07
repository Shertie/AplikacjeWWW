#!/bin/bash

# Test nowej implementacji APIView zgodnie z DRF Tutorial 3
# Po zmianach: Http404 zamiast get_object_or_404, format suffix, metoda get_object()

BASE_URL="http://localhost:8000/api"

echo "========================================="
echo "TEST NOWEJ IMPLEMENTACJI APIView"
echo "Zgodnie z Django REST Framework Tutorial 3"
echo "========================================="
echo ""

echo "1. Test GET - Lista kategorii"
echo "GET ${BASE_URL}/categories/"
curl -s ${BASE_URL}/categories/ | python3 -m json.tool
echo ""

echo "2. Test format suffix - .json"
echo "GET ${BASE_URL}/categories.json"
curl -s ${BASE_URL}/categories.json | python3 -m json.tool
echo ""

echo "3. Test GET - Szczegóły tematu (ID=1)"
echo "GET ${BASE_URL}/topics/1/"
curl -s ${BASE_URL}/topics/1/ | python3 -m json.tool
echo ""

echo "4. Test format suffix dla szczegółów"
echo "GET ${BASE_URL}/topics/1.json"
curl -s ${BASE_URL}/topics/1.json | python3 -m json.tool
echo ""

echo "5. Test obsługi błędów - Http404 (nieistniejący obiekt)"
echo "GET ${BASE_URL}/categories/999/"
echo "Oczekiwany wynik: {\"detail\":\"Not found.\"}"
curl -s ${BASE_URL}/categories/999/
echo ""
echo ""

echo "6. Test metody get_object() - Http404 dla Post"
echo "GET ${BASE_URL}/posts/999.json"
curl -s ${BASE_URL}/posts/999.json
echo ""
echo ""

echo "7. Test wyszukiwania (Search View)"
echo "GET ${BASE_URL}/categories/search/?name=tech"
curl -s "${BASE_URL}/categories/search/?name=tech" | python3 -m json.tool
echo ""

echo "8. Test GET - Lista postów (pusty)"
echo "GET ${BASE_URL}/posts/"
curl -s ${BASE_URL}/posts/ | python3 -m json.tool
echo ""

echo "========================================="
echo "PODSUMOWANIE ZMIAN:"
echo "✓ Użyto APIView zamiast funkcyjnych widoków"
echo "✓ Dodano metodę get_object() w DetailView"
echo "✓ Użyto Http404 zamiast get_object_or_404"
echo "✓ Dodano parametr format=None do metod"
echo "✓ Dodano format_suffix_patterns do URLs"
echo "✓ Dokumentacja zgodna z DRF Tutorial 3"
echo "========================================="
