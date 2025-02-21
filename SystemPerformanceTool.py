from imports import (tk, ttk, Image, filedialog, messagebox, random, string, GPUtil, psutil, FigureCanvasTkAgg, plt)
from CustomStyle import SimpleStyle 

class SystemPerformanceWidget(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        SimpleStyle(self)
        self.cpu_usage_history = []
        self.gpu_usage_history = []
        self.memory_usage_history = []
        
        cpu_frame = ttk.Frame(self)
        cpu_frame.pack(fill=tk.X, pady=10)

        self.cpu_label = ttk.Label(cpu_frame, text="CPU Usage: -", font=("Helvetica", 14, "bold"), foreground="white", background="#1f1f1f")
        self.cpu_label.pack(anchor=tk.W)

        self.cpu_progress = ttk.Progressbar(cpu_frame, orient=tk.HORIZONTAL, length=350, mode='determinate', style="TProgressbar")
        self.cpu_progress.pack(fill=tk.X)

        gpu_frame = ttk.Frame(self)
        gpu_frame.pack(fill=tk.X, pady=10)

        self.gpu_label = ttk.Label(gpu_frame, text="GPU Usage: -", font=("Helvetica", 14, "bold"), foreground="white", background="#1f1f1f")
        self.gpu_label.pack(anchor=tk.W)

        self.gpu_progress = ttk.Progressbar(gpu_frame, orient=tk.HORIZONTAL, length=350, mode='determinate', style="TProgressbar")
        self.gpu_progress.pack(fill=tk.X)

        memory_frame = ttk.Frame(self)
        memory_frame.pack(fill=tk.X, pady=10)

        self.memory_label = ttk.Label(memory_frame, text="Memory Usage: -", font=("Helvetica", 14, "bold"), foreground="white", background="#1f1f1f")
        self.memory_label.pack(anchor=tk.W)

        self.memory_progress = ttk.Progressbar(memory_frame, orient=tk.HORIZONTAL, length=350, mode='determinate', style="TProgressbar")
        self.memory_progress.pack(fill=tk.X)

        self.fig, (self.ax1, self.ax2, self.ax3) = plt.subplots(3, 1, figsize=(5, 3), dpi=100)
        self.ax1.set_title('CPU Usage (%)', fontsize=12, color='white')
        self.ax2.set_title('GPU Usage (%)', fontsize=12, color='white')
        self.ax3.set_title('Memory Usage (%)', fontsize=12, color='white')

        self.fig.patch.set_facecolor('#262626')
        self.ax1.set_facecolor('#262626')
        self.ax2.set_facecolor('#262626')
        self.ax3.set_facecolor('#262626')

        self.canvas = FigureCanvasTkAgg(self.fig, self)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        self.update_dashboard()

    def get_system_stats(self):
        cpu_usage = psutil.cpu_percent(interval=0.1)

        memory_info = psutil.virtual_memory()
        memory_usage = memory_info.percent

        gpu_usage = "N/A"
        gpus = GPUtil.getGPUs()
        if gpus:
            gpu_usage = f"{gpus[0].load * 100:.1f}%"

        return {
            "CPU": f"{cpu_usage}%",
            "GPU": gpu_usage,
            "Memory": f"{memory_usage}%"
        }

    def update_dashboard(self):
        stats = self.get_system_stats()

        self.cpu_label.config(text=f"CPU Usage: {stats['CPU']}")
        self.cpu_progress['value'] = float(stats['CPU'].strip('%'))

        self.gpu_label.config(text=f"GPU Usage: {stats['GPU']}")
        if stats['GPU'] != "N/A":
            self.gpu_progress['value'] = float(stats['GPU'].strip('%'))
        else:
            self.gpu_progress['value'] = 0

        self.memory_label.config(text=f"Memory Usage: {stats['Memory']}")
        self.memory_progress['value'] = float(stats['Memory'].strip('%'))

        self.cpu_usage_history.append(float(stats['CPU'].strip('%')))
        self.gpu_usage_history.append(float(stats['GPU'].strip('%')) if stats['GPU'] != "N/A" else 0)
        self.memory_usage_history.append(float(stats['Memory'].strip('%')))

        if len(self.cpu_usage_history) > 100:
            self.cpu_usage_history.pop(0)
            self.gpu_usage_history.pop(0)
            self.memory_usage_history.pop(0)

        self.ax1.plot(self.cpu_usage_history, color='#FF5733', linewidth=2)
        self.ax2.plot(self.gpu_usage_history, color='#33C1FF', linewidth=2)
        self.ax3.plot(self.memory_usage_history, color='#8E44AD', linewidth=2)

        self.canvas.draw()

        self.after(1000, self.update_dashboard)

class SystemPerformance(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("System Performance")
        self.geometry("800x800")
        self.configure(bg='#1f1f1f')
        self.iconbitmap('Assets/FaceLogo.ico')
        performance_widget = SystemPerformanceWidget(self)
        performance_widget.pack(fill=tk.BOTH, expand=True)

#! ---- Run App ----
def RunApp():
    
    app = SystemPerformance()
    
    app.mainloop()

if __name__ == "__main__":
    RunApp() 