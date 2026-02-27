#!/bin/bash

# CodeCraftHub API Automated Test Script
# This script tests the core CRUD operations and common error cases.

BASE_URL="http://127.0.0.1:5000/api/courses"

echo "🚀 Starting CodeCraftHub API Tests..."
echo "---------------------------------------"

# 1. POST - Create course
echo "1. Testing POST (Create Course)..."
CREATE_RES=$(curl -s -X POST $BASE_URL \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Automated Test Course",
    "description": "Created by bash script",
    "target_date": "2026-12-31",
    "status": "Not Started"
  }')
echo $CREATE_RES | grep -q "Course added successfully!" && echo "✅ Success" || echo "❌ Failed"
COURSE_ID=$(echo $CREATE_RES | sed -n 's/.*"id":\([0-9]*\).*/\1/p')

# 2. GET ALL
echo "2. Testing GET ALL..."
curl -s $BASE_URL | grep -q "\"total\":" && echo "✅ Success" || echo "❌ Failed"

# 3. GET SINGLE
echo "3. Testing GET SINGLE (ID: $COURSE_ID)..."
curl -s "$BASE_URL/$COURSE_ID" | grep -q "\"id\":$COURSE_ID" && echo "✅ Success" || echo "❌ Failed"

# 4. PUT - Update Status
echo "4. Testing PUT (Update Status)..."
curl -s -X PUT "$BASE_URL/$COURSE_ID" \
  -H "Content-Type: application/json" \
  -d '{"status": "In Progress"}' | grep -q "In Progress" && echo "✅ Success" || echo "❌ Failed"

# 5. ERROR - Missing Field
echo "5. Testing ERROR (Missing Description)..."
curl -s -X POST $BASE_URL \
  -H "Content-Type: application/json" \
  -d '{"name": "Fail Test", "target_date": "2026-01-01", "status": "Not Started"}' | grep -q "error" && echo "✅ Success (Caught Error)" || echo "❌ Failed (Error not caught)"

# 6. DELETE
echo "6. Testing DELETE..."
curl -s -X DELETE "$BASE_URL/$COURSE_ID" | grep -q "deleted successfully" && echo "✅ Success" || echo "❌ Failed"

echo "---------------------------------------"
echo "🎉 Tests Completed!"
