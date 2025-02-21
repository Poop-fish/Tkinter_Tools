from imports import ( tk, ttk, webview )

class WebApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Webview")
        self.root.geometry("900x600")
        self.embed_webview()
    
    def embed_webview(self):
        webview.create_window("Webview in Tkinter", "https://www.google.ca/", width=1000, height=800, resizable=True)
        webview.start()

#! ---- Run App ----
def RunApp():
    
    root = tk.Tk()
    
    app = WebApp(root)
    
    root.mainloop()

if __name__ == "__main__":
    RunApp()