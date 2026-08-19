import tkinter as tk            # lädt das Tkinter-Modul für grafische Oberfläche. Kurzform tk.
import cv2                      # lädt opencv-python. Für Öffnen und Auslesen der Videos
from PIL import Image, ImageTk  # lädt zwei Werkzeuge aus Pillow. Für sauberes Abspielen der Videos.
import time                     # Zeitmessung der Videowiedergabe. Für eine flüssige, realistische Abspielgeschwindigkeit
import pygame                   # Wird für die Audio-Wiedergabe der Instruktionen gebraucht.

# Erzeugt das Hauptfenster der Anwendung
fenster = tk.Tk()
fenster.title("Apraxie-Screening")  # Titel in der Fensterleiste
fenster.geometry("1100x800")        # Startgröße des Fensters
pygame.mixer.init()                 # startet das Audio-System von pygame

# Audio für Instruktionsseiten

pygame.mixer.music.load("assets/audio/instruktionen.mp3")

audio_stop_id = None

def spiele_audio(seiten_key):
    """Spielt den Audio-Abschnitt für die angegebene Instruktionsseite ab"""
    global audio_stop_id

    if audio_stop_id is not None:
        fenster.after_cancel(audio_stop_id)
        audio_stop_id = None
    pygame.mixer.music.stop()

    start, ende = audio_zeitstempel[seiten_key]
    dauer_ms = int((ende - start) * 1000)

    pygame.mixer.music.play(start=start)
    audio_stop_id = fenster.after(dauer_ms, pygame.mixer.music.stop)

def stoppe_audio():
    """Bricht eine laufende Audio-Wiedergabe ab, z.B. beim Verlassen einer Instruktionsseite."""
    global audio_stop_id
    if audio_stop_id is not None:
        fenster.after_cancel(audio_stop_id)
        audio_stop_id = None
    pygame.mixer.music.stop()

# Anleitung für die Testleitung am Anfang

label_ueberschrift = tk.Label(fenster, text="Instruktion für die Testleitung", font=("Calibri", 18, "bold"), padx=20, pady=10)
label_ueberschrift.pack()
label_ueberschrift.pack_forget()

anleitungstext = """
Positionieren Sie den Laptop so, dass sowohl Testleitung als auch der*die Patient*in den Bildschirm
gut wahrnehmen können.

Das Screening wird im Sitzen durchgeführt. Platzieren Sie den Stuhl des*der Patient*in gegenüber
dem Stuhl der Testleitung mit ausreichend Abstand. Achten Sie darauf, dass genügend Freiraum zum
Tisch besteht, sodass die Bein- und Fußbewegungen gut sichtbar und nicht eingeschränkt sind.

Der*Die Patient*in zieht die Schuhe aus; Socken können getragen werden. Die Ausgangsposition
ist eine hüftbreite Stellung der Beine. Der*Die Patient*in sitzt möglichst weit vorne auf
dem Stuhl, mit den Füßen flach auf dem Boden. Die Arme liegen locker auf dem Schoß oder, wenn
vorhanden, auf den Armlehnen. Alle Bewegungen werden spiegelbildlich demonstriert.

Zum Starten auf 'Start' klicken."""

label_anleitung = tk.Label(fenster, text=anleitungstext, justify="left", padx=20, pady=20, font=("Calibri", 14))
label_anleitung.pack()
label_anleitung.pack_forget()

def zurueck_zu_formular_von_anleitung_klick():
    """Blendet die Anleitung aus und zeigt wieder das Formular, mit dem man den dominanten Fuß auswählt."""
    stoppe_audio()
    label_ueberschrift.pack_forget()
    label_anleitung.pack_forget()
    button_zurueck_zu_formular_anleitung.pack_forget()
    button_start.pack_forget()

    label_fuss.pack()
    radio_links.pack()
    radio_rechts.pack()
    button_weiter.pack()

def start_klick():
    """Blendet die Anleitung für die Testleitung aus und blendet die erste Instruktion für die teilnehmende Person ein."""
    stoppe_audio()
    label_ueberschrift.pack_forget()
    label_anleitung.pack_forget()
    button_zurueck_zu_formular_anleitung.pack_forget()
    button_start.pack_forget()

    zeige_testblock(0)

button_zurueck_zu_formular_anleitung = tk.Button(fenster, text="Zurück", command=zurueck_zu_formular_von_anleitung_klick)
button_zurueck_zu_formular_anleitung.pack()
button_zurueck_zu_formular_anleitung.pack_forget()

button_start = tk.Button(fenster, text="Start", command=start_klick)
button_start.pack()
button_start.pack_forget()

# Merkt sich, welcher Fuß aktuell ausgewählt ist (Standard: Links)
fuss_variable = tk.StringVar(value="links")

# Beschriftung und Auswahlmöglichkeiten für den dominanten Fuß
label_fuss = tk.Label(fenster, text="Dominanter Fuß: ")
label_fuss.pack()

radio_links = tk.Radiobutton(fenster, text="links", variable=fuss_variable, value="links")
radio_links.pack()

radio_rechts = tk.Radiobutton(fenster, text="rechts", variable=fuss_variable, value="rechts")
radio_rechts.pack()

# Liste aller Objektfotos in der Reihenfolge, in der sie gezeigt werden. Nummerierung der Dateien stimmt nicht mit gezeigter Reihenfolge überein.
objekt_fotos = [
    "assets/objekte/01_Igelball.png",
    "assets/objekte/02_Fussball.png",
    "assets/objekte/03_Tretroller.png",
    "assets/objekte/04_Fussluftpumpe.png",
    "assets/objekte/05_Tretmuelleimer.png",
    "assets/objekte/06_Igelrolle.png",
    "assets/objekte/07_Spaten.png",
    "assets/objekte/08_Tuermatte.png",
    "assets/objekte/09_Hausschuhe.png",
    "assets/objekte/10_Fahrrad.png",
    "assets/objekte/11_Springseil.png",
    "assets/objekte/12_Schlittschuhe.png",
]

# Zähler, der sich merkt, beim wievielten Foto wir gerade sind (Start: 0 = erstes Foto)
aktueller_index = 0

# Leeres Label, das das jeweils aktuelle Foto anzeigt
label_bild = tk.Label(fenster)
label_bild.pack()

def zeige_foto():
    """Lädt das Foto an der aktuellen Zähler-Position und zeigt es im Label an."""
    global bild_referenz
    pfad = objekt_fotos[aktueller_index]
    bild_referenz = tk.PhotoImage(file=pfad)        # Bild laden
    bild_referenz = bild_referenz.subsample(2, 2)   # verkleinert auf 1/2 der Originalgröße
    label_bild.config(image=bild_referenz)          # Bild ins Label einsetzen

def naechstes_foto():
    """Button-Funktion. Zeigt das nächste Foto, oder springt zur nächsten Testblock."""
    global aktueller_index
    aktueller_index = aktueller_index + 1
    testblock = testbloecke[aktueller_testblock]
    if aktueller_index <= testblock["ende"]:
        zeige_foto()
    else:
        label_bild.config(image="")
        button_voriges_foto.pack_forget()
        button_naechstes_foto.pack_forget()
        zeige_testblock(aktueller_testblock + 1)

def voriges_foto():
    """Button-Funktion. Zeigt das vorherige Foto, oder springt zurück zur Instruktionsseite für Pantomime des Objektgebrauchs."""
    global aktueller_index
    testblock = testbloecke[aktueller_testblock]
    if aktueller_index > testblock["start"]:
        aktueller_index = aktueller_index - 1
        zeige_foto()
    else:
        label_bild.config(image="")
        button_voriges_foto.pack_forget()
        button_naechstes_foto.pack_forget()
        zeige_testblock(aktueller_testblock)

# Weiter-Button für die Foto-Phase
button_naechstes_foto = tk.Button(fenster, text="Weiter", command=naechstes_foto)
button_naechstes_foto.pack()        # einmal "registrieren", damit Tkinter die Platzierung kennt
button_naechstes_foto.pack_forget() # sofort wieder verstecken, bis die Fotos-Phase beginnt

# Zurück-Button für die Foto-Phase
button_voriges_foto = tk.Button(fenster, text="Zurück", command=voriges_foto)
button_voriges_foto.pack()          # einmal registrieren, damit Tkinter die Platzierung kennt
button_voriges_foto.pack_forget()   # sofort wieder verstecken, bis die Fotos-Phase beginnt

# Funktion, die beim Klick auf "Weiter" beim Fuß-Formular ausgeführt wird
def weiter_klick():
    """Liest den dominanten Fuß aus und zeigt die Anleitung für die Testleitung."""
    print("Dominanter Fuß:", fuss_variable.get())

    # Fuß-Auswahl ausblenden
    label_fuss.pack_forget()
    radio_links.pack_forget()
    radio_rechts.pack_forget()
    button_weiter.pack_forget()
    spiele_audio("Anleitung Testleitung")

    # Anleitungsseite einblenden
    label_ueberschrift.pack()
    label_anleitung.pack()
    button_zurueck_zu_formular_anleitung.pack()
    button_start.pack()
    spiele_audio("Anleitung Testleitung")

# Button, der die obige Funktion beim Klick aufruft
button_weiter = tk.Button(fenster, text="Weiter", command=weiter_klick)
button_weiter.pack()

# Bewegungsvideos

video_ids = [
    "13_ferse_innenrand",
    "14_oberseite",
    "15_abrollen",
    "16_wiederholtes_aufsetzen",
    "17_kreuz",
    "18_linie",
    "19_fuesse_ausstrecken",
    "20_aussenkanten",
    "21_fuesse_scharren",
    "22_boden_tippen",
    "23_zigarette",
    "24_seitlich_wegschieben",
    "25_wippen",
    "26_vorne_wegschieben",
    "27_aufheben",
    "28_hindernis",
    "29_ueberschlagen",
    "30_schuh_ausziehen",
    "31_salutieren",
    "32_ballerina",
]

def video_pfad(video_id):
    """Baut den passenden Dateipfad je nach dominantem Fuß zusammen."""
    if fuss_variable.get() == "links":
        return "assets/videos/links/real_" + video_id + ".mp4"
    else:
        return "assets/videos/rechts/spiegel_" + video_id + ".mp4"

# Zähler, der sich merkt, beim wievielten Video wir gerade sind
aktueller_video_index = 0

# Leeres Label, das das Video zeigt
label_video = tk.Label(fenster)
label_video.pack()
label_video.pack_forget()

video_capture = None
frame_callback_id = None

def zeige_video():
    """Öffnet das aktuelle Video und startet die Wiedergabe."""
    global video_capture, frame_callback_id
    
    # Falls noch ein alter Frame-Aufruf aussteht: abbrechen
    if frame_callback_id is not None:
        fenster.after_cancel(frame_callback_id)
        frame_callback_id = None
    
    # Falls noch ein altes Video offen ist: sauber schließen
    if video_capture is not None:
        video_capture.release()
    
    video_id = video_ids[aktueller_video_index]
    pfad = video_pfad(video_id)
    video_capture = cv2.VideoCapture(pfad)

    # sorgt dafür, dass Video in tatsächlicher Framerate ausgelesen wird.
    global video_delay
    fps = video_capture.get(cv2.CAP_PROP_FPS)
    video_delay = int(1000 / fps)

    naechster_frame()

def naechster_frame():
    """Liest den nächsten Frame aus dem Video und zeigt ihn an; wiederholt sich automatisch."""
    global video_capture, frame_callback_id
    start = time.time()

    erfolgreich, frame = video_capture.read()

    if erfolgreich:
        frame = cv2.resize(frame, (800, 450))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        bild = Image.fromarray(frame)
        bild_tk = ImageTk.PhotoImage(image=bild)
        label_video.image = bild_tk
        label_video.config(image=bild_tk)

        dauer = (time.time() - start) * 1000
        verbleibende_wartezeit = max(1, video_delay - int(dauer))   # zieht die tatsächlich schon verbrauchte Verarbeitungszeit von der Ziel-Wartezeit ab
        frame_callback_id = fenster.after(verbleibende_wartezeit, naechster_frame)

def video_replay():
    """Setzt das aktuelle Video auf den Anfang zurück und spielt es erneut ab."""
    global video_capture, frame_callback_id
    if frame_callback_id is not None:
        fenster.after_cancel(frame_callback_id)
        frame_callback_id = None

    video_capture.set(cv2.CAP_PROP_POS_FRAMES, 0)
    naechster_frame()

button_video_replay = tk.Button(fenster, text="Nochmal ansehen", command=video_replay)
button_video_replay.pack()
button_video_replay.pack_forget()

def naechstes_video():
    """Zeigt das nächste Video der aktuellen Testblock, springt zur nächsten Testblock, oder zeigt den Abschluss."""
    global aktueller_video_index, frame_callback_id, video_capture
    aktueller_video_index = aktueller_video_index + 1
    testblock = testbloecke[aktueller_testblock]
    if aktueller_video_index <= testblock["ende"]:
        zeige_video()
    else:
        if frame_callback_id is not None:
            fenster.after_cancel(frame_callback_id)
            frame_callback_id = None
        if video_capture is not None:
            video_capture.release()
            video_capture = None

        label_video.config(image="")
        button_voriges_video.pack_forget()
        button_video_replay.pack_forget()
        button_naechstes_video.pack_forget()

        if aktueller_testblock + 1 < len(testbloecke):
            zeige_testblock(aktueller_testblock + 1)
        else:
            label_ueberschrift_abschluss.pack()
            label_abschluss.pack()
            button_neustart.pack()


def voriges_video():
    """Zeigt das vorherige Video, oder springt zurück zur Instruktionsseite dieser Testblock."""
    global aktueller_video_index, frame_callback_id, video_capture
    testblock = testbloecke[aktueller_testblock]
    if aktueller_video_index > testblock["start"]:
        aktueller_video_index = aktueller_video_index - 1
        zeige_video()
    else:
        if frame_callback_id is not None:
            fenster.after_cancel(frame_callback_id)
            frame_callback_id = None
        if video_capture is not None:
            video_capture.release()
            video_capture = None

        label_video.config(image="")
        button_voriges_video.pack_forget()
        button_video_replay.pack_forget()
        button_naechstes_video.pack_forget()
        zeige_testblock(aktueller_testblock)
    
button_voriges_video = tk.Button(fenster, text="Zurück", command=voriges_video)
button_voriges_video.pack()
button_voriges_video.pack_forget()

button_naechstes_video = tk.Button(fenster, text="Weiter", command=naechstes_video)
button_naechstes_video.pack()
button_naechstes_video.pack_forget()
# Startet die Warteschleife - hält das Fenster offen und reagiert auf Eingaben

# Abschlussbildschirm

label_ueberschrift_abschluss = tk.Label(fenster, text="Screening beendet.", font=("Calibri", 18, "bold"), padx=20, pady=10)
label_ueberschrift_abschluss.pack()
label_ueberschrift_abschluss.pack_forget()

abschlusstext = """Das Apraxie-Screening der unteren Extremitäten ist abgeschlossen.

Alle Objektfotos und Bewegungsvideos wurden gezeigt."""

label_abschluss = tk.Label(fenster, text=abschlusstext, justify="left", padx=20, pady=20, font=("Calibri", 12))
label_abschluss.pack()
label_abschluss.pack_forget()

def neustart_klick():
    """Setzt das Screening zurück auf den Anfang für den nächsten Patienten."""
    global aktueller_index, aktueller_video_index, frame_callback_id, video_capture, aktueller_testblock

    # Laufende Wiedergabe sauber stoppen (falls noch etwas läuft)
    if frame_callback_id is not None:
        fenster.after_cancel(frame_callback_id)
        frame_callback_id = None
    if video_capture is not None:
        video_capture.release()
        video_capture = None

    aktueller_index = 0
    aktueller_video_index = 0
    aktueller_testblock = 0

    label_ueberschrift_abschluss.pack_forget()
    label_abschluss.pack_forget()
    button_neustart.pack_forget()

    label_fuss.pack()
    radio_links.pack()
    radio_rechts.pack()
    button_weiter.pack()

button_neustart = tk.Button(fenster, text="Neue*r Patient*in", command=neustart_klick)
button_neustart.pack()
button_neustart.pack_forget()

testbloecke = [
    {"typ": "foto", "start": 0, "ende": 6, "titel": "Pantomime des Objektgebrauchs - Unilaterale Bewegungen",
     "text": "Bitte zeigen Sie mit Ihrem dominanten Bein und dominanten Fuß, wie man diesen Gegenstand benutzt. Falls die korrekte Ausführung der Bewegung auch die Ausrichtung des Fußes erfordert, machen Sie bitte auch die passende Fußbewegung.\n\nDie für die Aufgabe relevanten Bewegungen betreffen ausschließlich die Beine. Armbewegungen sollen nicht demonstriert werden - lassen Sie diese bitte während des gesamten Tests entspannt auf Ihrem Schoß / den Armlehnen liegen.",
     "audio": "Pantomime unilateral"},
    {"typ": "foto", "start": 7, "ende": 11, "titel": "Pantomime des Objektgebrauchs - Bilaterale Bewegungen",
     "text": "Die nächsten Objekte erfordern eine Bewegung beider Beine. Zeigen Sie weiterhin mit Ihren Beinen und Füßen, wie man die Gegenstände benutzt. Armbewegungen sind auch hier nicht Teil der Aufgabe und Ihre Arme können weiterhin auf Ihrem Schoß / den Armlehnen liegen bleiben.",
     "audio": "Pantomime bilateral"},
    {"typ": "video", "start": 0, "ende": 4, "titel": "Imitation von Gesten - Unilateral BL",
     "text": "Bitte führen Sie mit Ihrem dominanten Bein und dominanten Fuß möglichst genau die Bewegung aus, die ich Ihnen vormache. Ich werde die Bewegung spiegelbildlich demonstrieren.\n\nJede Bewegung beginnt und endet in dieser Ausgangsposition. Beginnen Sie bitte mit der Imitation erst, nachdem ich diese Ausgangsposition wieder eingenommen habe. Achten Sie dabei genau auf die Einzelheiten der Bewegungen sowie auf die Anzahl der Wiederholungen.",
     "audio": "bedeutungslos unilateral"},
    {"typ": "video", "start": 5, "ende": 9, "titel": "Imitation von Gesten - Bilateral BL",
     "text": "Die nächsten Bewegungen, die ich vormachen werde, beziehen beide Beine ein. Bitte machen Sie auch diese Bewegungen so genau wie möglich nach. Ich werde die Bewegung spiegelbildlich demonstrieren.\n\nJede Bewegung beginnt und endet wieder in dieser Ausgangsposition. Beginnen Sie bitte mit der Imitation erst, nachdem ich diese Ausgangsposition wieder eingenommen habe. Achten Sie dabei genau auf die Einzelheiten der Bewegungen sowie auf die Anzahl der Wiederholungen.",
     "audio": "bedeutungslos bilateral"},
    {"typ": "video", "start": 10, "ende": 14, "titel": "Imitation von Gesten - Unilateral BV",
     "text": "Bitte führen Sie mit Ihrem dominanten Bein und dominanten Fuß möglichst genau die Bewegung aus, die ich Ihnen vormache. Ich werde die Bewegung spiegelbildlich demonstrieren.\n\nJede Bewegung beginnt und endet in dieser Ausgangsposition. Beginnen Sie bitte mit der Imitation erst, nachdem ich diese Ausgangsposition wieder eingenommen habe. Achten Sie dabei genau auf die Einzelheiten der Bewegungen sowie auf die Anzahl an Wiederholungen.",
     "audio": "bedeutungsvoll unilateral"},
    {"typ": "video", "start": 15, "ende": 19, "titel": "Imitation von Gesten - Unilateral BV",
     "text": "Die nächsten Bewegungen, die ich vormachen werde, beziehen beide Beine ein. Bitte machen Sie auch diese Bewegungen so genau wie möglich nach. Ich werde die Bewegung spiegelbildlich demonstrieren.\n\nJede Bewegung beginnt und endet wieder in dieser Ausgangsposition. Beginnen Sie bitte mit der Imitation direkt, nachdem ich diese Ausgangsposition wieder eingenommen habe. Achten Sie dabei genau auf die Einzelheiten der Bewegungen.""",
     "audio": "bedeutungsvoll bilateral"},
]

aktueller_testblock = 0

# Abschnitte der Erklärungen für die jeweiligen Testblöcke

audio_zeitstempel = {
    "Anleitung Testleitung": (4, 57),
    "Pantomime unilateral": (72, 105),
    "Pantomime bilateral": (170, 191),
    "bedeutungslos unilateral": (259, 292),
    "bedeutungslos bilateral": (437, 472),
    "bedeutungsvoll unilateral": (589, 621),
    "bedeutungsvoll bilateral": (708, 743)
}

label_ueberschrift_testblock = tk.Label(fenster, font=("Calibri", 18, "bold"), padx=20, pady=10)
label_ueberschrift_testblock.pack()
label_ueberschrift_testblock.pack_forget()

label_text_testblock = tk.Label(fenster, justify="left", padx=20, pady=20, font=("Calibri", 14), wraplength=700)
label_text_testblock.pack()
label_text_testblock.pack_forget()

def zeige_testblock(nr):
    """Zeigt die Instruktionsseite für den Testblock mit der angegebenen Nummer."""
    global aktueller_testblock
    aktueller_testblock = nr
    testblock = testbloecke[nr]

    label_ueberschrift_testblock.config(text=testblock["titel"])
    label_text_testblock.config(text=testblock["text"])
    label_ueberschrift_testblock.pack()
    label_text_testblock.pack()
    button_zurueck_testblock.pack()
    button_weiter_testblock.pack()

    spiele_audio(testblock["audio"])

def weiter_von_testblock_klick():
    """Startet die Fotos/Videos der aktuellen Testblock."""
    global aktueller_index, aktueller_video_index
    stoppe_audio()
    testblock = testbloecke[aktueller_testblock]

    label_ueberschrift_testblock.pack_forget()
    label_text_testblock.pack_forget()
    button_zurueck_testblock.pack_forget()
    button_weiter_testblock.pack_forget()

    if testblock["typ"] == "foto":
        aktueller_index = testblock["start"]
        button_voriges_foto.pack()
        button_naechstes_foto.pack()
        zeige_foto()
    else:
        aktueller_video_index = testblock["start"]
        label_video.pack()
        button_voriges_video.pack()
        button_video_replay.pack()
        button_naechstes_video.pack()
        zeige_video()

def zurueck_von_testblock_klick():
    """Springt zum vorherigen Testblock (letztes Element) oder zur Anleitung zurück."""
    global aktueller_index, aktueller_video_index, aktueller_testblock
    stoppe_audio()

    label_ueberschrift_testblock.pack_forget()
    label_text_testblock.pack_forget()
    button_zurueck_testblock.pack_forget()
    button_weiter_testblock.pack_forget()

    if aktueller_testblock == 0:
        label_ueberschrift.pack()
        label_anleitung.pack()
        button_zurueck_zu_formular_anleitung.pack()
        button_start.pack()
        spiele_audio("Anleitung Testleitung")
    else:
        aktueller_testblock = aktueller_testblock - 1
        vorherige = testbloecke[aktueller_testblock]
        if vorherige["typ"] == "foto":
            aktueller_index = vorherige["ende"]
            button_voriges_foto.pack()
            button_naechstes_foto.pack()
            zeige_foto()
        else:
            aktueller_video_index = vorherige["ende"]
            button_voriges_video.pack()
            button_video_replay.pack()
            button_naechstes_video.pack()
            zeige_video()

button_zurueck_testblock = tk.Button(fenster, text="Zurück", command=zurueck_von_testblock_klick)
button_zurueck_testblock.pack()
button_zurueck_testblock.pack_forget()

button_weiter_testblock = tk.Button(fenster, text="Weiter", command=weiter_von_testblock_klick)
button_weiter_testblock.pack()
button_weiter_testblock.pack_forget()

fenster.mainloop()
