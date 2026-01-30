import json

# ------------------------
# Prompt Builder
# ------------------------
def build_prompt(grade, difficulty):

    # examples omitted here for brevity—reuse your existing ones
    examples = {
        4: [
            {
                "Frage": "Tina erzielt 8,10,6,8 Punkte. Was ist der Durchschnitt?",
                "Schwierigkeit": "Einfach",
                "Klasse": "4",
                "Aufgabentyp": "Durchschnitt",
                "Antwort": 8,
                "Einheit": "Punkte",
                "Rechenschritte": "32÷4=8."
            },
            {
                "Frage": "Bens Schulweg ist 1 km 450 m. Wie viele Meter geht er in 5 Tagen hin und zurück?",
                "Schwierigkeit": "Schwer",
                "Klasse": "4",
                "Aufgabentyp": "Umrechnung",
                "Antwort": 14500,
                "Einheit": "Meter",
                "Rechenschritte": "1450m×2×5=14500."
            },
            {
                "Frage": "Ein Schulbus fährt täglich 5×18 km. Wie viel in 5 Tagen?",
                "Schwierigkeit": "Mittel",
                "Klasse": "4",
                "Aufgabentyp": "Multiplikation",
                "Antwort": 450,
                "Einheit": "km",
                "Rechenschritte": "18×5=90, 90×5=450."
            }
        ],
        3: [
            {
                "Frage": "Ein Bäcker backt 8 Bleche Plätzchen. Auf jedem Blech sind 9 Plätzchen. Wie viele Plätzchen sind das insgesamt?",
                "Schwierigkeit": "Einfach",
                "Klasse": "3",
                "Aufgabentyp": "Einfache Multiplikation",
                "Antwort": 72,
                "Einheit": "Plätzchen",
                "Rechenschritte": "8 Bleche × 9 Plätzchen = 72."
            },
            {
                "Frage": "Im Bus sitzen 17 Kinder. 5 steigen aus, 3 steigen ein. Wie viele Kinder sind jetzt im Bus?",
                "Schwierigkeit": "Mittel",
                "Klasse": "3",
                "Aufgabentyp": "Mehrschrittaufgabe",
                "Antwort": 15,
                "Einheit": "Kinder",
                "Rechenschritte": "17−5=12, 12+3=15."
            },
            {
                "Frage": "Lisa bekommt täglich 27 €. Unter der Woche spart sie 10 €, am Wochenende 14 €. Der Monat hat 22 Wochentage und 8 Wochenendtage. Wie viel spart sie insgesamt?",
                "Schwierigkeit": "Schwer",
                "Klasse": "3",
                "Aufgabentyp": "Geld (Mehrschritt)",
                "Antwort": 332,
                "Einheit": "Euro",
                "Rechenschritte": "22×10=220, 8×14=112 → 332."
            }
        ]
    }

    examples_json = json.dumps(examples[int(grade)], indent=2, ensure_ascii=False)

    # Curriculum encoding for small models
    curriculum_rules = {
        3: """
            Zahlenraum: ≤1.000
            Fertigkeiten:
            - Kopfrechnen +/− innerhalb von 1.000
            - Einfache ×- und ÷-Aufgaben mit kleinen Zahlen (1–20)
            - 1–2 Schritt-Aufgaben
            - Einheiten: Länge (cm/m), Zeit (min/h), Geld (€), Gewicht (g/kg)
            Erlaubte Aufgabentypen:
            - Vergleich („wie viel mehr…“)
            - Zunahme/Abnahme
            - Einfache Multiplikation/Division
            - Zeit (Dauer, Start/Ende)
            - Geld (Rückgeld, Gesamtbetrag)
            Einschränkungen:
            - Keine komplexen mehrstufigen Rechenketten
            - Keine großen Datensätze
            - Keine fortgeschrittenen schriftlichen Rechenverfahren
        """,

        4: """
            Zahlenraum: ≤100.000
            Fertigkeiten:
            - Sicheres +/−/×/÷ (Kopfrechnen und schriftlich)
            - Mehrstufige Aufgaben (2–4 Schritte)
            - Einheiten: cm/m/km; g/kg; ml/l; Geld (Euro/Cent)
            - Größere Datensätze (bis ca. 8 Datenpunkte)
            Erlaubte Aufgabentypen:
            - Durchschnitt (Mittelwert)
            - Mehrschritt/Nachrechnen
            - Größere Einheitenumrechnung
            - Startwert- oder Änderungswert-Unbekannt
            - Gemischte Operationen
            Einschränkungen:
            - Text kurz halten, nicht zu geschichtenlastig
            - Unrealistische große Zahlen vermeiden
        """

    }

    curriculum_text = curriculum_rules[int(grade)]

    return f"""
        Plane intern die Aufgabe vollständig, DANN erzeuge EINE Matheaufgabe für Klasse {grade}, Schwierigkeit: {difficulty}.
        Ausgabe: NUR ein einziges gültiges JSON-Objekt (kein Text davor oder danach).

        =====================
        CURRICULUM KLASSE {grade}
        =====================
        {curriculum_text}
        Schwer-Aufgaben:
        - Maximal 1 Kontext (keine Szenenwechsel)
        - Maximal 1 unbekannte Größe
        - Keine impliziten Annahmen (z.B. „pro Tag“, „insgesamt“) ohne klare Angabe

        =====================
        SCHWIERIGKEITSANLEITUNG
        =====================
        Einfach:
        - 1-Schritt-Berechnungen (+/−/×/÷)
        - Einfache Zahlen innerhalb des Zahlenraums der Klasse
        - Alle Zahlen im Frage müssen verwendet werden

        Mittel:
        - 2–3 Schritt-Aufgaben
        - Gemischte Operationen (+/−/×/÷)
        - Kann Einheitenumrechnung oder kleine mehrstufige Berechnungen enthalten
        - Alle Zahlen in "Rechenschritte" müssen zur Berechnung der endgültigen Antwort verwendet werden

        Schwer:
        - 3–4 Schritt-Aufgaben, gemischte Operationen
        - Alle Zahlen in "Rechenschritte" müssen zur Berechnung der Antwort beitragen
        - Optional 1–2 zusätzliche Zahlen dürfen nur als Kontext im Text erscheinen
        - Aufgabe muss vollständig aus den angegebenen Zahlen lösbar bleiben


        =====================
        REGELN
        =====================
        - Aufgabe muss Curriculum Klasse {grade} erfüllen.
        - Zahlen strikt im gültigen Zahlenraum.
        - Aufgabe vollständig im Feld "Frage".
        - Antwort = ganze Zahl.
        - Keine Listen, keine Erklärungen, keine Zusatzttexte außerhalb des JSON.
        - Jede Zahl, die in "Rechenschritte" oder zur Berechnung der Antwort verwendet wird, MUSS explizit im Feld "Frage" genannt sein.
        - "Rechenschritte" muss eine vollständige, schrittweise Rechenfolge sein (nur Gleichungen, keine Worte, keine neuen Zahlen, keine Sprünge).
        - Jede Zahl in "Rechenschritte" MUSS zur Berechnung der "Antwort" beitragen. Keine Rechenschritte dürfen isoliert sein oder ungenutzt bleiben.
        - Unnötige Zusatzinformationen dürfen nur in Worten erscheinen, nicht als zusätzliche Zahlen, die nicht zur Lösung beitragen.
        - Der Kontext der Aufgabe muss jedes Mal neu und kreativ sein (kleine Sachgeschichte).
        - Antwort muss exakt zu den Rechenschritten passen.

        =====================
        INTERNER SELBSTCHECK
        =====================
        (Vom Modell ausführen; NICHT ausgeben)
        0. Erstelle intern eine Gleichung oder Rechenfolge, die direkt von den Angaben im Frage zur Antwort führt.
        1. Prüfen, ob die Schwierigkeit {difficulty} korrekt umgesetzt ist:
        - Einfach: 1-step, simple numbers
        - Mittel: 2–3 Rechenschritte, mixed operations
        - Schwer: 3–4 Rechenschritte, all numbers used, optional extra context numbers only
        2. Prüfen:
        - Ist jede benötigte Information im Frage enthalten?
        - Kann die Antwort NUR mit den angegebenen Zahlen berechnet werden?
        - Ergibt das Nachrechnen exakt die "Antwort"?
        - Wird jede im Frage genannte Zahl mindestens einmal verwendet?

        =====================
        AUSGABEFORMAT
        =====================
        {{
        "Frage": "...",
        "Schwierigkeit": "{difficulty}",
        "Klasse": "{grade}",
        "Aufgabentyp": "...",
        "Antwort": 0,
        "Einheit": "...",
        "Rechenschritte": "..."
        }}

        =====================
        BEISPIELE
        =====================
        {examples_json}
    """