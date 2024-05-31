from cat.mad_hatter.decorators import hook,plugin
import os
import json
from cat.looking_glass.cheshire_cat import CheshireCat


def save_json(datas, filename, path):
    # Assicurati che il percorso esista, altrimenti crealo
    if not os.path.exists(path):
        os.makedirs(path)
    
    # Crea il percorso completo del file
    full_path = os.path.join(path, filename)
    
    # Scrivi la lista aggiornata nel file JSON
    with open(full_path, 'w') as file:
        json.dump(datas, file)

def read_json(filename, path):
    # Crea il percorso completo del file
    full_path = os.path.join(path, filename)
    
    # Verifica se il file esiste e non è vuoto
    if not os.path.exists(full_path) or os.path.getsize(full_path) == 0:
        return ["nessuna classificazione"]  # Ritorna una lista vuota se il file non esiste o è vuoto
    
    # Leggi il contenuto del file JSON e ritorna la lista
    with open(full_path, 'r') as file:
        try:
            datas = json.load(file)
        except json.JSONDecodeError:
            # Gestisci il caso in cui il file non è un JSON valido
            return ["nessuna classificazione"]

    return datas 

def stampa(testo, nome_file, path):
    """
    Writes or appends text to a text file. If the file does not exist, creates it with the text as initial content.
    If the file exists, appends the text to the existing content.

    Args:
    testo (str): Text to be written or appended.
    nome_file (str): The name of the file.
    percorso (str): The directory path.
    """
    percorso_completo = os.path.join(path, nome_file)
    
    # Ensure the directory exists, otherwise create it
    if not os.path.exists(path):
        os.makedirs(path)
    
    # Determine the mode based on the existence of the file: append if it exists, write if not
    mode = 'a' if os.path.exists(percorso_completo) else 'w'
    
    # Write or append text to the file
    with open(percorso_completo, mode, encoding='utf-8') as file:
        file.write(testo + "\n")  # Append new text with a newline for readability

def get_current_directory():
    """
    Restituisce il percorso della cartella in cui è eseguito il file Python in esecuzione.
    """
    current_directory = os.path.dirname(os.path.abspath(__file__))
    return current_directory

ccat = CheshireCat()

@plugin
def save_settings(settings):
    
    dir=get_current_directory()

    metadata_key=settings["metadata_key"]
    metadata_value=settings["metadata_value"]
    delete_document_of_selected_metadata=settings["delete_document_of_selected_metadata"]

    if delete_document_of_selected_metadata == True:

        vector_memory = ccat.memory.vectors
        vector_memory.collections["declarative"].delete_points_by_metadata_filter({metadata_key:metadata_value})

    settings["delete_document_of_selected_metadata"]=False
    save_json(settings, "settings.json", dir)

    return settings
