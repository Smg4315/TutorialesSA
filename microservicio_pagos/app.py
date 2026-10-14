from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/api/v2/comprar", methods=["GET", "POST"], strict_slashes=False)
def realizar_compra():
	"""Procesa una compra en la versión 2 del microservicio."""
	if request.method == "GET":
		return jsonify(
			{
				"mensaje": "El endpoint está disponible. Envía una solicitud POST para realizar una compra.",
				"ejemplo": {
					"producto_id": 1,
					"cantidad": 1,
				},
			}
		), 200

	datos = request.get_json(silent=True) or {}

	producto_id = datos.get("producto_id")
	cantidad = datos.get("cantidad", 1)

	if not producto_id:
		return jsonify({"error": "Falta el ID del producto."}), 400

	return jsonify(
		{
			"mensaje": "Compra procesada correctamente por el microservicio Flask (v2).",
			"producto_id": producto_id,
			"cantidad": cantidad,
			"estado": "Aprobado",
		}
	), 200


if __name__ == "__main__":
	app.run(host="0.0.0.0", port=5000)