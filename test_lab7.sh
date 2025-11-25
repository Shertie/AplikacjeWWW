#!/bin/bash

echo "========================================================"
echo "TEST LAB 7 - UPRAWNIENIA"
echo "========================================================"

BASE_URL="http://localhost:8001/api"

# IDs
CAT_ID=1 
POST_ID=3 

echo "--- ZADANIE 1 & 2: Sprawdzenie uprawnienia view_category ---"
echo "1. lab7user (ma uprawnienie) - GET /categories/$CAT_ID/simple/"
CODE=$(curl -s -o /dev/null -w "%{http_code}" -u lab7user:testpass123 "$BASE_URL/categories/$CAT_ID/simple/")
echo "   Kod: $CODE (Oczekiwane: 200)"

echo "2. testuser (brak uprawnienia) - GET /categories/$CAT_ID/simple/"
CODE=$(curl -s -o /dev/null -w "%{http_code}" -u testuser:testpass123 "$BASE_URL/categories/$CAT_ID/simple/")
echo "   Kod: $CODE (Oczekiwane: 403)"

echo ""
echo "--- ZADANIE 3: Custom permission can_edit_others_posts ---"
echo "1. moderator (ma uprawnienie) - PUT /posts/$POST_ID/moderator/"
# Note: We expect 200 or 400 (if validation fails), but NOT 403
CODE=$(curl -s -o /dev/null -w "%{http_code}" -X PUT -u moderator:testpass123 \
  -H "Content-Type: application/json" \
  -d '{"title":"Edited by Moderator","text":"Content","slug":"slug","topic":1}' \
  "$BASE_URL/posts/$POST_ID/moderator/")
echo "   Kod: $CODE (Oczekiwane: 200 lub 400)"

echo "2. lab7user (brak uprawnienia) - PUT /posts/$POST_ID/moderator/"
CODE=$(curl -s -o /dev/null -w "%{http_code}" -X PUT -u lab7user:testpass123 \
  -H "Content-Type: application/json" \
  -d '{"title":"Edited by Lab7User","text":"Content","slug":"slug","topic":1}' \
  "$BASE_URL/posts/$POST_ID/moderator/")
echo "   Kod: $CODE (Oczekiwane: 403)"

echo ""
echo "--- ZADANIE 4: CustomDjangoModelPermissions ---"
echo "1. lab7user (ma view_category) - GET /categories/$CAT_ID/permissions/"
CODE=$(curl -s -o /dev/null -w "%{http_code}" -u lab7user:testpass123 "$BASE_URL/categories/$CAT_ID/permissions/")
echo "   Kod: $CODE (Oczekiwane: 200)"

echo "2. lab7user (brak change_category) - PUT /categories/$CAT_ID/permissions/"
CODE=$(curl -s -o /dev/null -w "%{http_code}" -X PUT -u lab7user:testpass123 \
  -H "Content-Type: application/json" \
  -d '{"name":"New Name"}' \
  "$BASE_URL/categories/$CAT_ID/permissions/")
echo "   Kod: $CODE (Oczekiwane: 403)"

echo "3. testuser (brak view_category) - GET /categories/$CAT_ID/permissions/"
CODE=$(curl -s -o /dev/null -w "%{http_code}" -u testuser:testpass123 "$BASE_URL/categories/$CAT_ID/permissions/")
echo "   Kod: $CODE (Oczekiwane: 403)"
