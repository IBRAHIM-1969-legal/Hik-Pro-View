"""
Hik-Pro View - V5c HD 1080p - SNAPSHOT - 100% Clear
Uses Main Stream Channel 101 for 1920x1080 Full HD
No H.264 decode, just JPEG - Perfect Clear
"""
import tkinter as tk
from PIL import Image, ImageTk
import threading, time, io, base64
import urllib.request
import urllib.error

class HikProV5cHD:
    def __init__(self, root):
        self.root = root
        self.root.title("Hik-Pro View - V5c HD 1080p - Full HD - No H264")
        self.root.geometry("1200x750")
        self.root.configure(bg="#0f0f0f")
        self.running = False
        self.frame_count = 0
        self.is_hd = True

        header = tk.Frame(root, bg="#000", height=50)
        header.pack(fill="x")
        tk.Label(header, text="V5c HD 1080p ✅", bg="#000", fg="#00FF88", font=("Arial", 15, "bold")).pack(side="left", padx=15, pady=10)
        tk.Label(header, text="Main Stream 101 | 1920x1080 Full HD | No pip | 100% Clear", bg="#000", fg="#00FF88", font=("Arial", 10)).pack(side="left")

        main = tk.Frame(root, bg="#111")
        main.pack(fill="both", expand=True)

        self.video_label = tk.Label(main, bg="black", text="کلیک بکە Connect\nV5c HD 1080p - Full HD\n100% ڕوون", fg="white", font=("Arial", 14))
        self.video_label.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        right = tk.Frame(main, bg="#1a1a1a", width=260)
        right.pack(side="right", fill="y")
        right.pack_propagate(False)

        tk.Label(right, text="V5c - HD 1080p", bg="#1a1a1a", fg="#00FF88", font=("Arial", 12, "bold")).pack(pady=10)
        for txt in ["Main Stream 101", "1920x1080 Full HD", "100% Clear JPEG", "No H264 decode", "No pixelation"]:
            tk.Label(right, text="✅ " + txt, bg="#1a1a1a", fg="white", font=("Arial", 9), anchor="w").pack(fill="x", padx=10, pady=2)

        # HD/SD Switch
        switch_frame = tk.Frame(right, bg="#1a1a1a")
        switch_frame.pack(fill="x", padx=10, pady=10)
        tk.Label(switch_frame, text="Quality:", bg="#1a1a1a", fg="white").pack(side="left")
        self.quality_var = tk.StringVar(value="HD 1080p")
        tk.Radiobutton(switch_frame, text="HD 1080p", variable=self.quality_var, value="HD 1080p", bg="#1a1a1a", fg="white", selectcolor="#333", command=self.on_quality).pack(side="left")
        tk.Radiobutton(switch_frame, text="SD 480p", variable=self.quality_var, value="SD 480p", bg="#1a1a1a", fg="white", selectcolor="#333", command=self.on_quality).pack(side="left")

        tk.Label(right, text="زانیاری پەیوەندی", bg="#1a1a1a", fg="gray", font=("Arial", 9)).pack(pady=(15,5))

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

        self.btn = tk.Button(right, text="▶ CONNECT HD 1080p", bg="#0066cc", fg="white", font=("Arial", 11, "bold"), command=self.toggle, height=2)
        self.btn.pack(fill="x", padx=10, pady=10)

        self.status = tk.Label(right, text="Ready - HD Mode\nMain Stream 101", bg="#1a1a1a", fg="#00ff88", font=("Arial", 8), wraplength=230, justify="left")
        self.status.pack(fill="x", padx=10)

        self.save_btn = tk.Button(right, text="📸 Save HD Photo", bg="#333", fg="white", command=self.save_photo)
        self.save_btn.pack(fill="x", padx=10, pady=5)

        self.last_pil = None

    def on_quality(self):
        q = self.quality_var.get()
        self.is_hd = (q == "HD 1080p")
        if self.is_hd:
            self.btn.config(text="▶ CONNECT HD 1080p", bg="#0066cc")
            self.status.config(text="Mode: HD 1080p - Channel 101\nFull HD 1920x1080")
        else:
            self.btn.config(text="▶ CONNECT SD 480p", bg="#00aa44")
            self.status.config(text="Mode: SD 480p - Channel 102\nFast 640x480")

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
        
        # HD = 101, SD = 102
        if self.is_hd:
            snap_ch = ch_num * 100 + 1  # 101 = main stream HD
        else:
            snap_ch = ch_num * 100 + 2  # 102 = sub stream SD

        self.ip = ip
        self.user = user
        self.pwd = pwd
        self.snap_ch = snap_ch
        self.snap_url = f"http://{ip}/ISAPI/Streaming/channels/{snap_ch}/picture"

        self.status.config(text=f"Trying: channels/{snap_ch}/picture\n{'HD 1080p' if self.is_hd else 'SD 480p'}...")
        self.running = True
        self.btn.config(text="■ STOP", bg="#aa0000")
        threading.Thread(target=self.snapshot_loop, daemon=True).start()

    def stop(self):
        self.running = False
        txt = "▶ CONNECT HD 1080p" if self.is_hd else "▶ CONNECT SD 480p"
        bg = "#0066cc" if self.is_hd else "#00aa44"
        self.btn.config(text=txt, bg=bg)

    def fetch_jpeg(self, url, user, pwd):
        try:
            credentials = f"{user}:{pwd}"
            b64 = base64.b64encode(credentials.encode()).decode()
            req = urllib.request.Request(url)
            req.add_header("Authorization", f"Basic {b64}")
            with urllib.request.urlopen(req, timeout=5) as resp:
                data = resp.read()
                if len(data) > 1000 and data[:2] == b'\xff\xd8':
                    return data
                return None
        except urllib.error.HTTPError as e:
            if e.code == 401:
                try:
                    pm = urllib.request.HTTPPasswordMgrWithDefaultRealm()
                    pm.add_password(None, url, user, pwd)
                    handler = urllib.request.HTTPDigestAuthHandler(pm)
                    opener = urllib.request.build_opener(handler)
                    with opener.open(url, timeout=5) as resp2:
                        data = resp2.read()
                        if len(data) > 1000:
                            return data
                except:
                    return None
            return None
        except:
            return None

    def save_photo(self):
        if self.last_pil:
            try:
                filename = f"Hik-Pro-HD-1080p-{int(time.time())}.jpg"
                self.last_pil.save(filename, "JPEG", quality=95)
                self.status.config(text=f"Saved: {filename}\nFull HD!")
            except Exception as e:
                self.status.config(text=f"Save failed: {e}")

    def snapshot_loop(self):
        consecutive_fail = 0
        while self.running:
            start_t = time.time()
            data = self.fetch_jpeg(self.snap_url, self.user, self.pwd)
            if data and len(data) > 1000:
                try:
                    pil_img = Image.open(io.BytesIO(data))
                    if pil_img.mode != 'RGB':
                        pil_img = pil_img.convert('RGB')
                    self.last_pil = pil_img.copy()
                    self.frame_count += 1
                    
                    # For display, thumbnail to fit screen but keep high res for save
                    label_w = self.video_label.winfo_width()
                    label_h = self.video_label.winfo_height()
                    if label_w < 100: label_w = 1000
                    if label_h < 100: label_h = 700
                    
                    display_img = pil_img.copy()
                    display_img.thumbnail((label_w-20, label_h-20), Image.LANCZOS)
                    
                    imgtk = ImageTk.PhotoImage(image=display_img)
                    self.video_label.config(image=imgtk, text="")
                    self.video_label.image = imgtk
                    
                    res_text = "1920x1080" if self.is_hd else "640x480"
                    self.status.config(text=f"Live! Frame {self.frame_count}\n{len(data)//1024}KB - {res_text} - 100% Clear\nChannel {self.snap_ch} - No H264!\nHD Mode: {self.is_hd}")
                    consecutive_fail = 0
                except Exception as e:
                    consecutive_fail += 1
            else:
                consecutive_fail += 1
                self.status.config(text=f"Fail {consecutive_fail} - Retrying\nURL: {self.snap_ch}/picture\nCheck Main Stream is STD_H264")
                if consecutive_fail > 3:
                    time.sleep(1)
            
            elapsed = time.time() - start_t
            # HD is bigger, so slower FPS for stability: 0.15s = ~6-7 FPS for HD
            target_delay = 0.15 if self.is_hd else 0.1
            sleep_t = target_delay - elapsed
            if sleep_t > 0:
                time.sleep(sleep_t)

if __name__ == "__main__":
    root = tk.Tk()
    app = HikProV5cHD(root)
    root.mainloop()
