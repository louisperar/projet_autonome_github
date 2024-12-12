from datetime import datetime
from flask import Flask, jsonify, render_template, request
import sqlite3
app = Flask(__name__)


def cursor():
    conn = sqlite3.connect("./code/back/VM.db")
    cur = conn.cursor()
    return cur, conn


@app.route("/", methods=["GET"])
def verif():
    return render_template('verif.html.j2')


@app.route("/accueil", methods=["GET"])
def accueil():
    return render_template('accueil.html.j2')


@app.route("/VMs", methods=["GET", "POST"])
def VMs():
    cur, conn = cursor()
    if request.method == "GET" :
        liste_VMs = cur.execute("SELECT * FROM VM").fetchall()
        return render_template("VMs.html.j2", liste=liste_VMs)
    elif request.method == "POST" :
        nom = request.form.get("nom")
        etat = request.form.get("etat")
        ip = request.form.get("ip")
        ram = request.form.get("ram")
        stockage = request.form.get("stockage")
        creer = datetime.today().strftime("%d/%m/%Y")
        modifier = creer
        cur.execute("INSERT INTO VM (nom, etat, ip_addr, RAM, stockage, creer_le, modifier_le) VALUES (?, ?, ?, ?, ?, ?, ?)",  (nom, etat, ip, ram, stockage, creer, modifier))
        conn.commit()
        liste_VMs = cur.execute("SELECT * FROM VM").fetchall()
        return render_template("VMs.html.j2", liste=liste_VMs)
    else:
        return "ERREUR"


@app.route("/VMs/<id>", methods=["GET","POST"])
def VM(id):
    cur, conn = cursor()
    if request.method == "GET" :
        liste_VMs = cur.execute("SELECT * FROM VM WHERE id = ?", (id,)).fetchall()
        return render_template("VM.html.j2", liste=liste_VMs)
    elif request.method == "POST" :
        id = request.form.get("id")
        nom = request.form.get("nom")
        etat = request.form.get("etat")
        ip_addr = request.form.get("ip")
        ram = request.form.get("ram")
        stockage = request.form.get("stockage")
        modifier = datetime.today().strftime("%d/%m/%Y")
        if id != 0 and nom == "" and etat == "" and ip_addr == "" and ram == "" and stockage == "":
            liste_VMs = cur.execute("SELECT * FROM VM WHERE id = ?", (id,)).fetchall()
            return render_template("VM.html.j2", liste=liste_VMs)
        elif id != 0 and nom != "" or etat != "" or ip_addr != "" or ram != "" or stockage != "":
            if nom:
                cur.execute("UPDATE VM SET nom = ? WHERE id = ?", (nom, id))
            if etat:
                cur.execute("UPDATE VM SET etat = ? WHERE id = ?", (etat, id))
            if ip_addr:
                cur.execute("UPDATE VM SET ip = ? WHERE id = ?", (ip_addr, id))
            if ram:
                cur.execute("UPDATE VM SET ram = ? WHERE id = ?", (ram, id))
            if stockage:
                cur.execute("UPDATE VM SET stockage = ? WHERE id = ?", (stockage, id))
            cur.execute("UPDATE VM SET modifier_le = ? WHERE id = ?", (modifier, id))
            conn.commit()
            liste_VMs = cur.execute("SELECT * FROM VM WHERE id = ?", (id,)).fetchall()
            return render_template("VM.html.j2", liste=liste_VMs)
    else:
        return "ERREUR"+str(id)
    

@app.route("/VMs/delete/<id>", methods=["POST"])
def suppression(id):
    cur, conn = cursor()
    id = request.form.get("id")
    vm_existante = cur.execute("SELECT * FROM VM WHERE id = ?", (id,)).fetchall()
    if not vm_existante:
        liste_VMs = cur.execute("SELECT * FROM VM WHERE id = ?", (id,)).fetchall()
        return render_template("VM.html.j2", liste=liste_VMs)
    cur.execute("DELETE FROM VM WHERE id = ?", (id,))
    conn.commit()
    liste_VMs = cur.execute("SELECT * FROM VM WHERE id = ?", (id,)).fetchall()
    return render_template("VM.html.j2", liste=liste_VMs)


if __name__ == '__main__':
    app.run(port = 8080, debug=True)