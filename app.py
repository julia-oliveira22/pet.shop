from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Banco de dados simples em memória
animais_cadastrados = []

precos_servicos = {
    "Banho": 50.0,
    "Tosa": 40.0,
    "Vacinação": 80.0,
    "Consulta": 100.0,
    "Desparasitação": 30.0,
    "Corte de Unhas": 20.0
}

@app.route("/")
def index():
    return render_template("index.html", animais=animais_cadastrados, precos=precos_servicos)

@app.route("/cadastrar", methods=["POST"])
def cadastrar():
    nome_pet = request.form.get("nome_pet")
    nome_dono = request.form.get("nome_dono")
    telefone = request.form.get("telefone")
    email = request.form.get("email")
    servicos = request.form.getlist("servicos")

    if not nome_pet or not nome_dono or not telefone or not email or not servicos:
        return "Erro: Todos os campos são obrigatórios."

    preco_total = sum(precos_servicos[s] for s in servicos)

    novo_pet = {
        "nome_pet": nome_pet,
        "nome_dono": nome_dono,
        "telefone": telefone,
        "email": email,
        "servicos": servicos,
        "preco": preco_total
    }

    animais_cadastrados.append(novo_pet)
    return redirect(url_for("index"))

@app.route("/buscar", methods=["POST"])
def buscar():
    dono = request.form.get("busca_dono", "").lower()
    pet = request.form.get("busca_pet", "").lower()
    servico = request.form.get("busca_servico")

    resultados = []

    for a in animais_cadastrados:
        if dono and dono not in a["nome_dono"].lower():
            continue
        if pet and pet not in a["nome_pet"].lower():
            continue
        if servico and servico != "" and servico not in a["servicos"]:
            continue
        resultados.append(a)

    return render_template("index.html", animais=resultados, precos=precos_servicos)

if __name__ == "__main__":
    app.run(debug=True)
