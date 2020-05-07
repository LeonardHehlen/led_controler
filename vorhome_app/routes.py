from flask import Flask, render_template, redirect, url_for, request, session
from vorhome_app import app, db
import speech_recognition as sr
import serial
import time
from vorhome_app.models import Triggers
from vorhome_app.comtools import ArduinoCommunication

port = "/dev/cu.usbmodem1411"
baudrate = 115200

var_to_template = {}


def speech():
    # obtain audio from the microphone
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        now = time.time()
        end = now + 0.1
        while True:
            if time.time() > end:
                break
            audio = r.listen(source)

    # recognize speech using Google
    try:
        record = r.recognize_google(audio)
        return record
    except:
        print("Unknown")

def check_trigger(word):

    test = Triggers.query.filter_by(name=word).first()
    if test is None:
        return False
    else:
        return test

def suggest(entry):
    wordsinlist = False

    trigger_query = Triggers.query.all()
    triggers = []
    total_count = 0
    likely_triggers = []

    for words in trigger_query:
        triggers.append(words.name)

    # for trigger in triggers:
    #     if trigger == entry:
    #         print("Bien compris, j'effectue l'action associé à :", trigger)
    #         wordsinlist = True

    if wordsinlist == False:
        for trigger in triggers:
            count = 0
            for letter in trigger:
                if letter in entry:
                    count += 1
            if count >= 2:
                likely_triggers.append(trigger)
                total_count += 1

        if total_count > 0:
            # print("Did you meant :")
            # for result in likely_triggers:
            #     # print(result)
            #     return result
            return likely_triggers

        else:
            # print("Aucun résultat ne ressemble à votre entrée, consultez la liste de triggers sur cette page.")
            return None

print(suggest("bloom"))

@app.route("/home", methods = ['POST', 'GET'])
@app.route("/", methods = ['POST', 'GET'])
def home():
    req = False
    if request.method == 'POST':
        req = True
        response = 0
        if request.form['manual_entry'] != "":
            word = request.form['manual_entry']
        else:
            word = speech()
        if word != None:
            word = word.casefold()
            var_to_template['found_word'] = word
        else: #if word is None it means it hasn't been heard.
            word = None
            response = 0
            var_to_template['suggestions'] = None
            var_to_template['found_word'] = word
            var_to_template['response'] = response
            return render_template("index.html", var_to_template=var_to_template, req=req)


        if check_trigger(word) == False: # If the word isn't in the db
            suggestions = suggest(word)
            if suggestions is not None:
                var_to_template['found_word'] = word
                var_to_template['suggestions'] = suggestions
            else:
                word = None
                var_to_template['found_word'] = word
                var_to_template['suggestions'] = suggestions
        else:
            var_to_template['suggestions'] = None
            response = 1
            ard = ArduinoCommunication(port, baudrate, 0, word)
            ard.send()
            var_to_template['response'] = response

    return render_template("index.html", var_to_template=var_to_template, req=req)

@app.route("/suggestion/<suggestion>")
def suggestion(suggestion):
    ard = ArduinoCommunication(port, baudrate, 0, suggestion)
    ard.send()
    response = 1
    var_to_template['response'] = response
    var_to_template['found_word'] = suggestion

    return redirect(url_for("home"))

@app.route("/admin", methods = ['POST', 'GET'])
def admin():
    error = []
    var_to_template['triggers'] = Triggers.query.all()
    if request.method == "POST":
        name = request.form['name']
        description = request.form['description']
        if check_trigger(name) == False:
            inpt = Triggers(name=name, description=description)
            db.session.add(inpt)
            db.session.commit()
        else:
            error.append("Ce déclencheur est déjà enregistré.")

    return render_template("admin.html", var_to_template=var_to_template)

@app.route("/manualsubmit/<submit>")
def manualsubmit(submit):
    if check_trigger(submit) == False:
        help_response = "Commande non reconnue"
    else:
        help_response = "Entrée reconnue: "
        ard = ArduinoCommunication(port, baudrate, 0, submit)
        ard.send()   
    print(help_response)
    return redirect(url_for("home"))


@app.route("/triggeredit/<int:trigger_id>", methods = ['POST', 'GET'])
def triggeredit(trigger_id):
    var_to_template['trigger'] = Triggers.query.get_or_404(trigger_id)
    if request.method == "POST":
        name = request.form['name']
        description = request.form['description']
        trigger.query.filter_by(id=trigger_id).delete()
        new_trigger = Triggers(name=name, description=description)
        db.session.add(new_trigger)
        db.session.commit()
        return redirect(url_for("admin"))
    return render_template("trigger.html", var_to_template=var_to_template)


@app.route("/triggerdel/<int:trigger_id>")
def triggerdel(trigger_id):
    print(trigger_id)
    Triggers.query.filter_by(id=trigger_id).delete()
    db.session.commit()
    return redirect(url_for("admin"))