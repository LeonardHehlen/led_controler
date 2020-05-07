# VoR_Home

Voice Recognition Home is a portefolio oriented project, which aims at showing how I would go about making a project from start to finish, from software to hardware.

It includes languages like : Python, C++ (Arduino), html/css.
A confirmed knowledge of Flask and SQLAlchemy.
CAD Design with Blender for 3D Printing, and a certain knowledge of electronics and domotic.

Triggers(object):
-----------------
    <!-- "Trigger" defines a word that's been added to the database that will "trigger" an answer from the arduino, and act according to arduino's code. -->

    Triggers is an object parented to SQLAlchemy that takes two attributes : name and description.
        __________________________________________________________________
        Name will represent the word that needs to be said so it's called.
        Description is a quick describe of the action it's supposed to do.
        __________________________________________________________________
        Description is pretty much self explanatory : it's the action that 
        the code in the arduino will do with that trigger word.

ArduinoCommunication(object):
-----------------------------
    <!-- Arduino communication is the process that allows to communication with
    the arduino, through the serial port of the arduino. -->

    ArduinoCommunication is an object that will take 4 attributes, port, baudrate, timeout and msg.
        _______________________________________________________________________
        The serial port (str) that the arduino is currently connected to.
        _______________________________________________________________________
        The baudrate (int) of the serial (must be the same value of which is defined in the arduino code, in the examples it's 115200). 
        _______________________________________________________________________
        The timeout (int) that's needed for sending and receiving messages, for this app everything is setup to be working with a timeout of value 0.
        _______________________________________________________________________
        The message (str) that needs to be sent. It needs to be a string, one message at a time.

        send():
        -------
            Send() is the method that needs to be called to actually engage in sending the message.
            It adds an "\n" and encodes the message and send it to the arduino WHILE it hasn't received an answer.
            The arduino must print something once the message is received.
            Once the program has received an answer, it send an empty string to reset the arduino and stop the action that was processinG.
            
            This is an example of arduino code that will work with this method:
                  if (Serial.readStringUntil('\n') == "triggerword") {
                            digitalWrite(greenpin, HIGH);
                            Serial.println("ok");
                        } 
            This method is designed for your message to be sent until the arduino is ready to read it, and then stops when it receives a confirmation that the action is done.


ROUTES :
--------
    