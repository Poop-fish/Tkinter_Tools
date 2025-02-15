from CustomStyle import SimpleStyle 
from imports import ( tk, ttk, Image,filedialog, messagebox,subprocess, sys, os, json, datetime, colorsys, ImageTk )


class BugReporterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Bug Reporter")
        self.root.geometry("1200x800")
        self.root.iconbitmap("Assets/BugLogo.ico")
        self.root.configure(bg="black")
        self.hue = 0.0  
        self.bug_reports = []
        self.load_reports()
        SimpleStyle(root)
        self.create_sidebar()
        self.create_main_content()
        self.start_color_cycle()

    def hsv_to_rgb(self, h, s, v):
        r, g, b = colorsys.hsv_to_rgb(h, s, v)
        return int(r * 255), int(g * 255), int(b * 255)

    def start_color_cycle(self):
        self.cycle_background()

    def cycle_background(self):
        r, g, b = self.hsv_to_rgb(self.hue, 0.7, 0.2)
        hex_color = f"#{r:02x}{g:02x}{b:02x}"
        self.root.configure(bg=hex_color)
        self.hue += 0.002
        if self.hue >= 1.0:
            self.hue = 0.0
        self.root.after(50, self.cycle_background)
    
    def create_sidebar(self):
        sidebar = ttk.Frame(self.root, width=200 , relief="ridge",borderwidth=12)
        sidebar.pack(side=tk.LEFT, fill=tk.Y)
        
        logo = ttk.Label(sidebar, text="Bug Reporter", font=('Arial', 12, 'bold'))
        logo.pack(pady=20, padx=10)
        
        nav_buttons = [
            ("Report Bug", self.show_report_form),
            ("View Reports", self.show_bug_list),
            # ("Settings", lambda: self.show_placeholder("Settings"))
        ]
        
        for text, command in nav_buttons:
            btn = ttk.Button(sidebar, text=text, command=command)
            btn.pack(pady=5, fill=tk.X)
        

        submit_btn = ttk.Button(sidebar, text="Submit Bug Report", command=self.submit_bug)
        submit_btn.pack(pady=5, fill=tk.X)
    
    def create_main_content(self):
        main_frame = ttk.Frame(self.root, relief="ridge",borderwidth=12)
        main_frame.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH, padx=10, pady=10)
        
        self.form_frame = ttk.Frame(main_frame)
        self.create_report_form(self.form_frame)
        
        self.list_frame = ttk.Frame(main_frame)
        self.create_bug_list(self.list_frame)
        
        self.show_report_form()
    
    def create_report_form(self, parent):
        row = 0
        
        ttk.Label(parent, text="Bug Title:", font=('Arial', 12, 'bold')).grid(row=row, column=0, sticky=tk.E, pady=2)
        self.title_entry = ttk.Entry(parent, width=60)
        self.title_entry.grid(row=row, column=1, columnspan=5, sticky=tk.W, pady=2)  # Adjusted columnspan
        row += 1
        
        ttk.Label(parent, text="Description:", font=('Arial', 12, 'bold')).grid(row=row, column=0, sticky=tk.NE, pady=2)
        self.desc_text = tk.Text(parent, width=90, height=20, bg='#4d4d4d', fg='white')
        self.desc_text.grid(row=row, column=1, columnspan=5, sticky=tk.W, pady=2)  # Adjusted columnspan
        row += 1
        
        ttk.Label(parent, text="Reproduction Steps:", font=('Arial', 12, 'bold')).grid(row=row, column=0, sticky=tk.NW, pady=2)
        self.steps_text = tk.Text(parent, width=90, height=10, bg='#4d4d4d', fg='white')
        self.steps_text.grid(row=row, column=1, columnspan=5, sticky=tk.W, pady=2)  # Adjusted columnspan
        row += 1

        self.upload_frame = ttk.LabelFrame(parent, text="Upload Buttons", padding=10)
        self.upload_frame.place(x=425 , y=600)
     
        self.Section_frame = ttk.LabelFrame(parent, text="Upload Buttons", padding=10)
        self.Section_frame.place(x=425 , y=600)
            
        self.severity_frame = ttk.LabelFrame(parent, text="Report Settings", padding=10)
        self.severity_frame.grid(row=row, column=1, sticky="nsew", padx=5, pady=5)
        
        ttk.Label(self.severity_frame, text="Severity:").grid(row=0, column=0, sticky=tk.E, pady=2)
        self.severity_combo = ttk.Combobox(self.severity_frame, values=["Low", "Medium", "High"], state="readonly")
        self.severity_combo.grid(row=0, column=1, sticky=tk.W, pady=2)
        
        ttk.Label(self.severity_frame, text="Game Version:").grid(row=0, column=2, sticky=tk.E, pady=2)
        self.version_entry = ttk.Entry(self.severity_frame, width=20)
        self.version_entry.grid(row=0, column=3, sticky=tk.W, pady=2)

        ttk.Label(self.severity_frame, text="Platform:").grid(row=0, column=4, sticky=tk.E, pady=2)
        self.platform_combo = ttk.Combobox(self.severity_frame, values=["Windows", "Mac", "PlayStation", "Xbox","Linux"], state="readonly")
        self.platform_combo.grid(row=0, column=5, sticky=tk.W, pady=2)
        row += 1
        self.screenshot_btn = ttk.Button(self.upload_frame, text="Upload Screenshot", command=self.upload_screenshot)
        self.screenshot_btn.grid(row=1, column=0, padx=5, pady=2)
        
        self.video_btn = ttk.Button(self.upload_frame, text="Upload Video", command=self.upload_video)
        self.video_btn.grid(row=0, column=0, padx=5, pady=2)
        
        self.progress = ttk.Progressbar(parent, orient=tk.HORIZONTAL, length=100, mode='determinate')
        row += 1

    def create_bug_list(self, parent):
        filter_frame = ttk.Frame(parent)
        filter_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(filter_frame, text="Search:").pack(side=tk.LEFT)
        self.search_entry = ttk.Entry(filter_frame, width=30)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        self.search_entry.bind('<KeyRelease>', self.filter_bugs)
        
        ttk.Label(filter_frame, text="Status:").pack(side=tk.LEFT, padx=10)
        self.status_filter = ttk.Combobox(filter_frame, values=["All", "Open", "Closed"], state="readonly")
        self.status_filter.pack(side=tk.LEFT)
        self.status_filter.bind('<<ComboboxSelected>>', self.filter_bugs)
        
        columns = ('title', 'severity', 'date', 'status')
        self.tree = ttk.Treeview(parent, columns=columns, show='headings', cursor="hand2")
        
        self.tree.heading('title', text='Bug Title')
        self.tree.heading('severity', text='Severity')
        self.tree.heading('date', text='Date Submitted')
        self.tree.heading('status', text='Status')
        
        self.tree.column('title', width=300)
        self.tree.column('severity', width=100)
        self.tree.column('date', width=150)
        self.tree.column('status', width=100)
        
        vsb = ttk.Scrollbar(parent, orient="vertical", command=self.tree.yview)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=vsb.set)
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.bind('<Double-1>', self.show_bug_details)

    def upload_screenshot(self):
        filetypes = (("Image files", "*.png *.jpg *.jpeg"), ("All files", "*.*"))
        filename = filedialog.askopenfilename(title="Upload Screenshot", filetypes=filetypes)
        if filename:
            self.progress.start()
            self.root.after(2000, lambda: self.progress.stop())
            self.screenshot_path = filename

    def upload_video(self):
        filetypes = (("Video files", "*.mp4 *.avi *.mov"), ("All files", "*.*"))
        filename = filedialog.askopenfilename(title="Upload Video", filetypes=filetypes)
        if filename:
            self.progress.start()
            self.root.after(2000, lambda: self.progress.stop())
            self.video_path = filename

    def submit_bug(self):
        required_fields = [
            (self.title_entry, "Bug Title"),
            (self.desc_text, "Bug Description"),
            (self.severity_combo, "Severity Level"),
            (self.platform_combo, "Platform"),
            (self.version_entry, "Game Version")
        ]
        
        missing = []
        for field, name in required_fields:
            if isinstance(field, tk.Entry) and not field.get().strip():
                missing.append(name)
            elif isinstance(field, ttk.Combobox) and not field.get():
                missing.append(name)
            elif isinstance(field, tk.Text) and not field.get("1.0", tk.END).strip():
                missing.append(name)
        
        if missing:
            messagebox.showerror("Missing Information", f"Please fill in required fields:\n{', '.join(missing)}")
            return
        
        bug_data = {
            'title': self.title_entry.get(),
            'description': self.desc_text.get("1.0", tk.END).strip(),
            'steps': self.steps_text.get("1.0", tk.END).strip(),
            'severity': self.severity_combo.get(),
            'platform': self.platform_combo.get(),
            'version': self.version_entry.get(),
            'date': datetime.now().strftime("%Y-%m-%d %H:%M"),
            'status': 'Open',
            'screenshot': getattr(self, 'screenshot_path', None),
            'video': getattr(self, 'video_path', None)
        }
        
        self.bug_reports.append(bug_data)
        self.update_bug_list()
        self.save_reports()
        messagebox.showinfo("Success", "Bug report submitted successfully!")
        self.clear_form()

    def clear_form(self):
        self.title_entry.delete(0, tk.END)
        self.desc_text.delete("1.0", tk.END)
        self.steps_text.delete("1.0", tk.END)
        self.severity_combo.set('')
        self.platform_combo.set('')
        self.version_entry.delete(0, tk.END)
        self.progress.stop()
        if hasattr(self, 'screenshot_path'):
            del self.screenshot_path
        if hasattr(self, 'video_path'):
            del self.video_path

    def update_bug_list(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        for bug in self.bug_reports:
            self.tree.insert('', tk.END, values=(
                bug['title'],
                bug['severity'],
                bug['date'],
                bug['status']
            ))

    def filter_bugs(self, event=None):
        query = self.search_entry.get().lower()
        status = self.status_filter.get()
        
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        for bug in self.bug_reports:
            if (query in bug['title'].lower() or query in bug['description'].lower()) and \
               (status in ['All', bug['status']]):
                self.tree.insert('', tk.END, values=(
                    bug['title'],
                    bug['severity'],
                    bug['date'],
                    bug['status']
                ))

    def show_bug_details(self, event):
        selected = self.tree.focus()
        if not selected:
            return
        
        item = self.tree.item(selected)
        bug_title = item['values'][0]
        
        bug = next(b for b in self.bug_reports if b['title'] == bug_title)
        
        detail_win = tk.Toplevel(self.root)
        detail_win.title("Bug Details")
        detail_win.geometry("800x800")
        detail_win.configure(bg='#2d2d2d')
        
        container = ttk.Frame(detail_win)
        container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        def create_readonly_text(parent, content, height=5):
            frame = ttk.Frame(parent)
            frame.pack(fill=tk.X, pady=5)
            
            text_widget = tk.Text(
                frame, 
                wrap=tk.WORD, 
                height=height,
                bg='#4d4d4d', 
                fg='white',
                insertbackground='white',
                state='normal'
            )
            text_widget.insert(tk.END, content)
            text_widget.configure(state='disabled')
            
            vsb = ttk.Scrollbar(frame, orient="vertical", command=text_widget.yview)
            text_widget.configure(yscrollcommand=vsb.set)
            
            text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            vsb.pack(side=tk.RIGHT, fill=tk.Y)
            
            return text_widget
        
        ttk.Label(container, text=f"Title: {bug['title']}", font=('Arial', 12, 'bold')).pack(anchor=tk.W)
        
        ttk.Label(container, text="Description:").pack(anchor=tk.W, pady=(10, 0))
        desc_text = create_readonly_text(container, bug['description'], height=8)
        
        ttk.Label(container, text="Reproduction Steps:").pack(anchor=tk.W, pady=(10, 0))
        steps_text = create_readonly_text(container, bug['steps'], height=6)
        
        info_frame = ttk.Frame(container)
        info_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(info_frame, text=f"Severity: {bug['severity']}").pack(side=tk.LEFT, padx=10)
        ttk.Label(info_frame, text=f"Platform: {bug['platform']}").pack(side=tk.LEFT, padx=10)
        ttk.Label(info_frame, text=f"Status: {bug['status']}").pack(side=tk.LEFT, padx=10)
        
        media_frame = ttk.Frame(container)
        media_frame.pack(fill=tk.X, pady=10)

        if bug.get('screenshot'):
            try:
                img = Image.open(bug['screenshot'])
                img.thumbnail((200, 200))
                img = ImageTk.PhotoImage(img)
                screenshot_label = ttk.Label(media_frame, image=img)
                screenshot_label.image = img
                screenshot_label.pack(side=tk.LEFT, padx=10)
            except Exception as e:
                ttk.Label(media_frame, text="Failed to load screenshot").pack(side=tk.LEFT)

        if bug.get('video'):
            video_btn = ttk.Button(media_frame, text="▶ Play Video", 
                                  command=lambda: self.play_video(bug['video']))
            video_btn.pack(side=tk.LEFT, padx=10)

        btn_frame = ttk.Frame(container)
        btn_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(btn_frame, text="Mark as Resolved", 
                  command=lambda: self.update_bug_status(bug, "Closed", detail_win)).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Edit Report", 
                  command=lambda: self.edit_bug_report(bug, detail_win)).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Delete Report", 
                  command=lambda: self.delete_bug_report(bug, detail_win)).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Close", command=detail_win.destroy).pack(side=tk.RIGHT, padx=5)

    def play_video(self, video_path):
        try:
            if sys.platform == "win32":
                os.startfile(video_path)
            else:
                opener = "open" if sys.platform == "darwin" else "xdg-open"
                subprocess.call([opener, video_path])
        except Exception as e:
            messagebox.showerror("Playback Error", f"Could not play video: {str(e)}")

    def update_bug_status(self, bug, status, window):
        bug['status'] = status
        self.update_bug_list()
        self.save_reports()
        messagebox.showinfo("Status Updated", f"Bug status changed to {status}")
        window.destroy()

    def delete_bug_report(self, bug, window):
        confirm = messagebox.askyesno("Delete Report", "Are you sure you want to delete this bug report?")
        if confirm:
            self.bug_reports.remove(bug)
            self.update_bug_list()
            self.save_reports()
            messagebox.showinfo("Report Deleted", "The bug report has been deleted.")
            window.destroy()

    def edit_bug_report(self, bug, window):
        edit_win = tk.Toplevel(self.root)
        edit_win.title("Edit Bug Report")
        edit_win.geometry("600x400")
        edit_win.configure(bg='#2d2d2d')
        
        container = ttk.Frame(edit_win)
        container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        ttk.Label(container, text="Bug Title*:").grid(row=0, column=0, sticky=tk.W, pady=2)
        title_entry = ttk.Entry(container, width=60)
        title_entry.grid(row=0, column=1, columnspan=3, sticky=tk.W, pady=2)
        title_entry.insert(0, bug['title'])
        
        ttk.Label(container, text="Description*:").grid(row=1, column=0, sticky=tk.NW, pady=2)
        desc_text = tk.Text(container, width=60, height=5, bg='#4d4d4d', fg='white')
        desc_text.grid(row=1, column=1, columnspan=3, sticky=tk.W, pady=2)
        desc_text.insert(tk.END, bug['description'])
        
        ttk.Label(container, text="Reproduction Steps:").grid(row=2, column=0, sticky=tk.NW, pady=2)
        steps_text = tk.Text(container, width=60, height=3, bg='#4d4d4d', fg='white')
        steps_text.grid(row=2, column=1, columnspan=3, sticky=tk.W, pady=2)
        steps_text.insert(tk.END, bug['steps'])
        
        ttk.Label(container, text="Severity*:").grid(row=3, column=0, sticky=tk.W, pady=2)
        severity_combo = ttk.Combobox(container, values=["Low", "Medium", "High"], state="readonly")
        severity_combo.grid(row=3, column=1, sticky=tk.W, pady=2)
        severity_combo.set(bug['severity'])
        
        ttk.Label(container, text="Platform*:").grid(row=3, column=2, sticky=tk.W, pady=2)
        platform_combo = ttk.Combobox(container, values=["Windows", "Mac", "PlayStation", "Xbox"], state="readonly")
        platform_combo.grid(row=3, column=3, sticky=tk.W, pady=2)
        platform_combo.set(bug['platform'])
        
        ttk.Label(container, text="Game Version*:").grid(row=4, column=0, sticky=tk.W, pady=2)
        version_entry = ttk.Entry(container, width=20)
        version_entry.grid(row=4, column=1, sticky=tk.W, pady=2)
        version_entry.insert(0, bug['version'])
        
        submit_btn = ttk.Button(container, text="Save Changes", 
                               command=lambda: self.save_edited_bug(bug, title_entry.get(), 
                               desc_text.get("1.0", tk.END).strip(), 
                               steps_text.get("1.0", tk.END).strip(), 
                               severity_combo.get(), 
                               platform_combo.get(), 
                               version_entry.get(), 
                               edit_win))
        submit_btn.grid(row=5, column=3, sticky=tk.E, pady=20)

    def save_edited_bug(self, bug, title, description, steps, severity, platform, version, window):
        bug['title'] = title
        bug['description'] = description
        bug['steps'] = steps
        bug['severity'] = severity
        bug['platform'] = platform
        bug['version'] = version
        self.update_bug_list()
        self.save_reports()
        messagebox.showinfo("Success", "Bug report updated successfully!")
        window.destroy()

    def save_reports(self):
        with open('bug_reports.json', 'w') as f:
            json.dump(self.bug_reports, f)

    def load_reports(self):
        if os.path.exists('bug_reports.json'):
            with open('bug_reports.json', 'r') as f:
                self.bug_reports = json.load(f)

    def show_report_form(self):
        self.list_frame.pack_forget()
        self.form_frame.pack(fill=tk.BOTH, expand=True)

    def show_bug_list(self):
        self.form_frame.pack_forget()
        self.list_frame.pack(fill=tk.BOTH, expand=True)
        self.update_bug_list()

    def show_placeholder(self, text):
        messagebox.showinfo("Coming Soon", f"{text} section is under development")

#! ------ Run App ------
def RunApp():
    
    root = tk.Tk()
    
    app = BugReporterApp(root)
    
    root.mainloop() 

if __name__ == "__main__":
    RunApp()
