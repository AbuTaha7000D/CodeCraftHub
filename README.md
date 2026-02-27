# CodeCraftHub 🛠️

A beginner-friendly learning platform to track your developer journey.

## 🌟 Features
- **Full CRUD API** for course management.
- **Statistics Dashboard**: View course progress totals.
- **JSON Storage**: Simple file-based persistence.
- **Error Handling**: Comprehensive 400/404/500 scenarios.

## 📂 Installation & Run
1. **Clone/Create Directory**: `mkdir CodeCraftHub && cd CodeCraftHub`
2. **Install Dependencies**: `pip install -r requirements.txt`
3. **Run App**: `python app.py`

## 🔗 API Reference
| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/courses` | Create a course |
| GET | `/api/courses` | List all courses |
| GET | `/api/courses/<id>` | Get details |
| PUT | `/api/courses/<id>` | Update progress |
| DELETE | `/api/courses/<id>` | Remove course |
| GET | `/api/courses/stats` | View progress stats |

---
*Created for the CodeCraftHub REST API Lab.*
