import os
import tkinter as tk
from tkinter import simpledialog, messagebox, filedialog
import threading
import process_files
import email_handler
import database
import webbrowser

# Definir variáveis globais
user_email = ""
user_password = ""

def add_keyword():
    keyword = keyword_entry.get()
    if keyword:
        keywords_listbox.insert(tk.END, keyword)
        keyword_entry.delete(0, tk.END)

def delete_keyword(event=None):
    selected = keywords_listbox.curselection()
    if selected:
        keywords_listbox.delete(selected)

def copy_keyword(event=None):
    selected = keywords_listbox.curselection()
    if selected:
        keyword = keywords_listbox.get(selected)
        root.clipboard_clear()
        root.clipboard_append(keyword)

def delete_all():
    if messagebox.askyesno("Confirmação", "Deseja realmente excluir todas as palavras-chave e currículos?"):
        keywords_listbox.delete(0, tk.END)
        database.clear_resumes()
        update_resumes_listbox(all_resumes_listbox)
        update_resumes_listbox(filtered_resumes_listbox, True)

def upload_file():
    file_paths = filedialog.askopenfilenames(filetypes=[("PDF files", "*.pdf"), ("Word files", "*.docx")])
    if file_paths:
        for file_path in file_paths:
            result = process_files.process_file(file_path, keywords_listbox.get(0, tk.END))
            all_resumes_listbox.insert(tk.END, result)
        update_resumes_listbox(all_resumes_listbox)
        update_resumes_listbox(filtered_resumes_listbox, True)

def start_unseen_email_processing_thread():
    threading.Thread(target=start_unseen_email_processing).start()

def start_all_email_processing_thread():
    threading.Thread(target=start_all_email_processing).start()

def start_unseen_email_processing():
    server = email_handler.get_imap_server(user_email)
    email_handler.process_emails(server, 993, user_email, user_password, keywords_listbox.get(0, tk.END), fetch_all=False)
    root.after(0, update_resumes_listbox, all_resumes_listbox)
    root.after(0, update_resumes_listbox, filtered_resumes_listbox, True)

def start_all_email_processing():
    server = email_handler.get_imap_server(user_email)
    email_handler.process_emails(server, 993, user_email, user_password, keywords_listbox.get(0, tk.END), fetch_all=True)
    root.after(0, update_resumes_listbox, all_resumes_listbox)
    root.after(0, update_resumes_listbox, filtered_resumes_listbox, True)

def update_resumes_listbox(listbox, filter_keywords=False):
    resumes = database.get_resumes()
    listbox.delete(0, tk.END)
    keywords = [kw.lower() for kw in keywords_listbox.get(0, tk.END)]
    
    if filter_keywords:
        found = False
        for resume in resumes:
            resume_text = resume[3].lower()  # Converter texto do currículo para minúsculas
            if any(keyword in resume_text for keyword in keywords):
                listbox.insert(tk.END, f"{resume[0]} - {resume[2]} - {resume[1]}")
                found = True
        if not found:
            listbox.insert(tk.END, "Nenhum currículo contém as palavras-chaves necessárias.")
    else:
        for resume in resumes:
            listbox.insert(tk.END, f"{resume[0]} - {resume[2]} - {resume[1]}")

def copy_resume_name(event):
    selected = all_resumes_listbox.curselection()
    if selected:
        resume_name = all_resumes_listbox.get(selected[0]).split(' - ')[0]
        root.clipboard_clear()
        root.clipboard_append(resume_name)

def open_item(event, listbox):
    selected = listbox.curselection()
    if selected:
        item = listbox.get(selected).split(' - ')
        file_path = item[2]
        if os.path.exists(file_path):
            webbrowser.open('file://' + os.path.realpath(file_path))

def show_resume_context_menu(event):
    resume_context_menu.tk_popup(event.x_root, event.y_root)

def show_keyword_context_menu(event):
    keyword_context_menu.tk_popup(event.x_root, event.y_root)

def show_filtered_resumes():
    resumes = database.get_resumes()
    filtered_resumes_listbox.delete(0, tk.END)
    keywords = [kw.lower() for kw in keywords_listbox.get(0, tk.END)]
    found = False

    for resume in resumes:
        resume_text = resume[3].lower()
        if any(keyword in resume_text for keyword in keywords):
            found = True
            resume_name = resume[0]
            email = resume[2]
            file_path = resume[1]
            filtered_resumes_listbox.insert(tk.END, f"{resume_name} - {email} - {file_path}")

    if not found:
        filtered_resumes_listbox.insert(tk.END, "Nenhum currículo contém as palavras-chaves necessárias.")

def login():
    global user_email, user_password
    user_email = simpledialog.askstring("Login", "Digite seu email:")
    user_password = simpledialog.askstring("Login", "Digite sua senha:", show="*")
    
    if not user_email or not user_password:
        messagebox.showerror("Erro", "Email e senha são obrigatórios.")
        root.destroy()
    else:
        messagebox.showinfo("Sucesso", "Login realizado com sucesso!")

root = tk.Tk()
root.withdraw()  # Esconder a janela principal até o login ser feito

# Janela de Login
login()

root.deiconify()  # Mostrar a janela principal após o login
root.title("Gerenciador de Currículos")
root.geometry("1200x700")

frame_keywords = tk.LabelFrame(root, text="Palavras-chave", padx=10, pady=10)
frame_keywords.pack(fill="both", expand="yes", padx=10, pady=5)

keyword_entry = tk.Entry(frame_keywords)
keyword_entry.grid(row=0, column=0, padx=10, pady=5)
tk.Button(frame_keywords, text="Adicionar", command=add_keyword).grid(row=0, column=1, padx=10, pady=5)

keywords_frame = tk.Frame(frame_keywords)
keywords_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=5)

keywords_scrollbar_y = tk.Scrollbar(keywords_frame, orient="vertical")
keywords_scrollbar_x = tk.Scrollbar(keywords_frame, orient="horizontal")

keywords_listbox = tk.Listbox(keywords_frame, height=6, yscrollcommand=keywords_scrollbar_y.set, xscrollcommand=keywords_scrollbar_x.set)
keywords_listbox.pack(side="left", fill="both", expand=True)

keywords_scrollbar_y.pack(side="right", fill="y")
keywords_scrollbar_x.pack(side="bottom", fill="x")

keywords_scrollbar_y.config(command=keywords_listbox.yview)
keywords_scrollbar_x.config(command=keywords_listbox.xview)

keyword_context_menu = tk.Menu(root, tearoff=0)
keyword_context_menu.add_command(label="Copiar", command=copy_keyword)
keyword_context_menu.add_command(label="Excluir", command=delete_keyword)

keywords_listbox.bind("<Button-3>", show_keyword_context_menu)

frame_actions = tk.Frame(root, padx=10, pady=10)
frame_actions.pack(fill="both", expand="yes", padx=10, pady=5)

tk.Button(frame_actions, text="Enviar Currículo", command=upload_file).pack(side="left", padx=10, pady=5)
tk.Button(frame_actions, text="Processar E-mails Novos", command=start_unseen_email_processing_thread).pack(side="left", padx=10, pady=5)
tk.Button(frame_actions, text="Processar Todos os E-mails", command=start_all_email_processing_thread).pack(side="left", padx=10, pady=5)
tk.Button(frame_actions, text="Excluir Tudo", command=delete_all, fg="red").pack(side="right", padx=10, pady=5)
tk.Button(frame_actions, text="Filtrar Currículos", command=show_filtered_resumes).pack(side="right", padx=10, pady=5)

frame_resumes = tk.LabelFrame(root, text="Currículos Processados", padx=10, pady=10)
frame_resumes.pack(fill="both", expand="yes", padx=10, pady=5)

resumes_frame = tk.Frame(frame_resumes)
resumes_frame.pack(fill="both", expand=True)

resumes_scrollbar_y = tk.Scrollbar(resumes_frame, orient="vertical")
resumes_scrollbar_x = tk.Scrollbar(resumes_frame, orient="horizontal")

all_resumes_listbox = tk.Listbox(resumes_frame, width=50, height=10, yscrollcommand=resumes_scrollbar_y.set, xscrollcommand=resumes_scrollbar_x.set)
all_resumes_listbox.pack(side="left", fill="both", expand=True)

resumes_scrollbar_y.pack(side="right", fill="y")
resumes_scrollbar_x.pack(side="bottom", fill="x")

resumes_scrollbar_y.config(command=all_resumes_listbox.yview)
resumes_scrollbar_x.config(command=all_resumes_listbox.xview)

resume_context_menu = tk.Menu(root, tearoff=0)
resume_context_menu.add_command(label="Copiar Nome", command=copy_resume_name)

all_resumes_listbox.bind("<Double-Button-1>", lambda event: open_item(event, all_resumes_listbox))
all_resumes_listbox.bind("<Button-3>", show_resume_context_menu)

frame_filtered_resumes = tk.LabelFrame(root, text="Currículos Filtrados", padx=10, pady=10)
frame_filtered_resumes.pack(fill="both", expand="yes", padx=10, pady=5)

filtered_resumes_frame = tk.Frame(frame_filtered_resumes)
filtered_resumes_frame.pack(fill="both", expand=True)

filtered_resumes_scrollbar_y = tk.Scrollbar(filtered_resumes_frame, orient="vertical")
filtered_resumes_scrollbar_x = tk.Scrollbar(filtered_resumes_frame, orient="horizontal")

filtered_resumes_listbox = tk.Listbox(filtered_resumes_frame, width=50, height=10, yscrollcommand=filtered_resumes_scrollbar_y.set, xscrollcommand=filtered_resumes_scrollbar_x.set)
filtered_resumes_listbox.pack(side="left", fill="both", expand=True)

filtered_resumes_scrollbar_y.pack(side="right", fill="y")
filtered_resumes_scrollbar_x.pack(side="bottom", fill="x")

filtered_resumes_scrollbar_y.config(command=filtered_resumes_listbox.yview)
filtered_resumes_scrollbar_x.config(command=filtered_resumes_listbox.xview)

filtered_resumes_listbox.bind("<Double-Button-1>", lambda event: open_item(event, filtered_resumes_listbox))

database.init_db()

update_resumes_listbox(all_resumes_listbox)

root.mainloop()