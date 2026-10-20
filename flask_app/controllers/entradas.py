from flask import render_template, request, redirect, url_for, session, flash
from flask_app import app
from flask_app.models.entrada import Entrada

@app.route("/diario")
def dashboard():
    if "usuario_id" not in session:
        return redirect(url_for("inicio"))

    # Trae solo las entradas del usuario en sesion
    entradas = Entrada.obtener_por_usuario(session["usuario_id"])
    return render_template("panel.html", entradas=entradas)

@app.route("/diario/nueva")
def nueva_entrada():
    if "usuario_id" not in session:
        return redirect(url_for("inicio"))

    return render_template("nueva.html", datos_previos={})

@app.route("/diario/crear", methods=["POST"])
def crear_entrada():
    if "usuario_id" not in session:
        return redirect(url_for("inicio"))

    if not Entrada.validar_entrada(request.form):
        return render_template("nueva.html", datos_previos=request.form)

    datos = {
        "titulo": request.form["titulo"].strip(),
        "fecha": request.form["fecha"],
        "notas": request.form["notas"].strip(),
        "usuario_id": session["usuario_id"]
    }

    res = Entrada.guardar(datos)
    if not res:
        flash("Ocurrió un error al guardar la entrada.", "entrada")
        return render_template("nueva.html", datos_previos=request.form)

    return redirect(url_for("dashboard"))

@app.route("/diario/<int:id>")
def ver_entrada(id):
    if "usuario_id" not in session:
        return redirect(url_for("inicio"))

    entrada = Entrada.obtener_por_id(id)

    # Impedir que vea entradas de otros usuarios mediante URL
    if not entrada or entrada.usuario_id != session["usuario_id"]:
        flash("Acceso denegado a esa entrada.", "diario")
        return redirect(url_for("dashboard"))

    return render_template("ver.html", entrada=entrada)

@app.route("/diario/editar/<int:id>")
def editar_entrada(id):
    if "usuario_id" not in session:
        return redirect(url_for("inicio"))

    entrada = Entrada.obtener_por_id(id)

    # Impedir que edite entradas ajenas mediante URL
    if not entrada or entrada.usuario_id != session["usuario_id"]:
        flash("Acceso denegado.", "diario")
        return redirect(url_for("dashboard"))

    return render_template("editar.html", entrada=entrada, datos_previos={})

@app.route("/diario/actualizar/<int:id>", methods=["POST"])
def actualizar_entrada(id):
    if "usuario_id" not in session:
        return redirect(url_for("inicio"))

    entrada = Entrada.obtener_por_id(id)
    if not entrada or entrada.usuario_id != session["usuario_id"]:
        return redirect(url_for("dashboard"))

    if not Entrada.validar_entrada(request.form):
        return render_template("editar.html", entrada=entrada, datos_previos=request.form)

    datos = {
        "id": id,
        "titulo": request.form["titulo"].strip(),
        "fecha": request.form["fecha"],
        "notas": request.form["notas"].strip(),
        "usuario_id": session["usuario_id"]
    }

    Entrada.actualizar(datos)
    return redirect(url_for("dashboard"))

@app.route("/diario/borrar/<int:id>", methods=["POST"])
def borrar_entrada(id):
    # Requisito obligatorio: Eliminacion por metodo POST
    if "usuario_id" not in session:
        return redirect(url_for("inicio"))

    entrada = Entrada.obtener_por_id(id)
    if entrada and entrada.usuario_id == session["usuario_id"]:
        Entrada.eliminar(id, session["usuario_id"])

    return redirect(url_for("dashboard"))

@app.route("/diario/buscar")
def buscar_entrada():
    if "usuario_id" not in session:
        return redirect(url_for("inicio"))

    # Requisito BONUS: Buscar por la URL recibiendo el parametro q
    termino = request.args.get("q", "").strip()
    resultados = []

    if termino:
        resultados = Entrada.buscar_por_notas(session["usuario_id"], termino)

    return render_template("buscar.html", resultados=resultados, termino=termino)