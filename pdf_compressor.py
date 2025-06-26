import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import subprocess
import os
import sys
import threading

# --- Core Application Class ---
class PDFCompressorApp:
    """
    A desktop application for compressing PDF files using Ghostscript.
    The user can select a PDF, choose a compression level, and save the
    compressed file.
    """
    def __init__(self, root):
        """
        Initializes the main application window and its widgets.
        """
        self.root = root
        self.root.title("PDF Compressor")
        self.root.geometry("550x350")
        self.root.resizable(False, False)
        
        # Style configuration
        self.style = ttk.Style(self.root)
        self.style.theme_use('clam') # A clean, modern theme

        # --- Member Variables ---
        self.input_pdf_path = tk.StringVar()
        self.output_pdf_path = tk.StringVar()
        self.compression_level = tk.StringVar(value='ebook') # Default compression level
        self.ghostscript_path = self.find_ghostscript()

        # --- UI Setup ---
        self.create_widgets()

        # Check for Ghostscript installation on startup
        if not self.ghostscript_path:
            self.show_ghostscript_warning()

    def find_ghostscript(self):
        """
        Attempts to find the Ghostscript executable on Windows.
        Checks common installation directories and the system PATH.
        """
        # Common names for the Ghostscript command-line executable
        gs_names = ['gswin64c.exe', 'gswin32c.exe', 'gs.exe']
        
        # Check if it's in the system PATH
        for name in gs_names:
            if sys.platform == 'win32':
                try:
                    # Use 'where' command on Windows to find the executable
                    path = subprocess.check_output(['where', name]).strip().decode()
                    if os.path.exists(path):
                        return path
                except (subprocess.CalledProcessError, FileNotFoundError):
                    continue

        # Check common installation directories
        program_files = os.environ.get('ProgramFiles', 'C:\\Program Files')
        gs_dirs = [os.path.join(program_files, 'gs')]
        for gs_dir in gs_dirs:
            if os.path.isdir(gs_dir):
                for root, _, files in os.walk(gs_dir):
                    for name in gs_names:
                        if name in files:
                            return os.path.join(root, name)
        return None

    def show_ghostscript_warning(self):
        """
        Displays a warning message if Ghostscript is not found and provides a link.
        """
        messagebox.showwarning(
            "Ghostscript Not Found",
            "Ghostscript is required for PDF compression but could not be found.\n\n"
            "Please install Ghostscript and ensure it's added to your system's PATH.\n\n"
            "You can download it from: ghostscript.com/releases"
        )

    def create_widgets(self):
        """
        Creates and arranges all the UI elements in the main window.
        """
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(expand=True, fill=tk.BOTH)

        # --- Input File Selection ---
        input_frame = ttk.LabelFrame(main_frame, text="1. Select PDF File", padding="10")
        input_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Entry(input_frame, textvariable=self.input_pdf_path, state='readonly', width=50).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 10))
        ttk.Button(input_frame, text="Browse...", command=self.select_input_file).pack(side=tk.LEFT)

        # --- Compression Level Selection ---
        compression_frame = ttk.LabelFrame(main_frame, text="2. Choose Compression Level", padding="10")
        compression_frame.pack(fill=tk.X, pady=10)

        # Descriptions for each level
        levels = {
            "screen": "Low Quality (72 dpi) - Max Compression",
            "ebook": "Medium Quality (150 dpi) - Good for screen reading",
            "printer": "High Quality (300 dpi) - Good for printing",
            "prepress": "Best Quality (300 dpi, preserves color) - Minimal Compression"
        }
        
        for value, text in levels.items():
            ttk.Radiobutton(
                compression_frame,
                text=text,
                variable=self.compression_level,
                value=value
            ).pack(anchor=tk.W, pady=2)

        # --- Action Button & Status ---
        action_frame = ttk.Frame(main_frame, padding="10 0 0 0")
        action_frame.pack(fill=tk.X, pady=10)

        self.compress_button = ttk.Button(action_frame, text="Compress PDF", command=self.start_compression_thread)
        self.compress_button.pack(pady=10)
        
        self.progress = ttk.Progressbar(action_frame, orient=tk.HORIZONTAL, length=300, mode='indeterminate')
        self.status_label = ttk.Label(action_frame, text="Ready. Select a file to begin.")
        
        self.progress.pack_forget() # Hide until needed
        self.status_label.pack(pady=5)

    def select_input_file(self):
        """
        Opens a file dialog to select the input PDF file.
        """
        filepath = filedialog.askopenfilename(
            title="Select a PDF file",
            filetypes=[("PDF Files", "*.pdf")]
        )
        if filepath:
            self.input_pdf_path.set(filepath)
            self.status_label.config(text=f"Selected: {os.path.basename(filepath)}")

    def start_compression_thread(self):
        """
        Starts the compression process in a separate thread to keep the UI responsive.
        """
        # Validate inputs before starting
        if not self.input_pdf_path.get():
            messagebox.showerror("Error", "Please select an input PDF file first.")
            return
        
        if not self.ghostscript_path:
            self.show_ghostscript_warning()
            return

        # Ask for save location
        output_path = filedialog.asksaveasfilename(
            title="Save Compressed PDF As...",
            filetypes=[("PDF Files", "*.pdf")],
            defaultextension=".pdf",
            initialfile=f"{os.path.splitext(os.path.basename(self.input_pdf_path.get()))[0]}_compressed.pdf"
        )

        if not output_path:
            self.status_label.config(text="Save cancelled. Ready.")
            return

        self.output_pdf_path.set(output_path)
        
        # Disable button and show progress bar
        self.compress_button.config(state=tk.DISABLED)
        self.status_label.config(text="Compressing... Please wait.")
        self.progress.pack(pady=5)
        self.progress.start()
        
        # Run compression in a background thread
        compression_thread = threading.Thread(
            target=self.run_compression,
            daemon=True
        )
        compression_thread.start()

    def run_compression(self):
        """
        Executes the Ghostscript command to perform the PDF compression.
        This method is designed to be run in a background thread.
        """
        input_file = self.input_pdf_path.get()
        output_file = self.output_pdf_path.get()
        level = self.compression_level.get()

        # Ghostscript command arguments
        command = [
            self.ghostscript_path,
            '-sDEVICE=pdfwrite',
            '-dCompatibilityLevel=1.4',
            f'-dPDFSETTINGS=/{level}',
            '-dNOPAUSE',
            '-dQUIET',
            '-dBATCH',
            f'-sOutputFile={output_file}',
            input_file
        ]

        try:
            # Using PIPE for stdout/stderr to keep the console clean
            process = subprocess.run(
                command,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0
            )
            
            # After successful compression, update UI from the main thread
            self.root.after(0, self.on_compression_success)

        except subprocess.CalledProcessError as e:
            error_message = f"Ghostscript Error:\n{e.stderr.decode('utf-8', 'ignore')}"
            self.root.after(0, self.on_compression_error, error_message)
        except Exception as e:
            self.root.after(0, self.on_compression_error, str(e))

    def on_compression_success(self):
        """
        Callback function to update the UI after successful compression.
        """
        self.progress.stop()
        self.progress.pack_forget()
        self.compress_button.config(state=tk.NORMAL)
        self.status_label.config(text="Compression successful!")
        
        original_size = os.path.getsize(self.input_pdf_path.get()) / (1024 * 1024)
        compressed_size = os.path.getsize(self.output_pdf_path.get()) / (1024 * 1024)
        reduction = 100 - (compressed_size / original_size * 100)
        
        messagebox.showinfo(
            "Success",
            f"PDF compressed successfully!\n\n"
            f"Original Size: {original_size:.2f} MB\n"
            f"Compressed Size: {compressed_size:.2f} MB\n"
            f"Reduction: {reduction:.1f}%"
        )
        self.status_label.config(text="Ready.")

    def on_compression_error(self, error_message):
        """
        Callback function to update the UI after a compression error.
        """
        self.progress.stop()
        self.progress.pack_forget()
        self.compress_button.config(state=tk.NORMAL)
        self.status_label.config(text="An error occurred.")
        messagebox.showerror("Compression Failed", f"An error occurred during compression:\n\n{error_message}")


# --- Main Execution ---
if __name__ == "__main__":
    root = tk.Tk()
    app = PDFCompressorApp(root)
    root.mainloop()
