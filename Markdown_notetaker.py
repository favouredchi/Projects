# Create a markdown note-taking app allows users to create, open, edit, save, and preview markdown files

import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from tkinter.scrolledtext import ScrolledText
import os
import markdown2
from flask import Flask, request, jsonify
import language_tool_python
import re

app = Flask(__name__)
tool = language_tool_python.LanguageTool('en-US')

@app.route("/spellcheck", methods=["POST"])
def spellcheck():
    data = request.json
    text = data["text"]
    tool = language_tool_python.LanguageTool('en-US')
    matches = tool.check(text)
    return jsonify(matches)

@app.route("/markdown", methods=["POST"])
def markdown():
    data = request.json
    text = data["text"]
    html = markdown2.markdown(text)
    return jsonify(html)

class MarkdownNotetaker:
    def __init__(self, root):
        self.root = root
        self.root.title("Markdown Notetaker")
        self.text = ScrolledText(self.root, wrap=tk.WORD)
        self.text.pack(expand=True, fill="both")
        self.menu = tk.Menu(self.root)
        self.root.config(menu=self.menu)
        self.file_menu = tk.Menu(self.menu, tearoff=False)
        self.menu.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="New", command=self.new_file)
        self.file_menu.add_command(label="Open", command=self.open_file)
        self.file_menu.add_command(label="Save", command=self.save_file)
        self.file_menu.add_command(label="Save As", command=self.save_as_file)
        self.file_menu.add_command(label="Exit", command=self.exit)
        self.edit_menu = tk.Menu(self.menu, tearoff=False)
        self.menu.add_cascade(label="Edit", menu=self.edit_menu)
        self.edit_menu.add_command(label="Spell Check", command=self.spell_check)
        self.edit_menu.add_command(label="Preview", command=self.preview)
    
    def new_file(self):
        self.text.delete("1.0", tk.END)
    
    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Markdown files", "*.md")])
        if file_path:
            with open(file_path, "r") as file:
                self.text.delete("1.0", tk.END)
                self.text.insert(tk.END, file.read())
    
    def save_file(self):
        text = self.text.get("1.0", tk.END)
        if not text:
            messagebox.showerror("Error", "No text to save")
            return
        file_path = filedialog.asksaveasfilename(filetypes=[("Markdown files", "*.md")])
        if file_path:
            with open(file_path, "w") as file:
                file.write(text)
    
    def save_as_file(self):
        text = self.text.get("1.0", tk.END)
        if not text:
            messagebox.showerror("Error", "No text to save")
            return
        file_path = filedialog.asksaveasfilename(filetypes=[("Markdown files", "*.md")])
        if file_path:
            with open(file_path, "w") as file:
                file.write(text)
    
    def exit(self):
        self.root.destroy()
    
    def spell_check(self):
        text = self.text.get("1.0", tk.END)
        data = {"text": text}
        response = requests.post("http://