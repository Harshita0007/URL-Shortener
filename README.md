🔗 URL Shortener
A simple Flask-based URL shortening service that lets users shorten long URLs, redirect using a short code, and track analytics.

🚀 Getting Started
✅ Prerequisites
Python 3.8 or higher

pip for installing dependencies

⚙️ Setup Instructions
bash
Copy
Edit
# Clone or download the repository
cd url-shortener

# Create virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python -m flask --app app.main run
The app will be available at: http://localhost:5000

📌 Features
1. Shorten URL
POST /api/shorten

Accepts a long URL and returns a unique 6-character short code.

Example:

bash
Copy
Edit
curl -X POST http://localhost:5000/api/shorten \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}'
2. Redirect
GET /<short_code>

Redirects the user to the original long URL.

Increments the click count.

3. Analytics
GET /api/stats/<short_code>
Returns:
Original long URL
Total click count
Creation timestamp


✅ Functional Highlights
6-character alphanumeric short codes
In-memory storage for mapping URLs
Tracks redirect analytics
URL validation before shortening
Graceful error handling (404 for invalid codes)
Thread-safe for concurrent requests

🧪 Running Tests

pytest
Includes at least 5 test cases covering:
URL shortening
Redirection
Stats tracking
Invalid code handling
Input validation

🛠️ Technologies Used
Python 3.8+
Flask
Pytest

📁 Folder Structure
bash
Copy
Edit
url-shortener/
├── app/
│   ├── main.py         # Flask entrypoint
│   ├── routes.py       # API endpoints
│   ├── utils.py        # Helper functions (e.g., code generation)
│   └── storage.py      # In-memory data store
├── tests/
│   └── test_main.py    # Unit tests
├── requirements.txt
└── README.md
