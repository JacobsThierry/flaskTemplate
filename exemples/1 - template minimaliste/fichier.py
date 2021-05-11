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
    return render_template("liste.html", L=[]) #ce L fait référence au L qu'il y a dans liste.html

@app.route("/formulaire")
def formulaire():
    return render_template("formulaire.html")


@app.route("/envoi", methods=["GET", "POST"])
def envoi():
    
    if "name":
        return "aa"
        
    return redirect("/formulaire")



@app.route("/url/<val>")  # affiche l'insecte no val
def url(val):
    return val

