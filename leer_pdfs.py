import tkinter as tk
from tkinter import messagebox, filedialog
import PyPDF2

from pdf import PDF
            
        
def merge_pdfs():
    """Merge all the PDFs in the list"""
    merger = PyPDF2.PdfMerger()
    
    if not PDF.pdfs:
        messagebox.showerror("Error", "No hay PDFs para unir")
        return
    
    for pdf in PDF.pdfs:
        merger.append(PyPDF2.PdfReader(pdf.path))
    try:
        merger.write(file_name := filedialog.asksaveasfilename(filetypes=[("PDF files", "*.pdf")], defaultextension=".pdf"))
        messagebox.showinfo("Info", "PDFs merged successfully")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")        
        
def open_pdf():
    """Open a file and read its content"""
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if file_path:
        try:
            with open(file_path, 'rb') as path:
                reader = PyPDF2.PdfReader(path)
                content = ""
                for page in reader.pages:
                    text = page.extract_text()
                    if text:
                        content += text
                if PDF.exists(file_path):
                    messagebox.showinfo("Info", "El archivo ya fue leído")
                else:
                    PDF.pdfs.append(PDF(file_path, content))

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo leer el archivo: {e}")

root = tk.Tk()

root.title("Leer PDFs")

button_open = tk.Button(root, text="Abrir archivo", command=open_pdf)
button_open.config(width=20, height=2)
button_open.pack(pady=20)

listbox = tk.Listbox(root, width=80, height=20)
listbox.pack(pady=20)


button_merge = tk.Button(root, text="Merge PDFs", command=merge_pdfs)
button_merge.config(width=20, height=2)
button_merge.pack(pady=20)

def update_listbox():
    listbox.delete(0, tk.END)
    for idx, pdf in enumerate(PDF.pdfs):
        listbox.insert(tk.END, str(pdf))
        listbox.itemconfig(idx, {'bg':'white'})
        #listbox.bind('<Double-1>', on_double_click)
        listbox.bind('<Button-3>', on_right_click)

def on_double_click(event):
    selection = listbox.curselection()
    if selection:
        delete_pdf(selection[0])

def on_right_click(event):
    """
    Menu interactivo para tener varias opciones
    Args:
        event (_type_): _description_
    """
    selection = listbox.nearest(event.y)
    if selection >= 0 and selection < listbox.size():
        listbox.selection_set(selection)
        menu = tk.Menu(root, tearoff=0)
        menu.add_command(label="Eliminar", command=lambda: delete_pdf(listbox.curselection()[0]))
        
        menu.add_command(label="Ver informacion" , command=lambda: messagebox.showinfo("Informacion", PDF.pdfs[listbox.curselection()[0]].detailed_info()))
        menu.post(event.x_root, event.y_root)
        

def delete_pdf(index):
    del PDF.pdfs[index]
    update_listbox()

button_open.config(command=lambda: [open_pdf(), update_listbox()])



root.geometry("800x600")

if __name__ == "__main__":
    root.mainloop()