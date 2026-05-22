from flask import Flask, request, jsonify

app = Flask(__name__)

reports = []

@app.route("/")
def home():
    return "API Nodo Civico funcionando"

@app.route("/reports", methods=["GET"])
def get_reports():
    return jsonify(reports)

@app.route("/reports", methods=["POST"])
def create_report():
    data = request.json
    reports.append(data)
    return jsonify({
        "message": "Reporte creado",
        "data": data
    }), 201

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
