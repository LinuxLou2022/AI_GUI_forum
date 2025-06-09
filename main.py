# Rev 0.0.2 – Adds interaction history panel + file log

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime
import os

from core.model_interface import run_prompt_via_powershell

from tkinter import Toplevel, Checkbutton, IntVar, Label, Button
from core.model_interface import (
    get_installed_models,
    load_model_attributes,
    save_model_attributes
)



class AIGUIForum(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("AI GUI Forum")
        self.geometry("1000x600")

        # Menu Bar
        menu_bar = tk.Menu(self)

        # --- File Menu ---
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="New Session", command=self.new_session)
        file_menu.add_command(label="Open", command=self.open_history_file)
        file_menu.add_command(label="Save", command=self.save_history_file)
        menu_bar.add_cascade(label="File", menu=file_menu)

        # --- Config Menu ---
        config_menu = tk.Menu(menu_bar, tearoff=0)
        config_menu.add_command(label="Define Type", command=self.define_type)
        config_menu.add_command(label="Active Models", command=self.show_active_models)
        menu_bar.add_cascade(label="Config", menu=config_menu)

        # --- About Menu ---
        about_menu = tk.Menu(menu_bar, tearoff=0)
        about_menu.add_command(label="Credits", command=self.show_credits)
        about_menu.add_command(label="Licenses", command=self.show_licenses)
        menu_bar.add_cascade(label="About", menu=about_menu)

        self.config(menu=menu_bar)

        # Create layout container
        container = tk.Frame(self)
        container.pack(fill='both', expand=True, padx=10, pady=10)

        # Left side (main input/output stack)
        left_panel = tk.Frame(container)
        left_panel.pack(side='left', fill='both', expand=True)

        # Model selection dropdown
        self.model_var = tk.StringVar()
        self.model_dropdown = ttk.Combobox(left_panel, textvariable=self.model_var)
        #self.model_dropdown['values'] = ["Mistral", "Qwen2.5-Coder", "StarCoder2"]
        from core.model_interface import get_installed_models

        models = get_installed_models()
        self.model_dropdown['values'] = models
        if models:
            self.model_dropdown.current(0)
        self.model_dropdown.current(0)
        self.model_dropdown.pack(pady=(0, 10))

        # Prompt input box
        self.prompt_input = tk.Text(left_panel, height=8, width=80)
        self.prompt_input.pack(pady=(0, 10))

        # Submit button
        self.submit_button = tk.Button(left_panel, text="Submit Prompt", command=self.handle_submit)
        self.submit_button.pack(pady=(0, 10))

        # Output box
        self.output_display = tk.Text(left_panel, height=20, width=80, state='disabled', wrap='word')
        self.output_display.pack()

        # Right side: history panel
        self.history_log = tk.Text(container, width=40, state='disabled', wrap='word')
        self.history_log.pack(side='right', fill='y', padx=(10, 0))

        # Setup history file
        timestamp = datetime.now().strftime("%d%m%Y_%H%M")
        self.history_filename = f"history{timestamp}.txt"
        with open(self.history_filename, 'w', encoding='utf-8') as f:
            f.write("AI GUI Forum Interaction History\n\n")

    def handle_submit(self):
        selected_model = self.model_var.get()
        prompt = self.prompt_input.get("1.0", tk.END).strip()

        if not prompt:
            self.display_response("[Warning] Prompt is empty.")
            return

        response = run_prompt_via_powershell(selected_model, prompt)
        self.display_response(response)
        self.update_history(prompt, selected_model, response)

    def display_response(self, text):
        self.output_display.config(state='normal')
        self.output_display.delete("1.0", tk.END)
        self.output_display.insert(tk.END, text)
        self.output_display.config(state='disabled')

    def update_history(self, user_prompt, model_name, model_response):
        entry = (
            f"User → {model_name}:\n{user_prompt}\n\n"
            f"{model_name} Response:\n{model_response}\n\n"
            "-------------------------\n\n"
        )

        # GUI
        self.history_log.config(state='normal')
        self.history_log.insert(tk.END, entry)
        self.history_log.config(state='disabled')
        self.history_log.see(tk.END)

        # File
        with open(self.history_filename, 'a', encoding='utf-8') as f:
            f.write(entry)

    def new_session(self):
        # Clear all boxes and start fresh
        self.prompt_input.delete("1.0", tk.END)
        self.output_display.config(state='normal')
        self.output_display.delete("1.0", tk.END)
        self.output_display.config(state='disabled')
        self.history_log.config(state='normal')
        self.history_log.delete("1.0", tk.END)
        self.history_log.config(state='disabled')
        self.history_filename = f"history{datetime.now().strftime('%d%m%Y_%H%M')}.txt"

    def open_history_file(self):
        from tkinter.filedialog import askopenfilename
        file = askopenfilename(filetypes=[("Text Files", "*.txt")])
        if file:
            with open(file, 'r', encoding='utf-8') as f:
                content = f.read()
            self.history_log.config(state='normal')
            self.history_log.delete("1.0", tk.END)
            self.history_log.insert(tk.END, content)
            self.history_log.config(state='disabled')

    def save_history_file(self):
        from tkinter.filedialog import asksaveasfilename
        file = asksaveasfilename(defaultextension=".txt")
        if file:
            with open(file, 'w', encoding='utf-8') as f:
                content = self.history_log.get("1.0", tk.END)
                f.write(content)

    def define_type(self):
        messagebox.showinfo("Define Type", "This will later let you define model interaction roles/types.")

    def show_active_models(self):
        from core.model_interface import get_installed_models
        models = get_installed_models()
        messagebox.showinfo("Active Models", "\n".join(models))

    def show_credits(self):
        messagebox.showinfo("Credits", "Developed by Lou with support from GPT-4.\nGUI structure using Tkinter.")

    def show_licenses(self):
        messagebox.showinfo("Licenses",
                               "Ollama, StarCoder2, Mistral, and others are under their respective open licenses.")

    def define_type(self):
        attribs = ["Chat", "Code", "Math"]
        model_list = get_installed_models()
        existing_types = load_model_attributes()

        type_win = Toplevel(self)
        type_win.title("Define Model Types")

        type_vars = {}  # { model: {attr: IntVar, ...} }

        Label(type_win, text="Model", font=('Arial', 10, 'bold')).grid(row=0, column=0, padx=10, pady=5)
        for col, attr in enumerate(attribs, start=1):
            Label(type_win, text=attr, font=('Arial', 10, 'bold')).grid(row=0, column=col, padx=5)

        for row, model in enumerate(model_list, start=1):
            Label(type_win, text=model).grid(row=row, column=0, sticky='w', padx=10)
            type_vars[model] = {}
            for col, attr in enumerate(attribs, start=1):
                val = existing_types.get(model, {}).get(attr, False)
                var = IntVar(value=int(val))
                cb = Checkbutton(type_win, variable=var)
                cb.grid(row=row, column=col, padx=5)
                type_vars[model][attr] = var

        def save_and_close():
            updated = {}
            for model in type_vars:
                updated[model] = {attr: bool(var.get()) for attr, var in type_vars[model].items()}
            save_model_attributes(updated)
            type_win.destroy()

        Button(type_win, text="Save", command=save_and_close).grid(row=len(model_list) + 1, column=0, columnspan=4, pady=10)


if __name__ == "__main__":
    app = AIGUIForum()
    app.mainloop()
