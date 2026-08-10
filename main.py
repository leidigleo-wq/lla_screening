# Tkinter-Modul laden, Kurzform "tk" für spätere Befehle
import tkinter as tk
import cv2
from PIL import Image, ImageTk
import time

# Erzeugt das Hauptfenster der Anwendung
fenster = tk.Tk()
fenster.title("Apraxie-Screening") # Titel in der Fensterleiste
fenster.geometry("800x600") # Startgröße des Fensters

# Anleitung für die Testleitung

label_ueberschrift = tk.Label(fenster, text="Instruktion für die Testleitung", font=("Calibri", 18, "bold"), padx=20, pady=10)
label_ueberschrift.pack()
label_ueberschrift.pack_forget()

anleitungstext = """

Das Screening wird im Sitzen durchgeführt. Platzieren Sie den Stuhl des*der Patient*in gegenüber
dem Stuhl der Testleitung mit ausreichend Abstand. Positionieren Sie den Laptop so, dass sowohl
Sie als auch der*die Patient*in den Bildschirm gut wahrnehmen können. Achten Sie darauf, dass
genügend Freiraum zum Tisch besteht, sodass die Bein- und Fußbewegungen gut sichtbar und
nicht eingeschränkt sind.
Der*Die Patient*in zieht die Schuhe aus; Socken können getragen werden. Die Ausgangsposition
ist eine hüftbreite Stellung der Beine. Der*Die Patient*in sitzt möglichst weit vorne auf
dem Stuhl, mit den Füßen flach auf dem Boden. Die Arme liegen locker auf dem Schoß oder, wenn
vorhanden, auf den Armlehnen. Alle Bewegungen werden spiegelbildlich demonstriert.

Zum Starten auf 'Start' klicken."""

label_anleitung = tk.Label(fenster, text=anleitungstext, justify="left", padx=20, pady=20, font=("Calibri", 14))
label_anleitung.pack()
label_anleitung.pack_forget()

def zurueck_zu_formular_von_anleitung_klick():
    """Blendet die Anleitung aus und zeigt wieder das Formular."""
    label_ueberschrift.pack_forget()
    label_anleitung.pack_forget()
    button_zurueck_zu_formular_anleitung.pack_forget()
    button_start.pack_forget()

    label_fuss.pack()
    radio_links.pack()
    radio_rechts.pack()
    button_weiter.pack()

def start_klick():
    """Blendet die Anleitung aus und zeigt die Hinweisseite vor den Fotos."""
    label_ueberschrift.pack()
    label_ueberschrift.pack_forget()
    label_anleitung.pack_forget()
    button_zurueck_zu_formular_anleitung.pack_forget()
    button_start.pack_forget()

    label_ueberschrift_fotos.pack()
    label_hinweis_fotos.pack()
    button_zurueck_zu_formular.pack()
    button_weiter_zu_fotos.pack()

button_zurueck_zu_formular_anleitung = tk.Button(fenster, text="Zurück", command=zurueck_zu_formular_von_anleitung_klick)
button_zurueck_zu_formular_anleitung.pack()
button_zurueck_zu_formular_anleitung.pack_forget()

button_start = tk.Button(fenster, text="Start", command=start_klick)
button_start.pack()
button_start.pack_forget()

## Merkt sich, welcher Fuß aktuell ausgewählt ist (Standard: Links)
fuss_variable = tk.StringVar(value="links")

## Beschriftung und Auswahlmöglichkeiten für den dominanten Fuß
label_fuss = tk.Label(fenster, text="Dominanter Fuß: ")
label_fuss.pack()

radio_links = tk.Radiobutton(fenster, text="links", variable=fuss_variable, value="links")
radio_links.pack()

radio_rechts = tk.Radiobutton(fenster, text="rechts", variable=fuss_variable, value="rechts")
radio_rechts.pack()

# Hinweistext vor den Objektfotos
label_ueberschrift_fotos = tk.Label(fenster, text="Instruktion", font=("Calibri", 18, "bold"), padx=20, pady=10)

hinweistext_fotos = """

Bitte zeigen Sie mit Ihrem dominanten Bein und dominanten Fuß, wie man diesen Gegenstand
benutzt. Falls die korrekte Ausführung der Bewegung auch die Ausrichtung des Fußes erfordert,
machen Sie bitte auch die passende Fußbewegung."""

label_hinweis_fotos = tk.Label(fenster, text=hinweistext_fotos, justify="left", padx=20, pady=20, font=("Calibri", 14))
label_hinweis_fotos.pack()
label_hinweis_fotos.pack_forget()

def zurueck_zu_anleitung_von_fotos_klick():
    """Blendet die Instruktion vor den Fotos aus und zeigt wieder die Anleitung."""
    label_ueberschrift_fotos.pack_forget()
    label_hinweis_fotos.pack_forget()
    button_zurueck_zu_formular.pack_forget()
    button_weiter_zu_fotos.pack_forget()

    label_ueberschrift.pack()
    label_anleitung.pack()
    button_zurueck_zu_formular_anleitung.pack()
    button_start.pack()

def weiter_zu_fotos_klick():
    """Blendet den Hinweistext aus und startet die Fotos"""
    label_ueberschrift_fotos.pack_forget()
    label_hinweis_fotos.pack_forget()
    button_zurueck_zu_formular.pack_forget()
    button_weiter_zu_fotos.pack_forget()

    button_voriges_foto.pack()
    button_naechstes_foto.pack()
    zeige_foto()

# Button, der zurück zur Startseite führt
button_zurueck_zu_formular = tk.Button(fenster, text="Zurück", command=zurueck_zu_anleitung_von_fotos_klick)
button_zurueck_zu_formular.pack()
button_zurueck_zu_formular.pack_forget()

# Button, der zu den Fotos weiterleitet
button_weiter_zu_fotos = tk.Button(fenster, text="Weiter", command=weiter_zu_fotos_klick)
button_weiter_zu_fotos.pack()
button_weiter_zu_fotos.pack_forget()

# Liste aller Objektfotos in der Reihenfolge, in der sie gezeigt werden
objekt_fotos = [
    "assets/objekte/02_Igelball.png",
    "assets/objekte/01_Fussball.png",
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

# Leeres Label, das später jeweils das aktuelle Foto anzeigt
label_bild = tk.Label(fenster)
label_bild.pack()

def zeige_foto():
    """Lädt das Foto an der aktuellen Zähler-Position und zeigt es im Label an."""
    global bild_referenz
    pfad = objekt_fotos[aktueller_index]
    bild_referenz = tk.PhotoImage(file=pfad) # Bild laden
    bild_referenz = bild_referenz.subsample(2, 2) # verkleinert auf 1/2 der Originalgröße
    label_bild.config(image=bild_referenz) # Bild ins Label einsetzen

def naechstes_foto():
    """Wird bei Klick auf 'Weiter' (Fotos-Phase) aufgerufen, zeigt das nächste Foto oder die Hinweisseite vor den Videos."""
    global aktueller_index
    aktueller_index = aktueller_index + 1
    if aktueller_index < len(objekt_fotos):
        zeige_foto()
    else:
        # Fotos-Bereich ausblenden
        label_bild.config(image="")
        button_voriges_foto.pack_forget()
        button_naechstes_foto.pack_forget()

        # Hinweisseite vor den Videos einblenden
        label_ueberschrift_videos.pack()
        label_hinweis_videos.pack()
        button_zurueck_zu_fotos.pack()
        button_weiter_zu_videos.pack()

def voriges_foto():
    """Wird bei Klick auf 'Zurück' aufgerufen, zeigt das vorherige Foto."""
    global aktueller_index
    if aktueller_index > 0:
        aktueller_index = aktueller_index - 1
        zeige_foto()
    else:
        # von erstem Foto zurück zu Instruktion Fotos
        label_bild.config(image="")
        button_voriges_foto.pack_forget()
        button_naechstes_foto.pack_forget()

        label_ueberschrift_fotos.pack()
        label_hinweis_fotos.pack() # Hinweisseite statt Formular
        button_zurueck_zu_formular.pack()
        button_weiter_zu_fotos.pack()

# Next-Button für die Foto-Phase
button_naechstes_foto = tk.Button(fenster, text="Weiter", command=naechstes_foto)
button_naechstes_foto.pack()
button_naechstes_foto.pack_forget() # direkt wieder verstecken

# Back-Button für die Foto-Phase
button_voriges_foto = tk.Button(fenster, text="Zurück", command=voriges_foto)
button_voriges_foto.pack()
button_voriges_foto.pack_forget()

# Funktion, die beim Klick auf "Weiter" ausgeführt wird
def weiter_klick():
    """Liest den dominanten Fuß aus und zeigt die Anleitung für die Testleitung."""
    print("Dominanter Fuß:", fuss_variable.get())

    # Fuß-Auswahl ausblenden
    label_fuss.pack_forget()
    radio_links.pack_forget()
    radio_rechts.pack_forget()
    button_weiter.pack_forget()

    # Anleitungsseite einblenden
    label_ueberschrift.pack()
    label_anleitung.pack()
    button_zurueck_zu_formular_anleitung.pack()
    button_start.pack()

# Button, der die obige Funktion beim Klick aufruft
button_weiter = tk.Button(fenster, text="Weiter", command=weiter_klick)
button_weiter.pack()

# Zwischenseite: Hinweistext vor den Bewegungsvideos

label_ueberschrift_videos = tk.Label(fenster, text="Instruktion", font=("Arial", 16, "bold"), padx=20, pady=10)
label_ueberschrift_videos.pack()
label_ueberschrift_videos.pack_forget()

hinweistext_videos = """
Bitte führen Sie mit Ihrem dominanten Bein und dominanten Fuß möglichst genau die Bewegung
aus, die Sie auf dem Bildschirm sehen. Führen Sie die Bewegungen spiegelbildlich zum im Video
gezeigten Ablauf aus. Jede Bewegung beginnt und endet in der Ausgangsposition (hüftbreite
Beinposition). Beginnen Sie mit der Imitation erst, wenn im Video die Ausgangsposition wieder
eingenommen wurde. Achten Sie dabei genau auf die Einzelheiten der Bewegungen sowie auf die
Anzahl der Wiederholungen."""

label_hinweis_videos = tk.Label(fenster, text=hinweistext_videos, justify="left", padx=20, pady=20, font=("Calibri", 14))
label_hinweis_videos.pack()
label_hinweis_videos.pack_forget()

def zurueck_zu_fotos_von_videos_klick():
    """Blendet die Hinweisseite aus und zeigt wieder das letzte Foto."""
    global aktueller_index
    label_ueberschrift_videos.pack_forget()
    label_hinweis_videos.pack_forget()
    button_zurueck_zu_fotos.pack_forget()
    button_weiter_zu_videos.pack_forget()

    aktueller_index = len(objekt_fotos) - 1
    button_voriges_foto.pack()
    button_naechstes_foto.pack()
    zeige_foto()

def weiter_zu_videos_klick():
    """Blendet die Hinweisseite aus und startet die Videos."""
    label_ueberschrift_videos.pack_forget()
    label_hinweis_videos.pack_forget()
    button_zurueck_zu_fotos.pack_forget()
    button_weiter_zu_videos.pack_forget()

    label_video.pack()
    button_voriges_video.pack()
    button_video_replay.pack()
    button_naechstes_video.pack()
    zeige_video()

button_zurueck_zu_fotos = tk.Button(fenster, text="Zurück", command=zurueck_zu_fotos_von_videos_klick)
button_zurueck_zu_fotos.pack()
button_zurueck_zu_fotos.pack_forget()

button_weiter_zu_videos = tk.Button(fenster, text="Weiter", command=weiter_zu_videos_klick)
button_weiter_zu_videos.pack()
button_weiter_zu_videos.pack_forget()

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

    """sorgt dafür, dass Video in tatsächlicher Framerate ausgelesen wird."""
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
        frame = cv2.resize(frame, (640, 360))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        bild = Image.fromarray(frame)
        bild_tk = ImageTk.PhotoImage(image=bild)
        label_video.image = bild_tk
        label_video.config(image=bild_tk)

        dauer = (time.time() - start) * 1000
        verbleibende_wartezeit = max(1, video_delay - int(dauer)) # zieht die tatsächlich schon verbrauchte Verarbeitungszeit von der Ziel-Wartezeit ab
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
    """Wird bei Klick auf 'Weiter' (Video-Phase) aufgerufen, zeigt das nächste Video oder beendet das Screening."""
    global aktueller_video_index
    aktueller_video_index = aktueller_video_index + 1
    if aktueller_video_index < len(video_ids):
        zeige_video()
    else:
        print("Alle Videos gezeigt - Screening beendet")

def voriges_video():
    """Wird bei Klick auf 'Zurück' (Video-Phase) aufgerufen, zeigt das vorherige Video."""
    global aktueller_video_index
    if aktueller_video_index > 0:
        aktueller_video_index = aktueller_video_index - 1
        zeige_video()
    
button_voriges_video = tk.Button(fenster, text="Zurück", command=voriges_video)
button_voriges_video.pack()
button_voriges_video.pack_forget()

button_naechstes_video = tk.Button(fenster, text="Weiter", command=naechstes_video)
button_naechstes_video.pack()
button_naechstes_video.pack_forget()
# Startet die Warteschleife - hält das Fenster offen und reagiert auf Eingaben

fenster.mainloop()
