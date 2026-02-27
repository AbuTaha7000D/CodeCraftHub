# CodeCraftHub API Testing Guide 🚀

This guide provides everything you need to test the **CodeCraftHub** API.

## ✅ Success Scenarios

### 1. Add a New Course (POST)
```bash
curl -X POST http://127.0.0.1:5000/api/courses \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Flask Basics",
    "description": "Learn the fundamentals of Flask",
    "target_date": "2026-04-10",
    "status": "Not Started"
  }'
```

### 2. Get All Courses (GET)
```bash
curl http://127.0.0.1:5000/api/courses
```

### 3. Get Course Statistics (GET) - CHALLENGE
```bash
curl http://127.0.0.1:5000/api/courses/stats
```

### 4. Delete Course (DELETE)
```bash
curl -X DELETE http://127.0.0.1:5000/api/courses/1
```

---

## ❌ Error Scenarios

### 1. Missing Required Fields (400)
```bash
curl -X POST http://127.0.0.1:5000/api/courses \
  -H "Content-Type: application/json" \
  -d '{"name": "Incomplete"}'
```

### 2. Invalid Status (400)
```bash
curl -X POST http://127.0.0.1:5000/api/courses \
  -H "Content-Type: application/json" \
  -d '{"name": "X", "description": "Y", "target_date": "2026-01-01", "status": "Pending"}'
```
