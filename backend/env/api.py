from flask import Flask, jsonify
import analytics

app = Flask(__name__)

@app.route("/")
def home():
    return "Jira Reporting API Running"

@app.route("/api/status")
def status():
    data = analytics.issue_stats()
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)