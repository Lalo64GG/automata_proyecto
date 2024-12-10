import os
import csv
from tkinter import messagebox, filedialog
from transitions import transitions
from datetime import datetime  # Para manejar fechas y horas


class Automata:
    def __init__(self):
        self.state = 'q0'
        self.final_states = ['q33']
        self.transitions = transitions  

    def transition(self, symbol):
        key = (self.state, symbol)
        print(f"Current State: {self.state}, Symbol: '{symbol}'")
        if key in self.transitions:
            self.state = self.transitions[key]
            print(f"Transitioning to: {self.state}")
            self.error_message = None
        else:
            self.error_message = f"No hay transición definida desde el estado '{self.state}' con el símbolo '{symbol}'."
            self.state = ''  # Estado de rechazo
            print(f"Rechazado: {self.error_message}")

    def is_accepting(self):
        return self.state in self.final_states

    def reset(self):
        self.state = 'q0'
        self.error_message = None


def parse_filename(filename_no_ext):
    parts = filename_no_ext.split(' - ')
    if len(parts) == 4:
        return tuple(part.strip() for part in parts)
    return None


def generate_csv(data):
    # Obtener la fecha y hora actuales
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    default_filename = f"resultado_{timestamp}.csv"

    # Solicitar al usuario dónde guardar el archivo con un nombre predeterminado
    save_path = filedialog.asksaveasfilename(
        initialfile=default_filename,
        defaultextension=".csv",
        filetypes=[("CSV files", "*.csv")]
    )
    
    if not save_path:
        messagebox.showwarning("Guardado cancelado", "No se guardó el archivo CSV.")
        return

    with open(save_path, 'w', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(["Asignatura", "Cuatrimestre y Grupo", "Docente", "Periodo"])
        csvwriter.writerows(data)

    messagebox.showinfo("CSV generado", f"El archivo CSV ha sido guardado en:\n{save_path}")


def generate_text_file(data):
    # Similar lógica para el nombre único del archivo de texto
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    default_filename = f"rechazados_{timestamp}.txt"

    save_path = filedialog.asksaveasfilename(
        initialfile=default_filename,
        defaultextension=".txt",
        filetypes=[("Text files", "*.txt")]
    )
    
    if not save_path:
        messagebox.showwarning("Guardado cancelado", "No se guardó el archivo de texto.")
        return

    with open(save_path, 'w', encoding='utf-8') as txtfile:
        txtfile.write("Datos Rechazados:\n\n")
        for filename, content in data:
            txtfile.write(f"Archivo: {filename}\nContenido: {content}\n\n")

    messagebox.showinfo("Archivo de texto generado", f"El archivo de texto ha sido guardado en:\n{save_path}")


def process_directory():
    directory = filedialog.askdirectory()
    if not directory:
        messagebox.showwarning("Directorio no seleccionado", "Por favor, selecciona un directorio para continuar.")
        return

    accepted_data = []
    rejected_data = []

    for filename in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, filename)):
            filename_with_ext = filename.strip()
            print(f"Procesando archivo: {filename_with_ext}")
            automata = Automata()
            for symbol in filename_with_ext:
                automata.transition(symbol)
                if automata.error_message:
                    print(f"Error en archivo '{filename}': {automata.error_message}")
                    break

            print(f"Estado final para el archivo '{filename}': {automata.state}")
            if automata.is_accepting():
                filename_no_ext = os.path.splitext(filename)[0].strip()
                fields = parse_filename(filename_no_ext)
                if fields:
                    accepted_data.append(fields)
                else:
                    rejected_data.append((filename, filename_no_ext))
            else:
                rejected_data.append((filename, filename_with_ext))

    if accepted_data:
        generate_csv(accepted_data)
    else:
        messagebox.showinfo("Resultados", "No hubo datos aceptados para generar el archivo CSV.")

    if rejected_data:
        generate_text_file(rejected_data)
    else:
        messagebox.showinfo("Resultados", "No hubo datos rechazados para generar el archivo de texto.")
