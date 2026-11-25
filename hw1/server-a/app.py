# A 電腦：數學運算服務（port 5000）
import math, os, socket
from flask import Flask, request, jsonify

app = Flask(__name__)

def where():
    return {"pod": socket.gethostname(), "node": os.environ.get("NODE_NAME", "local")}

OPS = {
    "add": lambda a, b: a + b,
    "sub": lambda a, b: a - b,
    "mul": lambda a, b: a * b,
    "div": lambda a, b: a / b,
    "pow": lambda a, b: a ** b,
}

@app.route("/")
def index():
    return jsonify(service="A 電腦 - 數學運算", apis=["/calc?a=&b=&op=add|sub|mul|div|pow", "/prime?n=", "/gcd?a=&b="], **where())

@app.route("/calc")
def calc():
    try:
        a, b = float(request.args["a"]), float(request.args["b"])
        op = request.args.get("op", "add")
        result = OPS[op](a, b)
        return jsonify(a=a, b=b, op=op, result=result, **where())
    except ZeroDivisionError:
        return jsonify(error="除數不可為 0", **where()), 400
    except (KeyError, ValueError):
        return jsonify(error="參數錯誤：需要數字 a、b 與 op", **where()), 400

@app.route("/prime")
def prime():
    try:
        n = int(request.args["n"])
    except (KeyError, ValueError):
        return jsonify(error="參數錯誤：需要整數 n", **where()), 400
    is_p = n > 1 and all(n % i for i in range(2, math.isqrt(n) + 1))
    return jsonify(n=n, is_prime=is_p, **where())

@app.route("/gcd")
def gcd():
    try:
        a, b = int(request.args["a"]), int(request.args["b"])
    except (KeyError, ValueError):
        return jsonify(error="參數錯誤：需要整數 a、b", **where()), 400
    g = math.gcd(a, b)
    return jsonify(a=a, b=b, gcd=g, lcm=(a * b // g if g else 0), **where())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
