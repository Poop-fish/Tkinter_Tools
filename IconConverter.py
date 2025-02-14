from CustomStyle import SimpleStyle 
from imports import ( tk, ttk,filedialog, messagebox, Image, ImageTk , os )

class ICOConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ICO Converter")
        self.root.geometry("720x620")
        self.root.configure(bg="black")
        self.root.iconbitmap("Assets/FaceLogo.ico")
        self.original_image = None
        self.last_selected_size = None
        self.create_widgets()
        self.setup_bindings()
        SimpleStyle(root)

    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding=15)
        main_frame.pack(fill=tk.BOTH, expand=True)
        #! ----
        self.preview_frame = ttk.LabelFrame(main_frame, text=" Live Preview ", padding=10)
        self.preview_frame.pack(fill=tk.BOTH, pady=5, expand=True)
        #! ----
        self.preview_canvas = tk.Canvas(self.preview_frame, width=256, height=256, bg='#444444')
        self.preview_canvas.pack()
        self.preview_canvas.create_text(128, 128, text="Select an image to begin", 
                                       fill="#cccccc", font=('Arial', 12))
        #! ----
        file_frame = ttk.Frame(main_frame)
        file_frame.pack(fill=tk.X, pady=5)
        #! ----
        self.file_path = tk.StringVar()
        ttk.Entry(file_frame, textvariable=self.file_path, width=40, state='readonly').pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Button(file_frame, text="Browse PNG", command=self.load_image).pack(side=tk.RIGHT)
        #! ----
        size_frame = ttk.LabelFrame(main_frame, text=" Icon Sizes ", padding=10)
        size_frame.pack(fill=tk.X, pady=5)
        #! ----
        self.size_vars = {
            (16, 16): tk.BooleanVar(),
            (32, 32): tk.BooleanVar(),
            (48, 48): tk.BooleanVar(),
            (64, 64): tk.BooleanVar(),
            (128, 128): tk.BooleanVar(),
            (256, 256): tk.BooleanVar()
        }
        
        for i, (size, var) in enumerate(self.size_vars.items()):
            cb = tk.Checkbutton(size_frame, text=f"{size[0]}x{size[1]}", variable=var,
                                command=lambda s=size: self.update_size_preview(s), bg="#555555")
            cb.grid(row=i//3, column=i%3, sticky=tk.W, padx=5, pady=2)

        #! ----
        opt_frame = ttk.Frame(main_frame)
        opt_frame.pack(fill=tk.X, pady=5)
        #! ----
        self.keep_aspect = tk.BooleanVar(value=True)
        tk.Checkbutton(opt_frame, text="Maintain Aspect Ratio", variable=self.keep_aspect,
                       command=self.update_preview, bg="#555555").pack(side=tk.LEFT, padx=10)
        #! ----
        self.keep_alpha = tk.BooleanVar(value=True)
        tk.Checkbutton(opt_frame, text="Preserve Transparency", variable=self.keep_alpha,
                       command=self.update_preview, bg="#555555").pack(side=tk.LEFT, padx=10)
        #! ----
        self.convert_btn = ttk.Button(main_frame, text="Convert to ICO", 
                                     command=self.convert_image, state=tk.DISABLED)
        self.convert_btn.pack(pady=10)
        #! ----
        self.status = ttk.Label(self.root, text="Ready", anchor=tk.W)
        self.status.pack(fill=tk.X)
        #! ----
    def setup_bindings(self):
        self.root.bind("<Configure>", self.handle_resize)

    def handle_resize(self, event):
        if self.original_image:
            self.update_preview()

    def load_image(self):
        filetypes = [("PNG Files", "*.png"), ("All Files", "*.*")]
        filename = filedialog.askopenfilename(title="Select Image", filetypes=filetypes)
        if filename:
            try:
                self.original_image = Image.open(filename)
                self.file_path.set(filename)
                self.convert_btn.config(state=tk.NORMAL)
                self.update_preview()
                self.status.config(text=f"Loaded: {os.path.basename(filename)}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load image:\n{str(e)}")

    def update_size_preview(self, size):
        self.last_selected_size = size
        self.update_preview()

    def update_preview(self):
        if not self.original_image:
            return

        selected_sizes = [s for s, var in self.size_vars.items() if var.get()]
        if not selected_sizes:
            self.preview_canvas.delete("all")
            self.preview_canvas.create_text(128, 128, text="No sizes selected", 
                                          fill="#cccccc", font=('Arial', 12))
            return

        preview_size = self.last_selected_size if self.last_selected_size else max(selected_sizes)
        width, height = preview_size

        try:
            img = self.original_image.copy()
            if self.keep_alpha.get() and img.mode != 'RGBA':
                img = img.convert('RGBA')

            if self.keep_aspect.get():
                img.thumbnail((width, height), Image.Resampling.LANCZOS)
                bg = Image.new('RGBA', (width, height), (255, 255, 255, 0))
                bg.paste(img, ((width - img.width)//2, (height - img.height)//2))
                img = bg
            else:
                img = img.resize((width, height), Image.Resampling.LANCZOS)

            img.thumbnail((256, 256), Image.Resampling.LANCZOS)
            self.preview_image = ImageTk.PhotoImage(img)
            self.preview_canvas.delete("all")
            self.preview_canvas.create_image(128, 128, image=self.preview_image)
            self.preview_canvas.create_text(5, 5, text=f"Preview: {width}x{height}", 
                                          anchor=tk.NW, fill="black" )

        except Exception as e:
            messagebox.showerror("Oh No A Preview Error :(", f"Could not generate preview:\n{str(e)}")

    def convert_image(self):
        try:
            selected_sizes = [s for s, var in self.size_vars.items() if var.get()]
            if not selected_sizes:
                messagebox.showwarning("No Size Selected", "Please select at least one icon size")
                return

            output_path = filedialog.asksaveasfilename(
                defaultextension=".ico",
                filetypes=[("ICO Files", "*.ico")],
                title="Save ICO File"
            )
            if not output_path:
                return

            images = []
            for width, height in selected_sizes:
                img = self.original_image.copy()
                if self.keep_alpha.get() and img.mode != 'RGBA':
                    img = img.convert('RGBA')

                if self.keep_aspect.get():
                    img.thumbnail((width, height), Image.Resampling.LANCZOS)
                    bg = Image.new('RGBA', (width, height), (255, 255, 255, 0))
                    bg.paste(img, ((width - img.width)//2, (height - img.height)//2))
                    img = bg
                else:
                    img = img.resize((width, height), Image.Resampling.LANCZOS)
                images.append(img)

            images[0].save(
                output_path,
                format="ICO",
                append_images=images[1:],
                quality=100,
                bitmap_format="bmp"
            )

            messagebox.showinfo("Success", "ICO file created successfully!")
            self.status.config(text=f"Saved: {os.path.basename(output_path)}")

        except Exception as e:
            messagebox.showerror("Error", f"Conversion failed:\n{str(e)}")
            self.status.config(text="Error occurred during conversion")
#! ------ Run App ------
def RunApp():
    
    root = tk.Tk()
    
    app = ICOConverterApp(root)
    
    root.mainloop()

if __name__ == "__main__":
    RunApp()