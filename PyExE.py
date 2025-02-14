from CustomStyle import SimpleStyle 
from imports import ( tk, ttk, filedialog, messagebox , scrolledtext, np, pyfiglet, pyperclip, subprocess, os, threading, queue )

class PyToExeConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Python to EXE Converter")
        self.root.geometry("800x800")
        self.root.configure(bg="black")
        self.root.iconbitmap("Assets/FaceLogo.ico")
        SimpleStyle(root)
        self.output_queue = queue.Queue()
        
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.convert_btn = None
        self.create_file_selection()
        self.create_options_frame()
        self.create_console_output()
        self.create_action_buttons()
        self.root.after(100, self.process_queue)

    def create_file_selection(self):
        file_frame = ttk.LabelFrame(self.main_frame, text=" Python File Selection ")
        file_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.file_path = tk.StringVar()
        
        ttk.Label(file_frame, text="Select Python File:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        
        self.file_entry = ttk.Entry(file_frame, textvariable=self.file_path, width=50)
        self.file_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.EW)
        
        browse_btn = ttk.Button(file_frame, text="Browse", command=self.browse_file)
        browse_btn.grid(row=0, column=2, padx=5, pady=5)

    def create_options_frame(self):
        options_frame = ttk.LabelFrame(self.main_frame, text=" Conversion Options ")
        options_frame.pack(fill=tk.X, padx=5, pady=5)
        options_frame.grid_columnconfigure(1, weight=1)
        
        self.onefile_var = tk.BooleanVar(value=True)
        tk.Checkbutton(options_frame, text="Create Single File (--onefile)", 
                        variable=self.onefile_var, bg="#555555").grid(row=0, column=0, padx=5, pady=2, sticky=tk.W)
        
        self.console_var = tk.BooleanVar(value=True)
        tk.Checkbutton(options_frame, text="Show Console Window (--console)", 
                        variable=self.console_var, bg="#555555").grid(row=0, column=1, padx=5, pady=2, sticky=tk.W)
        
        self.icon_path = tk.StringVar()
        ttk.Label(options_frame, text="Application Icon:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        icon_entry = ttk.Entry(options_frame, textvariable=self.icon_path, width=50)
        icon_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.EW)
        ttk.Button(options_frame, text="Browse", command=self.browse_icon).grid(row=1, column=2, padx=5, pady=5)
        
        ttk.Label(options_frame, text="Additional Arguments:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.additional_args = ttk.Entry(options_frame, width=50)
        self.additional_args.grid(row=2, column=1, columnspan=2, padx=5, pady=5, sticky=tk.EW)

    def create_console_output(self):
        console_frame = ttk.LabelFrame(self.main_frame, text=" Conversion Output ")
        console_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.console = scrolledtext.ScrolledText(console_frame, wrap=tk.WORD, state='disabled')
        self.console.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def create_action_buttons(self):
        btn_frame = ttk.Frame(self.main_frame)
        btn_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.convert_btn = ttk.Button(btn_frame, text="Convert to EXE", command=self.start_conversion)
        self.convert_btn.pack(side=tk.LEFT, padx=5, pady=5)
        
        exit_btn = ttk.Button(btn_frame, text="Exit", command=self.root.quit)
        exit_btn.pack(side=tk.RIGHT, padx=5, pady=5)

    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Python Files", "*.py")])
        if file_path:
            self.file_path.set(file_path)

    def browse_icon(self):
        icon_path = filedialog.askopenfilename(filetypes=[("Icon Files", "*.ico")])
        if icon_path:
            self.icon_path.set(icon_path)

    def start_conversion(self):
        if not os.path.isfile(self.file_path.get()):
            messagebox.showerror("Error", "Please select a valid Python file!")
            return
        
        self.convert_btn.config(state='disabled')
        threading.Thread(target=self.run_conversion, daemon=True).start()

    def run_conversion(self):
        cmd = [
            'pyinstaller',
            '--noconfirm',
            '--onefile' if self.onefile_var.get() else '',
            '--console' if self.console_var.get() else '--noconsole',
            self.file_path.get()
        ]
        
        if self.icon_path.get():
            cmd.extend(['--icon', self.icon_path.get()])
        
        cmd += self.additional_args.get().split()
        cmd = [arg for arg in cmd if arg]
        
        try:
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True
            )
            
            for line in process.stdout:
                self.output_queue.put(line)
                
            process.wait()
            self.output_queue.put("\nConversion completed!\n")
            
        except Exception as e:
            self.output_queue.put(f"Error: {str(e)}\n")
        finally:
            self.root.after(0, lambda: self.convert_btn.config(state='normal'))

    def process_queue(self):
        while not self.output_queue.empty():
            line = self.output_queue.get()
            self.console.config(state='normal')
            self.console.insert(tk.END, line)
            self.console.see(tk.END)
            self.console.config(state='disabled')
        self.root.after(100, self.process_queue)

#! ------ Run App ------
def RunApp():
    
    root = tk.Tk()
    
    app = PyToExeConverterApp(root)
    
    root.mainloop() 

if __name__ == "__main__":
    RunApp()