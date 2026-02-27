"""
CodeCraftHub - Personalized Learning Platform
Final Lab Version: Includes all CRUD, stats challenge, and robust error handling.

Lab Requirements:
- Python Flask (Flask==3.0.0, Werkzeug==3.0.1)
- Storage: courses.json
- Integer IDs starting from 1
"""

import json
import os
from datetime import datetime, timezone
from flask import Flask, jsonify, request
from flask_cors import CORS

# ─────────────────────────────────────────────────────────────
# 1. App Configuration
# ─────────────────────────────────────────────────────────────

app = Flask(__name__)
# Enable CORS for all routes (necessary for frontend/backend communication on different ports)
CORS(app)

# Data file path
DATA_FILE = "courses.json"

# Allowed course statuses (Enum validation)
VALID_STATUSES = ["Not Started", "In Progress", "Completed"]


# ─────────────────────────────────────────────────────────────
# 2. Database Helpers (Persistence Layer)
# ─────────────────────────────────────────────────────────────

def initialize_database():
    """Create courses.json with an empty list if it doesn't exist."""
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w") as f:
            json.dump([], f)
        print(f"[*] Initialized empty database: {DATA_FILE}")


def load_courses():
    """Load courses from JSON file with error handling."""
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        # If file is missing or corrupted, return empty list
        return []
    except Exception as e:
        # For other unexpected file errors
        raise Exception(f"Failed to read data file: {str(e)}")


def save_courses(courses):
    """Save courses list to JSON file with error handling."""
    try:
        with open(DATA_FILE, "w") as f:
            json.dump(courses, f, indent=2)
    except Exception as e:
        raise Exception(f"Failed to write to data file: {str(e)}")


def get_next_id(courses):
    """Generate the next integer ID based on current max ID."""
    if not courses:
        return 1
    return max(course["id"] for course in courses) + 1


# ─────────────────────────────────────────────────────────────
# 3. API Routes
# ─────────────────────────────────────────────────────────────

@app.route("/", methods=["GET"])
def health_check():
    """Root endpoint to verify the API is running."""
    return jsonify({
        "status": "online",
        "message": "Welcome to CodeCraftHub API",
        "version": "1.0.0"
    }), 200


# --- Phase 2: Create Course (POST) ---
@app.route("/api/courses", methods=["POST"])
def create_course():
    """Create a new course after validating all required fields."""
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400

    # Required field validation
    required = ["name", "description", "target_date", "status"]
    missing = [f for f in required if not data.get(f)]
    if missing:
        return jsonify({"error": f"Missing required fields: {', '.join(missing)}"}), 400

    # Status value validation
    if data["status"] not in VALID_STATUSES:
        return jsonify({"error": f"Invalid status. Must be one of: {VALID_STATUSES}"}), 400

    # Date format validation (YYYY-MM-DD)
    try:
        datetime.strptime(data["target_date"], "%Y-%m-%d")
    except ValueError:
        return jsonify({"error": "Invalid target_date format. Use YYYY-MM-DD"}), 400

    try:
        courses = load_courses()
        new_course = {
            "id": get_next_id(courses),
            "name": data["name"],
            "description": data["description"],
            "target_date": data["target_date"],
            "status": data["status"],
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        courses.append(new_course)
        save_courses(courses)
        return jsonify(new_course), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# --- Phase 2: List All Courses (GET) ---
@app.route("/api/courses", methods=["GET"])
def list_courses():
    """Retrieve all stored courses."""
    try:
        return jsonify(load_courses()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# --- Phase 2: Get One Course (GET) ---
@app.route("/api/courses/<int:course_id>", methods=["GET"])
def get_course(course_id):
    """Retrieve a single course by ID or 404 if not found."""
    courses = load_courses()
    course = next((c for c in courses if c["id"] == course_id), None)
    
    if not course:
        return jsonify({"error": f"Course with ID {course_id} not found"}), 404
    
    return jsonify(course), 200


# --- Phase 2: Update Course (PUT) ---
@app.route("/api/courses/<int:course_id>", methods=["PUT"])
def update_course(course_id):
    """Update existing course fields with validation."""
    data = request.get_json()
    courses = load_courses()
    course_index = next((i for i, c in enumerate(courses) if c["id"] == course_id), None)

    if course_index is None:
        return jsonify({"error": f"Course with ID {course_id} not found"}), 404

    # Update only provided fields
    target_course = courses[course_index]
    
    if "status" in data:
        if data["status"] not in VALID_STATUSES:
            return jsonify({"error": f"Invalid status. Must be one of: {VALID_STATUSES}"}), 400
        target_course["status"] = data["status"]
    
    if "target_date" in data:
        try:
            datetime.strptime(data["target_date"], "%Y-%m-%d")
            target_course["target_date"] = data["target_date"]
        except ValueError:
            return jsonify({"error": "Invalid target_date format. Use YYYY-MM-DD"}), 400

    if "name" in data: target_course["name"] = data["name"]
    if "description" in data: target_course["description"] = data["description"]

    courses[course_index] = target_course
    save_courses(courses)
    return jsonify(target_course), 200


# --- Phase 2: Delete Course (DELETE) ---
@app.route("/api/courses/<int:course_id>", methods=["DELETE"])
def delete_course(course_id):
    """Remove a course from the database."""
    courses = load_courses()
    new_courses = [c for c in courses if c["id"] != course_id]
    
    if len(new_courses) == len(courses):
        return jsonify({"error": f"Course with ID {course_id} not found"}), 404
    
    save_courses(new_courses)
    return jsonify({"message": f"Course {course_id} deleted successfully"}), 200


# --- Phase 6 Challenge: Stats (GET) ---
@app.route("/api/courses/stats", methods=["GET"])
def get_stats():
    """Calculate and return course statistics."""
    courses = load_courses()
    stats = {
        "total": len(courses),
        "by_status": {status: 0 for status in VALID_STATUSES}
    }
    for c in courses:
        stats["by_status"][c["status"]] += 1
    return jsonify(stats), 200


# ─────────────────────────────────────────────────────────────
# 4. App Initialization
# ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    initialize_database()
    print("\n🚀 CodeCraftHub API is starting...")
    print("📍 Local URL: http://127.0.0.1:5000")
    print("🛠️  Press Ctrl+C to stop the server\n")
    app.run(debug=True, port=5000)
