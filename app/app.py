from flask import Flask, request, redirect, jsonify
import redis
import hashlib

app = Flask(__name__)
r = redis.Redis(host='redis', port=6379)

@app.route('/shorten', methods=['POST'])
def shorten_url():
    data = request.get_json()
    original_url = data.get('url')

    if not original_url:
        return jsonify({'error': 'URL is required'}), 400

    # Create short hash
    short_hash = hashlib.sha256(original_url.encode()).hexdigest()[:6]
    r.set(short_hash, original_url)

    short_url = request.host_url + short_hash
    return jsonify({'short_url': short_url}), 200

@app.route('/<short_hash>')
def redirect_url(short_hash):
    original_url = r.get(short_hash)

    if original_url:
        return redirect(original_url.decode('utf-8'))
    return jsonify({'error': 'URL not found'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


# how to run:
# docker run -d --name redis -p 6379:6379 redis 
# docker build -t url-shortener ./app
# docker run -d --name url-app --link redis -p 5050:5000 url-shortener

# curl -X POST http://localhost:5050/shorten \
#      -H "Content-Type: application/json" \
#      -d '{"url": "https://example.com"}'