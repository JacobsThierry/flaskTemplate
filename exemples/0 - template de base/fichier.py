from flask import Flask, Blueprint, render_template, abort, request, redirect
from flask import g
import sqlite3

app = Flask(__name__) #On crée l'application

DATABASE = "a.db"  # on définie le nom de notre base de données


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db



@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/') #On note le chemin vers notre page : c'est ce qu'on met dans l'url après l'adresse du site. Doit toujours commencé par un /
def home():
    return render_template("home.html") #home.html doit être dans le dossier templates


@app.route("/liste")
def liste():
    return render_template("liste.html", L=["papillon", "insecte", "ours"]) #ce L fait référence au L qu'il y a dans liste.html

@app.route("/formulaire")
def formulaire():
    return render_template("formulaire.html")


@app.route("/envoi", methods=["GET", "POST"])
def envoi():
    
    if "du_texte" in request.form and "une_couleur" in request.form and "un_numero" in request.form:
        texte = request.form["du_texte"]
        couleur = request.form["une_couleur"]
        numero = int(request.form["un_numero"])
        return render_template("envoi.html", N=numero, c = couleur, t = texte)
    
    return redirect("/formulaire")


def un_exemple_de_requete_bdd():
    db = get_db()
    c = db.cursor()

    c.execute("drop table if exists INSECTE")
    c.executescript("""CREATE TABLE INSECTE(
        id_insecte INTEGER PRIMARY KEY,
        nom_insecte TEXT
    );""" )

    nom_ins = [ ("perce oreille",), ("coccinelle",)] #les () et la , c'est car sqlite demande des tableau en paramètres. Si on let met pas, il pense que le tableau est la chaien qu'on lui donne

    c.executemany("INSERT INTO INSECTE (nom_insecte) VALUES (?)", nom_ins)

    db.commit()


@app.route("/url/<val>")  # affiche l'insecte no val
def url(val):
    un_exemple_de_requete_bdd()

    db = get_db()

    if (val.isdigit()):
        return db.cursor().execute("SELECT nom_insecte FROM INSECTE WHERE id_insecte = ?", (val,)).fetchall()[0][0]
    else:
        return "Oups, tu n'as pas donné un numéro d'insecte"
    

