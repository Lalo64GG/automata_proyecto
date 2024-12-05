import tkinter as tk
from tkinter import filedialog
from automata import process_directory

def create_app():
    root = tk.Tk()
    root.title("Simulador de Autómata")
    root.geometry("800x500")  # Ventana más grande
    root.configure(bg="#2b2b2b")  # Fondo oscuro

    # Estilo del título
    title_label = tk.Label(
        root, text="Simulador de Autómata",
        font=("Arial", 24, "bold"), bg="#2b2b2b", fg="#ffffff"
    )
    title_label.pack(pady=20)

    # Agrega un marco para centrar los elementos
    frame = tk.Frame(root, bg="#3c3f41", relief="groove", borderwidth=5)
    frame.pack(pady=20, padx=20, fill="both", expand=True)

    # Botón de procesar
    process_button = tk.Button(
        frame, text="Seleccionar Directorio y Procesar Archivos",
        command=process_directory,
        bg="#007acc", fg="white", font=("Arial", 14, "bold"),
        relief="raised", borderwidth=4, padx=20, pady=10
    )
    process_button.pack(pady=40)

    # Texto decorativo
    footer_label = tk.Label(
        frame, text="¡Selecciona un directorio para empezar!",
        font=("Arial", 14), bg="#3c3f41", fg="#ffffff"
    )
    footer_label.pack(side="bottom", pady=10)

    return root
