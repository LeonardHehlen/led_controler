from flask import Flask, render_template, redirect, url_for, request, session
from vorhome_app import app, db
import speech_recognition as sr
import serial
import time
from vorhome_app.models import Triggers
from vorhome_app.comtools import ArduinoCommunication

port = "/dev/cu.usbmodem1411"
baudrate = 115200

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

def check_trigger(trigger):

    test = Triggers.query.filter_by(name=trigger).first()
    if test is None:
        return False
    else:
        return test

@app.route("/", methods = ['POST', 'GET'])
def home():
    req = False
    # vor = ""
    # response = ""
    url_stuff = [] # 0 = Words, 1 = Responses
    if request.method == 'POST':
        req = True
        vor = speech()
        if vor != None:
            vor = vor.casefold()
            url_stuff.insert(1, vor)
        else:
            vor = "Unknown"
            url_stuff.insert(1, vor)

        if check_trigger(vor) == False:
            response = "Commande non reconnue"
            url_stuff.insert(0, response)
        else:
            response = "Entrée reconnue: "
            ard = ArduinoCommunication(port, baudrate, 0, vor)
            ard.send()
            url_stuff.insert(0, response)
    return render_template("index.html", url_stuff=url_stuff, req=req)


@app.route("/admin", methods = ['POST', 'GET'])
def admin():
    error = []
    triggers = Triggers.query.all()
    if request.method == "POST":
        name = request.form['name']
        description = request.form['description']
        if check_trigger(name) == False:
            inpt = Triggers(name=name, description=description)
            db.session.add(inpt)
            db.session.commit()
        else:
            error.append("Ce déclencheur est déjà enregistré.")

    return render_template("admin.html", triggers=triggers)

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
    trigger = Triggers.query.get_or_404(trigger_id)
    if request.method == "POST":
        name = request.form['name']
        description = request.form['description']
        trigger.query.filter_by(id=trigger_id).delete()
        new_trigger = Triggers(name=name, description=description)
        db.session.add(new_trigger)
        db.session.commit()
        return redirect(url_for("admin"))
    return render_template("trigger.html", trigger=trigger)


@app.route("/triggerdel/<int:trigger_id>")
def triggerdel(trigger_id):
    print(trigger_id)
    Triggers.query.filter_by(id=trigger_id).delete()
    db.session.commit()
    return redirect(url_for("admin"))