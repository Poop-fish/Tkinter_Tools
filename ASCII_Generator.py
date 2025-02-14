from CustomStyle import SimpleStyle 
from imports import ( tk, ttk, Image,filedialog, messagebox, np, pyfiglet, pyperclip )

class ASCIIConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ASCII Generator")
        self.root.geometry("900x800")
        self.root.configure(bg="black")
        self.root.iconbitmap("Assets/FaceLogo.ico")
        SimpleStyle(root)
        self._build_ui()

    def _build_ui(self):
        self.main_frame = ttk.Frame(self.root, style='Main.TFrame')
        self.main_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        self.control_frame = ttk.LabelFrame(self.main_frame, text="Controls", padding=10)
        self.control_frame.pack(fill=tk.X, padx=5, pady=5)

        self.btn_open = ttk.Button(
            self.control_frame, text="Open Image", command=self.open_image, style='Button.TButton'
        )
        self.btn_open.pack(side=tk.LEFT, padx=5)

        self.btn_style = ttk.Button(
            self.control_frame, text="Frame Text", command=self.stylize_text, style='Button.TButton'
        )
        self.btn_style.pack(side=tk.LEFT, padx=5)

        self.btn_ascii_text = ttk.Button(
            self.control_frame, text="Text to ASCII", command=self.text_to_ascii, style='Button.TButton'
        )
        self.btn_ascii_text.pack(side=tk.RIGHT, padx=5)

        self.font_var = tk.StringVar()
        self.fonts = pyfiglet.FigletFont.getFonts()
        self.font_var.set(self.fonts[0])  
        self.font_menu = ttk.Combobox(
            self.control_frame, textvariable=self.font_var, values=self.fonts, state="readonly"
        )
        self.font_menu.pack(side=tk.LEFT, padx=5)

        self.font_size_var = tk.IntVar(value=8)  # Default font size
        self.font_size_label = ttk.Label(self.control_frame, text="Font Size:", style='Label.TLabel')
        self.font_size_label.pack(side=tk.LEFT, padx=5)
        self.font_size_spinbox = ttk.Spinbox(
            self.control_frame, from_=6, to=20, textvariable=self.font_size_var, width=5
        )
        self.font_size_spinbox.pack(side=tk.LEFT, padx=5)

        self.btn_copy = ttk.Button(
            self.control_frame, text="Copy to Clipboard", command=self.copy_to_clipboard, style='Button.TButton'
        )
        self.btn_copy.pack(side=tk.RIGHT, padx=5)

        self.text_frame = ttk.LabelFrame(self.main_frame, text="ASCII Output", padding=10)
        self.text_frame.pack(expand=True, fill=tk.BOTH, padx=5, pady=5)

        self.text_box = tk.Text(
            self.text_frame, wrap=tk.WORD, font=("Courier", self.font_size_var.get()), bg="white", fg="black"
        )
        self.text_box.pack(expand=True, fill=tk.BOTH)

        self.scrollbar = ttk.Scrollbar(self.text_box, orient=tk.VERTICAL, command=self.text_box.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_box.config(yscrollcommand=self.scrollbar.set)

        self.font_size_var.trace_add("write", self.update_font_size)

    def update_font_size(self, *args):
        self.text_box.config(font=("Courier", self.font_size_var.get()))

    def image_to_ascii(self, image_path, width=100):
        chars = "@%#*+=-:. "
        try:
            img = Image.open(image_path)
            aspect_ratio = img.height / img.width
            new_height = int(width * aspect_ratio * 0.55)
            img = img.resize((width, new_height)).convert('L')
            pixels = np.array(img)
            ascii_art = "\n".join("".join(chars[pixel // 32] for pixel in row) for row in pixels)
            return ascii_art
        except Exception as e:
            messagebox.showerror("Error", f"Failed to process image: {e}")
            return None

    def add_border(self, text):
        lines = text.split("\n")
        width = max(len(line) for line in lines)
        border = "#" * (width + 4)
        framed_text = [border] + [f"# {line.ljust(width)} #" for line in lines] + [border]
        return "\n".join(framed_text)

    def text_to_ascii(self):
        """Convert text to ASCII art using the selected font."""
        user_text = self.text_box.get(1.0, tk.END).strip()
        selected_font = self.font_var.get()
        if user_text:
            try:
                ascii_text = pyfiglet.figlet_format(user_text, font=selected_font)
                self.text_box.delete(1.0, tk.END)
                self.text_box.insert(tk.END, ascii_text)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to generate ASCII text: {e}")

    def open_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if file_path:
            ascii_result = self.image_to_ascii(file_path)
            if ascii_result:
                framed_result = self.add_border(ascii_result)
                self.text_box.delete(1.0, tk.END)
                self.text_box.insert(tk.END, framed_result)

    def stylize_text(self):
        text = self.text_box.get(1.0, tk.END).strip()
        if text:
            styled_text = self.add_border(text)
            self.text_box.delete(1.0, tk.END)
            self.text_box.insert(tk.END, styled_text)

    def copy_to_clipboard(self):
        text = self.text_box.get(1.0, tk.END).strip()
        if text:
            pyperclip.copy(text)
            messagebox.showinfo("Success", "Text copied to clipboard!")
        else:
            messagebox.showwarning("Warning", "No text to copy.")

#! ------ Run App ------
def RunApp():

    root = tk.Tk()
    
    app = ASCIIConverterApp(root)
    
    root.mainloop() 

if __name__ == "__main__":
    RunApp()


    