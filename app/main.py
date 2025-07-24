from flask import Flask, request, jsonify, redirect, render_template, url_for
from datetime import datetime
import threading

from models import URLStore
from utils import generate_short_code, is_valid_url

app = Flask(__name__)

url_store = URLStore()
lock = threading.Lock()



@app.route('/')
def health_check():
    return jsonify({
        "status": "healthy",
        "service": "URL Shortener API"
    })

@app.route('/api/health')
def api_health():
    return jsonify({
        "status": "ok",
        "message": "URL Shortener API is running"
    })

@app.route('/health')
def health():
    return jsonify({"status": "healthy"}), 200



@app.route('/api/shorten', methods=['POST'])
def shorten_url():
    """
    API: Shorten a URL
    POST /api/shorten
    """
    try:
        data = request.get_json()
        if not data or 'url' not in data:
            return jsonify({"error": "URL is required"}), 400

        original_url = data['url']
        if not is_valid_url(original_url):
            return jsonify({"error": "Invalid URL format"}), 400

        with lock:
            short_code = generate_short_code()
            while url_store.exists(short_code):
                short_code = generate_short_code()
            url_store.store_url(short_code, original_url)

        short_url = f"{request.host_url.rstrip('/')}/{short_code}"

        return jsonify({
            "short_code": short_code,
            "short_url": short_url
        }), 201

    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500

@app.route('/api/stats/<short_code>')
def get_stats(short_code):
    """
    API: Get analytics stats
    GET /api/stats/<short_code>
    """
    try:
        with lock:
            url_data = url_store.get_url(short_code)

        if not url_data:
            return jsonify({"error": "Short code not found"}), 404

        return jsonify({
            "url": url_data['original_url'],
            "clicks": url_data['clicks'],
            "created_at": url_data['created_at'].isoformat()
        }), 200

    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500



@app.route('/<short_code>')
def redirect_url(short_code):
    """
    Redirect to original URL
    GET /<short_code>
    """
    try:
        with lock:
            url_data = url_store.get_url(short_code)

        if not url_data:
            return render_template("404.html", error="Short URL not found"), 404

        # Increment click count
        with lock:
            url_store.increment_clicks(short_code)

        return redirect(url_data['original_url'], code=302)

    except Exception as e:
        return render_template("error.html", error="Internal server error"), 500



@app.route("/shorten", methods=["GET", "POST"])
def shorten_form():
    if request.method == "POST":
        url = request.form.get("url")
        if not is_valid_url(url):
            return render_template("index.html", error="Invalid URL format")

        with lock:
            short_code = generate_short_code()
            while url_store.exists(short_code):
                short_code = generate_short_code()
            url_store.store_url(short_code, url)

        return redirect(url_for("show_shortened", code=short_code))

    return render_template("index.html")


@app.route("/shortened/<code>")
def show_shortened(code):
    short_url = f"{request.host_url.rstrip('/')}/{code}"
    return render_template("shortened.html", short_url=short_url, code=code)


@app.route("/stats-page/<code>")
def show_stats(code):
    with lock:
        url_data = url_store.get_url(code)

    if not url_data:
        return render_template("stats.html", error="Short code not found")

    return render_template("stats.html", code=code, data=url_data)



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
