from flask import Flask, jsonify, render_template
import analytics

app = Flask(__name__, template_folder="../templates")

@app.route("/")
def home():
    return render_template("dashboard.html")

@app.route("/api/status")
def status():
    data = analytics.issue_stats()
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)