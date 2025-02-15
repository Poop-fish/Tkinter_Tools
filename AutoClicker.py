from CustomStyle import SimpleStyle 
from imports import ( tk , ttk, pyautogui, keyboard, threading, time )

class AutoClickerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Auto Clicker")
        self.root.geometry("450x400")
        self.root.resizable(False, False)
        self.root.configure(bg="black")
        self.root.iconbitmap("Assets/Appicon_1.ico")
        self.clicking = False
        self.click_interval = tk.DoubleVar(value=0.0001)
        self.start_key = "f6"
        self.stop_key = "f7"
        self.start_key_press_count = 0
        SimpleStyle(root)

        #! ----
        self.main_frame = ttk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        #! ----
        self.title_label = ttk.Label(self.main_frame, text="Auto Clicker", font=("Helvetica", 16, "bold"))
        self.title_label.grid(row=0, column=0, columnspan=2, pady=10)
        #! ----
        self.interval_frame = ttk.LabelFrame(self.main_frame, text="Click Interval (seconds)", padding=10 )
        self.interval_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        #! ----
        self.interval_options = [1.0, 0.9, 0.08, 0.007, 0.0006, 0.0005, 0.0004, 0.0003, 0.0002, 0.0001]
        self.interval_dropdown = ttk.Combobox(
            self.interval_frame,
            values=self.interval_options,
            textvariable=self.click_interval,
            state="readonly"
        )
        self.interval_dropdown.grid(row=0, column=0, sticky="ew", pady=5)
        self.interval_dropdown.current(0)
        #! ----
        self.custom_interval_entry = ttk.Entry(
            self.interval_frame,
            textvariable=self.click_interval
        )
        self.custom_interval_entry.grid(row=1, column=0, sticky="ew", pady=5)
        #! ----
        self.keybind_frame = ttk.LabelFrame(self.main_frame, text="Keybind Settings", padding=10)
        self.keybind_frame.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)
        #! ----
        self.start_button = ttk.Button(
            self.keybind_frame,
            text=f"Start ({self.start_key.upper()})",
            command=self.start_clicking
        )
        self.start_button.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        self.start_button.bind("<Button-3>", self.change_start_key)
        #! ----
        self.stop_button = ttk.Button(
            self.keybind_frame,
            text=f"Stop ({self.stop_key.upper()})",
            command=self.stop_clicking,
            state=tk.DISABLED
        )
        self.stop_button.grid(row=1, column=0, padx=5, pady=5, sticky="ew")
        self.stop_button.bind("<Button-3>", self.change_stop_key)
        #! ----
        self.status_frame = ttk.LabelFrame(self.main_frame, text="Status", padding=10)
        self.status_frame.grid(row=2, column=0, columnspan=2, padx=5, pady=5)
        #! ----
        self.status_label = ttk.Label(self.status_frame, text="Status: Stopped", font=("Helvetica", 12))
        self.status_label.grid(row=0, column=0, pady=5)
        #! ----
        self.info_label = ttk.Label(
            self.main_frame,
            text="Press And Hold Your Start Key\nKeybind multiple times to increase click speed\nBEWARE DONT GO TO FAST",
            justify=tk.CENTER
        )
        self.info_label.grid(row=3, column=0, columnspan=2, pady=5)

        self.info_label2 = ttk.Label(
            self.main_frame,
            text="Right-click Start/Stop button and click a Key you want to bind",
            justify=tk.CENTER
        )
        self.info_label2.grid(row=4, column=0, columnspan=2, pady=5)
        #! ----
        keyboard.add_hotkey(self.start_key, self.start_clicking)
        keyboard.add_hotkey(self.stop_key, self.stop_clicking)

    def change_start_key(self, event):
        """Change the start keybind."""
        self.status_label.config(text="Press a key for Start")
        new_key = keyboard.read_event().name
        self.start_key = new_key
        self.start_button.config(text=f"Start ({self.start_key.upper()})")
        keyboard.add_hotkey(self.start_key, self.start_clicking)
        self.status_label.config(text="Status: Stopped")

    def change_stop_key(self, event):
        """Change the stop keybind."""
        self.status_label.config(text="Press a key for Stop")
        new_key = keyboard.read_event().name
        self.stop_key = new_key
        self.stop_button.config(text=f"Stop ({self.stop_key.upper()})")
        keyboard.add_hotkey(self.stop_key, self.stop_clicking)
        self.status_label.config(text="Status: Stopped")

    def start_clicking(self):
        """Start the auto-clicker."""
        self.start_key_press_count += 1
        if self.start_key_press_count > 1:
            new_interval = max(self.click_interval.get() - 0.0001, 0.00001)
            self.click_interval.set(new_interval)

        try:
            self.click_interval.set(float(self.custom_interval_entry.get()))
        except ValueError:
            self.click_interval.set(0.0001)

        self.clicking = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.status_label.config(text="Status: Clicking...")

        self.click_thread = threading.Thread(target=self.auto_click)
        self.click_thread.start()

    def stop_clicking(self):
        """Stop the auto-clicker."""
        self.clicking = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.status_label.config(text="Status: Stopped")
        self.start_key_press_count = 0  

    def auto_click(self):
        """Auto-clicker logic."""
        while self.clicking:
            pyautogui.click()
            time.sleep(self.click_interval.get()) 

#! ------ Run App ------

def Auto_Clicker_App ():
   
    root = tk.Tk()
    
    app = AutoClickerApp(root)
    
    root.mainloop() 

if __name__ == "__main__":
  Auto_Clicker_App()
