import os
import getpass
import shutil
from tkinter import *
from tkinter import filedialog

# Benutzername heruaslesen
username = getpass.getuser()

# Funktion für Verzeichnis wählen
def choose_directory():
    path = filedialog.askdirectory(title="Speicherort wählen")
    if path:
        path_entry.delete(0, END)      # delete old path
        path_entry.insert(0, path)     # paste new path

# Ein Warnfenster erstellen mit benutzerdefiniertem Text
def show_window_warning(warn_text=str):
    window_warning = Tk()
    window_warning.eval(f'tk::PlaceWindow . center')
    window_warning.title("Achtung!")
    warning_label = Label(window_warning, text=warn_text)
    warning_label.pack()

#  Projekt einrichten mit allen Ordner und Files
def create_project():
    project_name = project_name_entry.get()
    path = path_entry.get()


    if project_name == "":
        show_window_warning("Bitte ein Projektname eingeben!")
        return
    
    if path == "":
        show_window_warning("Bitte ein Speicherort wählen!")
        return
       

    # Erstelle die Ordnerstruktur
    python_path = os.path.join(path, 'Python')
    files_path = os.path.join(python_path, 'files')
    abbildungen_path = os.path.join(files_path, 'Abbildungen')
    setup_path = os.path.join(python_path, 'setup')

    os.makedirs(abbildungen_path, exist_ok=True)
    os.makedirs(setup_path, exist_ok=True)

    # Erstelle die .code-workspace Datei im Python-Ordner
    workspace_file = os.path.join(python_path, f"{project_name}_{username}_workspace.code-workspace")
    workspace_content = f'''{{
    "folders": [
        {{
            "name": "{project_name}",
            "path": "."
        }},
        {{
            "name": "engicalc",
            "path": "C:/Users/{username}/engicalc"
        }}
    ],
    "settings": {{
        "python.analysis.extraPaths": [
            "${{workspaceFolder}}",  
            "C:/Users/{username}/engicalc"
        ],
        "python.envFile": "./setup/engicalc/.env"
    }}
}}'''
    with open(workspace_file, 'w') as f:
        f.write(workspace_content)

    # Erstelle die .env Datei im setup-Ordner
    env_file = os.path.join(setup_path, 'engicalc.env')
    with open(env_file, 'w') as f:
        f.write("PYTHONPATH=${PYTHONPATH};C:/Users/${USERNAME}/engicalc")

    # Notebook-Vorlage kopieren
    template_notebook = './files/template.ipynb'  # Pfad zur Vorlage
    target_notebook = os.path.join(files_path, f'{project_name}.ipynb')  # Zielname anpassen

    try:
        shutil.copyfile(template_notebook, target_notebook)
    except FileNotFoundError:
        message = "Notebook-Vorlage nicht gefunden. Stelle sicher, dass 'files/template_notebook.ipynb' existiert."

    # Beispielbild kopieren
    template_image = './files/Bild_01.jpg'  # Pfad zur Vorlage
    target_image = os.path.join(abbildungen_path, 'Bild_01.jpg')  # Zielname anpassen

    try:
        shutil.copyfile(template_image, target_image)
    except FileNotFoundError:
        message = "Bild-Vorlage nicht gefunden. Stelle sicher, dass 'files/Bild_01.jpg' existiert."

    # Word-Vorlage kopieren
    template_Word = './files/Vorlage_Python_Export.docx'  # Pfad zur Vorlage
    target_Word = os.path.join(setup_path, 'Vorlage_Python_Export.docx')  # Zielname anpassen

    try:
        shutil.copyfile(template_Word, target_Word)
    except FileNotFoundError:
        message = "Word-Vorlage nicht gefunden. Stelle sicher, dass 'files/Vorlage_Python_Export.docx' existiert."

    show_window_warning(message)

    # Deaktiviere den Knopf nach dem Erstellen, damit nicht versehentlich eine 2. Ordnerstruktur erstellt wird.
    create_button.config(state='disabled')
    return



# create a window
window = Tk()
window.eval('tk::PlaceWindow . center')

# window title
window.title("Neues Projekt einrichten")



# Projektname erfassen: Label erstellen und platzieren
project_name_label = Label(window, text="Projektname:", width=20)
project_name_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")

# Eingabefeld für den Projektnamen
project_name_entry = Entry(window, width=50)
project_name_entry.grid(row=0, column=1, padx=10, pady=10)


# Speicherort erfassen: Label erstellen und platzieren
path_button = Button(window, text="Speicherort wählen:", width=20, command=choose_directory)
path_button.grid(row=1, column=0, padx=10, pady=10, sticky="e")

# Eingabefeld für den Speicherort
path_entry = Entry(window, width=50)
path_entry.grid(row=1, column=1, padx=10, pady=10)

# Button für Projekt einrichten 
create_button = Button(window, text="Projekt erstellen", width=20, command=create_project)
create_button.grid(row=2, column=0, padx=10, pady=10, sticky="e")

# Button für Beenden
leave_button = Button(window, text="Beenden",width=42 , command=window.destroy)
leave_button.grid(row=2, column=1, padx=10, pady=10, sticky="e")

# warten auf Eingabe Benutzer
window.mainloop()