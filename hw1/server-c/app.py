# C 電腦：整合平台（port 5002），透過 HTTP 呼叫 A、B 兩台電腦
import os, socket
import requests
from flask import Flask, request, render_template

app = Flask(__name__)
# 在 K8S 中用 Service 名稱（DNS）找到 A、B；本機測試可用環境變數覆蓋
A_URL = os.environ.get("A_URL", "http://server-a-service:5000")
B_URL = os.environ.get("B_URL", "http://server-b-service:5001")

def call(base, path, params):
    try:
        r = requests.get(base + path, params=params, timeout=3)
        return r.json()
    except Exception as e:
        return {"error": f"無法連線到 {base}：{e}"}

@app.route("/")
def index():
    return render_template("index.html", me=socket.gethostname(),
                           node=os.environ.get("NODE_NAME", "local"),
                           a=call(A_URL, "/", {}), b=call(B_URL, "/", {}))

@app.route("/calc")
def calc():
    params = {k: request.args.get(k, "") for k in ("a", "b", "op")}
    res = call(A_URL, "/calc", params)
    return render_template("result.html", title="四則運算", server="A", res=res)

@app.route("/prime")
def prime():
    res = call(A_URL, "/prime", {"n": request.args.get("n", "")})
    return render_template("result.html", title="質數判斷", server="A", res=res)

@app.route("/text")
def text():
    res = call(B_URL, "/text", {"s": request.args.get("s", "")})
    return render_template("result.html", title="文字分析", server="B", res=res)

@app.route("/palindrome")
def palindrome():
    res = call(B_URL, "/palindrome", {"s": request.args.get("s", "")})
    return render_template("result.html", title="迴文判斷", server="B", res=res)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)
