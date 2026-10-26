"""
Hik-Pro View - V5b SNAPSHOT - NO EXTERNAL LIBS
Uses only built-in urllib, no requests needed.
100% Clear JPEG from NVR.
"""
import tkinter as tk
from PIL import Image, ImageTk
import threading, time, io, base64
import urllib.request
import urllib.error

class HikProV5b:
    def __init__(self, root):
        self.root = root
        self.root.title("Hik-Pro View - V5b SNAPSHOT - Built-in Only - No pip needed")
        self.root.geometry("1100x700")
        self.root.configure(bg="#0f0f0f")
        self.running = False
        self.frame_count = 0

        header = tk.Frame(root, bg="#000", height=50)
        header.pack(fill="x")
        tk.Label(header, text="V5b SNAPSHOT ✅ No pip install", bg="#000", fg="#00FF88", font=("Arial", 14, "bold")).pack(side="left", padx=15, pady=10)
        tk.Label(header, text="Uses urllib - No requests - 100% Clear", bg="#000", fg="yellow", font=("Arial", 9)).pack(side="left")

        main = tk.Frame(root, bg="#111")
        main.pack(fill="both", expand=True)

        self.video_label = tk.Label(main, bg="black", text="کلیک بکە Connect\nV5b - بە urllib - 100% ڕوون\nپێویست بە pip ناکات", fg="white", font=("Arial", 14))
        self.video_label.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        right = tk.Frame(main, bg="#1a1a1a", width=240)
        right.pack(side="right", fill="y")
        right.pack_propagate(False)

        tk.Label(right, text="V5b - بێ requests", bg="#1a1a1a", fg="#00FF88", font=("Arial", 11, "bold")).pack(pady=10)
        for txt in ["No pip install", "No requests lib", "Uses urllib only", "100% Clear JPEG", "No H264 errors"]:
            tk.Label(right, text="✅ " + txt, bg="#1a1a1a", fg="white", font=("Arial", 8), anchor="w").pack(fill="x", padx=10, pady=2)

        tk.Label(right, text="زانیاری پەیوەندی", bg="#1a1a1a", fg="gray", font=("Arial", 9)).pack(pady=(20,5))

        f1 = tk.Frame(right, bg="#1a1a1a"); f1.pack(fill="x", padx=10, pady=3)
        tk.Label(f1, text="NVR IP:", bg="#1a1a1a", fg="white", width=7, anchor="w").pack(side="left")
        self.ip_entry = tk.Entry(f1); self.ip_entry.insert(0, "192.168.4.12"); self.ip_entry.pack(side="left", fill="x", expand=True)

        f2 = tk.Frame(right, bg="#1a1a1a"); f2.pack(fill="x", padx=10, pady=3)
        tk.Label(f2, text="User:", bg="#1a1a1a", fg="white", width=7, anchor="w").pack(side="left")
        self.user_entry = tk.Entry(f2); self.user_entry.insert(0, "admin"); self.user_entry.pack(side="left", fill="x", expand=True)

        f3 = tk.Frame(right, bg="#1a1a1a"); f3.pack(fill="x", padx=10, pady=3)
        tk.Label(f3, text="Pass:", bg="#1a1a1a", fg="white", width=7, anchor="w").pack(side="left")
        self.pass_entry = tk.Entry(f3, show="*"); self.pass_entry.pack(side="left", fill="x", expand=True)

        f4 = tk.Frame(right, bg="#1a1a1a"); f4.pack(fill="x", padx=10, pady=3)
        tk.Label(f4, text="Channel:", bg="#1a1a1a", fg="white", width=7, anchor="w").pack(side="left")
        self.ch_entry = tk.Entry(f4); self.ch_entry.insert(0, "1"); self.ch_entry.pack(side="left", fill="x", expand=True)

        self.btn = tk.Button(right, text="▶ CONNECT V5b", bg="#00aa44", fg="white", font=("Arial", 11, "bold"), command=self.toggle, height=2)
        self.btn.pack(fill="x", padx=10, pady=10)

        self.status = tk.Label(right, text="Ready - No pip needed\nJust click Connect", bg="#1a1a1a", fg="#00ff88", font=("Arial", 8), wraplength=210, justify="left")
        self.status.pack(fill="x", padx=10)

        self.log = tk.Text(right, bg="#0a0a0a", fg="#888", font=("Courier", 7), height=10)
        self.log.pack(fill="x", padx=10, pady=10)
        self.log.insert("1.0", "Log:\n")

    def toggle(self):
        if self.running:
            self.stop()
        else:
            self.start()

    def start(self):
        ip = self.ip_entry.get().strip()
        user = self.user_entry.get().strip() or "admin"
        pwd = self.pass_entry.get().strip()
        ch = self.ch_entry.get().strip() or "1"
        if not ch.isdigit(): ch = "1"
        ch_num = int(ch)
        snap_ch = ch_num * 100 + 2  # 102

        self.ip = ip
        self.user = user
        self.pwd = pwd
        self.snap_ch = snap_ch
        self.snap_url = f"http://{ip}/ISAPI/Streaming/channels/{snap_ch}/picture"
        # Also try alternative URL: /ISAPI/Streaming/channels/{ch}01/picture?videoResolutionWidth=640
        self.alt_url = f"http://{ip}/ISAPI/Streaming/channels/101/picture"

        self.log.insert("end", f"Trying {self.snap_url}\n")
        self.status.config(text=f"Trying: {snap_ch}/picture\nBasic Auth...")
        self.running = True
        self.btn.config(text="■ STOP", bg="#aa0000")
        threading.Thread(target=self.snapshot_loop, daemon=True).start()

    def stop(self):
        self.running = False
        self.btn.config(text="▶ CONNECT V5b", bg="#00aa44")
        self.status.config(text="Stopped")

    def fetch_jpeg(self, url, user, pwd):
        # Try Basic Auth first (Hikvision supports both)
        try:
            # Create basic auth header
            credentials = f"{user}:{pwd}"
            b64 = base64.b64encode(credentials.encode()).decode()
            req = urllib.request.Request(url)
            req.add_header("Authorization", f"Basic {b64}")
            # Increase timeout
            with urllib.request.urlopen(req, timeout=5) as resp:
                data = resp.read()
                if len(data) > 1000 and data[:2] == b'\xff\xd8':  # JPEG magic
                    return data
                else:
                    # Might be XML error, try to log
                    self.log.insert("end", f"Not JPEG: {data[:200]}\n")
                    return None
        except urllib.error.HTTPError as e:
            self.log.insert("end", f"HTTPError {e.code}: {e.read()[:100]}\n")
            # If 401, try digest
            if e.code == 401:
                try:
                    # Try with password manager for digest
                    pm = urllib.request.HTTPPasswordMgrWithDefaultRealm()
                    pm.add_password(None, url, user, pwd)
                    handler = urllib.request.HTTPDigestAuthHandler(pm)
                    opener = urllib.request.build_opener(handler)
                    urllib.request.install_opener(opener)
                    with urllib.request.urlopen(url, timeout=5) as resp2:
                        data = resp2.read()
                        if len(data) > 1000:
                            return data
                except Exception as e2:
                    self.log.insert("end", f"Digest failed: {e2}\n")
                    return None
            return None
        except Exception as e:
            self.log.insert("end", f"Fetch error: {e}\n")
            return None

    def snapshot_loop(self):
        consecutive_fail = 0
        url_to_try = self.snap_url
        while self.running:
            start_t = time.time()
            data = self.fetch_jpeg(url_to_try, self.user, self.pwd)
            if data is None and url_to_try == self.snap_url:
                # Try alt URL (101)
                self.log.insert("end", f"Trying alt {self.alt_url}\n")
                url_to_try = self.alt_url
                data = self.fetch_jpeg(url_to_try, self.user, self.pwd)
            
            if data and len(data) > 1000:
                try:
                    pil_img = Image.open(io.BytesIO(data))
                    if pil_img.mode != 'RGB':
                        pil_img = pil_img.convert('RGB')
                    self.frame_count += 1
                    
                    # Resize
                    label_w = self.video_label.winfo_width()
                    label_h = self.video_label.winfo_height()
                    if label_w < 100: label_w = 800
                    if label_h < 100: label_h = 600
                    pil_img.thumbnail((label_w-20, label_h-20), Image.LANCZOS)
                    
                    imgtk = ImageTk.PhotoImage(image=pil_img)
                    self.video_label.config(image=imgtk, text="")
                    self.video_label.image = imgtk
                    self.status.config(text=f"Live! Frame {self.frame_count}\n{len(data)//1024}KB - 100% Clear\nURL: {self.snap_ch}\nNo H264 errors!")
                    consecutive_fail = 0
                except Exception as e:
                    self.log.insert("end", f"Img error: {e}\n")
                    consecutive_fail += 1
            else:
                consecutive_fail += 1
                self.status.config(text=f"Fail {consecutive_fail} - No JPEG\nURL: {url_to_try}\nCheck IP/User/Pass\nFirewall?")
                if consecutive_fail > 3:
                    time.sleep(1)
            
            # 10 FPS ~ 0.1s delay
            elapsed = time.time() - start_t
            sleep_t = 0.1 - elapsed
            if sleep_t > 0:
                time.sleep(sleep_t)
            
            # Keep log short
            lines = self.log.get("1.0", "end").split("\n")
            if len(lines) > 30:
                self.log.delete("1.0", "10.0")

if __name__ == "__main__":
    root = tk.Tk()
    app = HikProV5b(root)
    root.mainloop()
