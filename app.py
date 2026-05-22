from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Base de datos temporal en memoria
reports = []

# Ruta principal
@app.route("/")
def home():
    return jsonify({
        "message": "API Nodo Civico funcionando"
    })


# Obtener todos los reportes
@app.route("/reports", methods=["GET"])
def get_reports():
    return jsonify(reports)


# Obtener un reporte por ID
@app.route("/reports/<int:report_id>", methods=["GET"])
def get_report(report_id):

    report = next(
        (r for r in reports if r["id"] == report_id),
        None
    )

    if report is None:
        return jsonify({
            "error": "Reporte no encontrado"
        }), 404

    return jsonify(report)


# Crear reporte
@app.route("/reports", methods=["POST"])
def create_report():

    data = request.json

    if not data:
        return jsonify({
            "error": "No se recibieron datos"
        }), 400

    required_fields = [
        "title",
        "description",
        "category",
        "priority",
        "status",
        "location",
        "date"
    ]

    for field in required_fields:
        if field not in data:
            return jsonify({
                "error": f"Falta el campo: {field}"
            }), 400

    new_report = {
        "id": len(reports) + 1,
        "title": data["title"],
        "description": data["description"],
        "category": data["category"],
        "priority": data["priority"],
        "status": data["status"],
        "location": data["location"],
        "date": data["date"]
    }

    reports.append(new_report)

    return jsonify({
        "message": "Reporte creado correctamente",
        "data": new_report
    }), 201


# Actualizar reporte
@app.route("/reports/<int:report_id>", methods=["PUT"])
def update_report(report_id):

    report = next(
        (r for r in reports if r["id"] == report_id),
        None
    )

    if report is None:
        return jsonify({
            "error": "Reporte no encontrado"
        }), 404

    data = request.json

    report["title"] = data.get("title", report["title"])
    report["description"] = data.get("description", report["description"])
    report["category"] = data.get("category", report["category"])
    report["priority"] = data.get("priority", report["priority"])
    report["status"] = data.get("status", report["status"])
    report["location"] = data.get("location", report["location"])
    report["date"] = data.get("date", report["date"])

    return jsonify({
        "message": "Reporte actualizado",
        "data": report
    })


# Eliminar reporte
@app.route("/reports/<int:report_id>", methods=["DELETE"])
def delete_report(report_id):

    global reports

    report = next(
        (r for r in reports if r["id"] == report_id),
        None
    )

    if report is None:
        return jsonify({
            "error": "Reporte no encontrado"
        }), 404

    reports = [
        r for r in reports
        if r["id"] != report_id
    ]

    return jsonify({
        "message": "Reporte eliminado"
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
