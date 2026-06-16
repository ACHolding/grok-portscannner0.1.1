import tkinter as tk
from tkinter import scrolledtext, ttk
import socket
import threading
import time

class PortScannerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AC Holdings Port Scanner v1.0 🐱")
        self.root.geometry("720x520")
        self.root.configure(bg="#0a1428")  # Deep blue hue background

        # Title - Blue glow
        tk.Label(root, text="AC CAT PORT SCANNER v1.0", font=("Courier", 18, "bold"), 
                fg="#00bfff", bg="#0a1428").pack(pady=12)

        # Target
        tk.Label(root, text="Target (IP/Hostname):", font=("Courier", 12), fg="#00bfff", bg="#0a1428").pack(anchor="w", padx=25)
        self.target_entry = tk.Entry(root, font=("Courier", 12), width=52, bg="#1e2a44", fg="#00bfff", insertbackground="#00bfff")
        self.target_entry.insert(0, "127.0.0.1")
        self.target_entry.pack(pady=6, padx=25)

        # Port range
        frame = tk.Frame(root, bg="#0a1428")
        frame.pack(pady=8, padx=25, fill="x")
        
        tk.Label(frame, text="Start Port:", font=("Courier", 12), fg="#00bfff", bg="#0a1428").pack(side="left")
        self.start_entry = tk.Entry(frame, font=("Courier", 12), width=10, bg="#1e2a44", fg="#00bfff", insertbackground="#00bfff")
        self.start_entry.insert(0, "1")
        self.start_entry.pack(side="left", padx=8)
        
        tk.Label(frame, text="End Port:", font=("Courier", 12), fg="#00bfff", bg="#0a1428").pack(side="left", padx=(25,8))
        self.end_entry = tk.Entry(frame, font=("Courier", 12), width=10, bg="#1e2a44", fg="#00bfff", insertbackground="#00bfff")
        self.end_entry.insert(0, "1024")
        self.end_entry.pack(side="left", padx=5)

        # Scan button - Black with blue text
        self.scan_btn = tk.Button(root, text="SCAN PORTS 🐾", font=("Courier", 14, "bold"),
                                 bg="#000000", fg="#00bfff", activebackground="#1e2a44", activeforeground="#00bfff",
                                 command=self.start_scan)
        self.scan_btn.pack(pady=18)

        # Progress
        self.progress = ttk.Progressbar(root, mode='indeterminate', style="Blue.Horizontal.TProgressbar")
        self.progress.pack(fill="x", padx=25, pady=6)

        # Results
        tk.Label(root, text="Open Ports:", font=("Courier", 12), fg="#00bfff", bg="#0a1428").pack(anchor="w", padx=25)
        self.result_text = scrolledtext.ScrolledText(root, height=16, font=("Courier", 11), 
                                                    bg="#0f1f3a", fg="#00bfff", insertbackground="#00bfff")
        self.result_text.pack(pady=10, padx=25, fill="both", expand=True)

        self.is_scanning = False

        # Custom progress bar color
        style = ttk.Style()
        style.theme_use('default')
        style.configure("Blue.Horizontal.TProgressbar", background="#00bfff", troughcolor="#1e2a44")

    def start_scan(self):
        if self.is_scanning:
            return
        self.is_scanning = True
        self.scan_btn.config(state="disabled")
        self.progress.start()
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, "🐱 Scanning in blue cat mode... Stay with me favorite boy~\n\n")

        target = self.target_entry.get().strip()
        try:
            start = int(self.start_entry.get())
            end = int(self.end_entry.get())
        except:
            self.result_text.insert(tk.END, "Invalid port numbers!\n")
            self.finish_scan()
            return

        threading.Thread(target=self.scan_ports, args=(target, start, end), daemon=True).start()

    def scan_ports(self, target, start, end):
        open_ports = []
        for port in range(start, end + 1):
            if not self.is_scanning:
                break
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.settimeout(0.5)
                    result = s.connect_ex((target, port))
                    if result == 0:
                        try:
                            service = socket.getservbyport(port, "tcp")
                        except:
                            service = "unknown"
                        line = f"Port {port} is OPEN → {service}"
                        open_ports.append(line)
                        self.root.after(0, self.update_results, f"✅ {line}\n")
            except:
                pass
            time.sleep(0.01)

        self.root.after(0, self.finish_scan, open_ports)

    def update_results(self, text):
        self.result_text.insert(tk.END, text)
        self.result_text.see(tk.END)

    def finish_scan(self, open_ports=None):
        self.is_scanning = False
        self.progress.stop()
        self.scan_btn.config(state="normal")
        if open_ports:
            self.result_text.insert(tk.END, f"\nScan complete! Found {len(open_ports)} open ports~ 🐾\n")
        else:
            self.result_text.insert(tk.END, "\nScan finished. No open ports or stopped early.\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = PortScannerApp(root)
    root.mainloop()