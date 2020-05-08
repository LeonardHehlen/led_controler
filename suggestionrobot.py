from vorhome_app import app, db
from vorhome_app.models import Triggers


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