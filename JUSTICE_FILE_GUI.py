"""Justice File AI Control Panel GUI.

Features:
 - Task selection (A: Summaries, B: Contradictions, C: Evidence Brief)
 - Child selector
 - Evidence folder picker
 - Run Selected / Run All (A,B,C)
 - Dry Run toggle (no API calls; placeholder outputs)
 - Open Outputs / PDFs / Master Excel buttons
 - Live streaming log window

Usage:
 python JUSTICE_FILE_GUI.py
"""
from __future__ import annotations
import subprocess
import threading
import queue
import os
import sys
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox

PIPELINE_SCRIPT = "MASTER_PIPELINE_GPT5.py"
DEFAULT_CHILDREN = "Jace,Josh"
DEFAULT_INPUT = "evidence"  # user can change
OUTPUT_DIR = "pipeline/outputs"
PDF_DIR = "legal_export/pdf"
MASTER_EXCEL = "MASTER_JUSTICE_FILE_SUPREME_v1.xlsx"

class PipelineRunner(threading.Thread):
    def __init__(self, cmd, log_q: queue.Queue):
        super().__init__(daemon=True)
        self.cmd = cmd
        self.log_q = log_q
        self.process = None

    def run(self):
        try:
            self.log_q.put(f"[RUN] {' '.join(self.cmd)}\n")
            self.process = subprocess.Popen(self.cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            for line in self.process.stdout:  # type: ignore
                self.log_q.put(line)
            self.process.wait()
            rc = self.process.returncode
            self.log_q.put(f"\n[EXIT] Return code: {rc}\n")
        except Exception as e:
            self.log_q.put(f"[ERROR] {e}\n")

class JusticeGUI:
    def __init__(self, root: tk.Tk):
        self.root = root
        root.title("Justice File AI Control Panel")
        self.log_q: queue.Queue[str] = queue.Queue()

        # Task frame
        tasks_frame = tk.LabelFrame(root, text="Tasks")
        tasks_frame.grid(row=0, column=0, sticky="ew", padx=8, pady=4)
        self.var_A = tk.BooleanVar(value=True)
        self.var_B = tk.BooleanVar(value=True)
        self.var_C = tk.BooleanVar(value=True)
        tk.Checkbutton(tasks_frame, text="A (Summaries)", variable=self.var_A).grid(row=0, column=0, sticky="w")
        tk.Checkbutton(tasks_frame, text="B (Contradictions)", variable=self.var_B).grid(row=0, column=1, sticky="w")
        tk.Checkbutton(tasks_frame, text="C (Brief)", variable=self.var_C).grid(row=0, column=2, sticky="w")

        # Children
        tk.Label(root, text="Children (comma separated):").grid(row=1, column=0, sticky="w", padx=8)
        self.children_entry = tk.Entry(root, width=40)
        self.children_entry.insert(0, DEFAULT_CHILDREN)
        self.children_entry.grid(row=2, column=0, sticky="w", padx=8)

        # Input folder picker
        folder_frame = tk.Frame(root)
        folder_frame.grid(row=3, column=0, sticky="ew", padx=8, pady=(4,2))
        tk.Label(folder_frame, text="Evidence Folder:").grid(row=0, column=0, sticky="w")
        self.input_var = tk.StringVar(value=DEFAULT_INPUT)
        self.input_entry = tk.Entry(folder_frame, textvariable=self.input_var, width=40)
        self.input_entry.grid(row=0, column=1, sticky="w")
        tk.Button(folder_frame, text="Browse", command=self.pick_folder).grid(row=0, column=2, padx=4)

        # Dry run toggle
        self.dry_run_var = tk.BooleanVar(value=False)
        tk.Checkbutton(root, text="Dry Run (no API calls)", variable=self.dry_run_var).grid(row=4, column=0, sticky="w", padx=8)

        # Run buttons
        run_frame = tk.Frame(root)
        run_frame.grid(row=5, column=0, sticky="ew", padx=8, pady=4)
        tk.Button(run_frame, text="Run Selected", command=self.run_selected).grid(row=0, column=0, padx=4)
        tk.Button(run_frame, text="Run All (A,B,C)", command=self.run_all).grid(row=0, column=1, padx=4)

        # Open buttons
        open_frame = tk.Frame(root)
        open_frame.grid(row=6, column=0, sticky="ew", padx=8, pady=4)
        tk.Button(open_frame, text="Open Outputs", command=lambda: self.open_path(OUTPUT_DIR)).grid(row=0, column=0, padx=2)
        tk.Button(open_frame, text="Open PDFs", command=lambda: self.open_path(PDF_DIR)).grid(row=0, column=1, padx=2)
        tk.Button(open_frame, text="Open Master Excel", command=lambda: self.open_path(MASTER_EXCEL)).grid(row=0, column=2, padx=2)

        # Log box
        log_frame = tk.LabelFrame(root, text="Pipeline Log")
        log_frame.grid(row=7, column=0, sticky="nsew", padx=8, pady=4)
        self.text = tk.Text(log_frame, height=22, width=100, state="disabled", wrap="word", background="#111", foreground="#0f0")
        self.text.pack(fill="both", expand=True)

        # Configure resizing
        root.grid_rowconfigure(7, weight=1)
        root.grid_columnconfigure(0, weight=1)

        # Poll log queue
        self.root.after(150, self.drain_log)
        self.runner: PipelineRunner | None = None

    def pick_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.input_var.set(folder)

    def tasks_selected(self) -> str:
        selected = []
        if self.var_A.get(): selected.append('A')
        if self.var_B.get(): selected.append('B')
        if self.var_C.get(): selected.append('C')
        return ','.join(selected)

    def run_all(self):
        self.var_A.set(True); self.var_B.set(True); self.var_C.set(True)
        self.run_selected()

    def run_selected(self):
        if self.runner and self.runner.is_alive():
            messagebox.showwarning("Busy", "Pipeline is already running.")
            return
        tasks = self.tasks_selected()
        if not tasks:
            messagebox.showinfo("No Tasks", "Select at least one task (A,B,C).")
            return
        input_dir = Path(self.input_var.get())
        if not input_dir.exists():
            messagebox.showerror("Input Missing", f"Input folder does not exist: {input_dir}")
            return
        children = self.children_entry.get().strip() or DEFAULT_CHILDREN
        cmd = [sys.executable, PIPELINE_SCRIPT, "--input", str(input_dir), "--tasks", tasks, "--children", children, "--out", OUTPUT_DIR]
        if self.dry_run_var.get():
            cmd.append("--dry-run")
        # Ensure output dir exists for user convenience
        Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)
        self.append_log(f"Starting pipeline (tasks {tasks})...\n")
        self.runner = PipelineRunner(cmd, self.log_q)
        self.runner.start()

    def append_log(self, text: str):
        self.text.configure(state="normal")
        self.text.insert("end", text)
        self.text.see("end")
        self.text.configure(state="disabled")

    def drain_log(self):
        try:
            while True:
                line = self.log_q.get_nowait()
                self.append_log(line)
        except queue.Empty:
            pass
        self.root.after(150, self.drain_log)

    def open_path(self, target: str):
        p = Path(target)
        if not p.exists():
            messagebox.showinfo("Missing", f"Path does not exist yet: {p}")
            return
        try:
            if os.name == 'nt':
                os.startfile(str(p))  # type: ignore[attr-defined]
            elif sys.platform == 'darwin':
                subprocess.Popen(['open', str(p)])
            else:
                subprocess.Popen(['xdg-open', str(p)])
        except Exception as e:
            messagebox.showerror("Open Failed", str(e))


def main():
    root = tk.Tk()
    app = JusticeGUI(root)
    root.minsize(780, 600)
    root.mainloop()

if __name__ == "__main__":
    main()
