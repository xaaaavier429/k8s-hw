# B 電腦：文字處理服務（port 5001）
import os, socket
from collections import Counter
from flask import Flask, request, jsonify

app = Flask(__name__)

def where():
    return {"pod": socket.gethostname(), "node": os.environ.get("NODE_NAME", "local")}

@app.route("/")
def index():
    return jsonify(service="B 電腦 - 文字處理", apis=["/text?s=", "/palindrome?s="], **where())

@app.route("/text")
def text():
    s = request.args.get("s", "")
    words = s.split()
    top = Counter(w.lower() for w in words).most_common(3)
    return jsonify(text=s, chars=len(s), words=len(words), upper=s.upper(),
                   reversed=s[::-1], top_words=top, **where())

@app.route("/palindrome")
def palindrome():
    s = request.args.get("s", "")
    clean = "".join(ch.lower() for ch in s if ch.isalnum())
    return jsonify(text=s, is_palindrome=bool(clean) and clean == clean[::-1], **where())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
