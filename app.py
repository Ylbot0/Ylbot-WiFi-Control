import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import threading
import requests
import webbrowser
from PIL import Image, ImageTk

class WifiControlApp:
    def __init__(self, root):
        self.root = root
        self.root.title("随身网卡控制器")
        self.root.geometry("600x820")
        self.root.resizable(False, False)
        self.root.configure(bg="#102A43")

        self.ip = "192.168.68.1"
        self.key = "wifi123456"
        self.scanning = False
        self.show_welcome()
        top_bar = tk.Frame(root, bg="#165DFF", height=50)
        top_bar.pack(fill=tk.X)
        title = tk.Label(top_bar, text="随身网卡控制器", font=("微软雅黑",14,"bold"), fg="white", bg="#165DFF")
        title.pack(pady=10)
        btn_frame = tk.Frame(root, bg="#102A43")
        btn_frame.pack(pady=8)

        self.set_btn = tk.Button(btn_frame, text="⚙ 设置", font=("微软雅黑",10),
                                 bg="#2563EB", fg="white", width=10,
                                 command=self.open_setting_window)
        self.set_btn.grid(row=0, column=0, padx=5)

        self.refresh_sta_btn = tk.Button(btn_frame, text="🔄 刷新状态", font=("微软雅黑",10),
                                         bg="#2563EB", fg="white", width=12,
                                         command=self.manual_refresh)
        self.refresh_sta_btn.grid(row=0, column=1, padx=5)

        self.scan_btn = tk.Button(btn_frame, text="🔍 搜索WiFi", font=("微软雅黑",10),
                                  bg="#2563EB", fg="white", width=12,
                                  command=self.start_scan)
        self.scan_btn.grid(row=0, column=2, padx=5)
        tk.Label(root, text="可用WiFi", font=("微软雅黑",10), fg="white", bg="#102A43").pack(anchor="w", padx=15)
        self.wifi_list = tk.Listbox(root, font=("微软雅黑",10), height=12,
                                    bg="#0F172A", fg="white",
                                    selectbackground="#2563EB", bd=0, highlightthickness=0)
        self.wifi_list.pack(fill=tk.X, padx=15, pady=5)
        self.wifi_list.bind("<Double-1>", self.try_connect)
        tk.Label(root, text="运行日志", font=("微软雅黑",10), fg="white", bg="#102A43").pack(anchor="w", padx=15)
        self.log_text = tk.Text(root, font=("Consolas",9), height=8,
                                bg="#0F172A", fg="white", bd=0)
        self.log_text.pack(fill=tk.X, padx=15, pady=5)
        sta_frame = tk.LabelFrame(root, text=" 设备状态 ", font=("微软雅黑",10,"bold"),
                                  bg="#102A43", fg="white",
                                  labelanchor="n", bd=2, relief=tk.GROOVE)
        sta_frame.pack(fill=tk.X, padx=15, pady=10)

        self.sta_text = tk.Label(sta_frame, font=("微软雅黑",9), fg="white", bg="#102A43",
                                 justify=tk.LEFT, anchor="w")
        self.sta_text.pack(fill=tk.X, padx=10, pady=8)
        bottom_frame = tk.Frame(root, bg="#102A43")
        bottom_frame.pack(pady=10, fill=tk.X)
        try:
            qr_img = Image.open("2.png").resize((120, 120), Image.Resampling.LANCZOS)
            self.qr_photo = ImageTk.PhotoImage(qr_img)
            qr_label = tk.Label(bottom_frame, image=self.qr_photo, bg="#102A43")
            qr_label.pack(side=tk.LEFT, padx=15)
        except:
            tk.Label(bottom_frame, text="null", fg="red", bg="#102A43").pack(side=tk.LEFT, padx=15)
        info_frame = tk.Frame(bottom_frame, bg="#102A43")
        info_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)

        tk.Label(info_frame, text="给开发者买杯咖啡 ☕", font=("微软雅黑",11,"bold"),
                 fg="white", bg="#102A43").pack(anchor="w", pady=2)
        github_label = tk.Label(info_frame, text="GitHub: https://github.com/Ylbot0",
                                font=("微软雅黑",10), fg="#4FC3F7", bg="#102A43", cursor="hand2")
        github_label.pack(anchor="w")
        github_label.bind("<Button-1>", lambda e: webbrowser.open("https://github.com/Ylbot0"))

        tk.Label(info_frame, text="基于高通410随身WiFi控制器", font=("微软雅黑",9),
                 fg="#90CAF9", bg="#102A43").pack(anchor="w", pady=2)

        self.log("系统启动成功")
        self.update_device_info()

    # ========== 欢迎提示 ==========
    def show_welcome(self):
        msg = (
            "本项目是 Ylbot 基于高通410随身WiFi研发的控制系统\n"
            "项目已在 GitHub 开源：https://github.com/Ylbot0\n\n"
            "版权所有 @Ylbot"
        )
        messagebox.showinfo("欢迎使用", msg)

    def log(self, msg):
        self.log_text.insert(tk.END, f"• {msg}\n")
        self.log_text.see(tk.END)
    def open_setting_window(self):
        pwd = simpledialog.askstring("权限验证", "请输入管理员密码：", show="*")
        if pwd != "123456":
            messagebox.showerror("错误", "密码错误")
            return

        set_win = tk.Toplevel(self.root)
        set_win.title("系统设置")
        set_win.geometry("400x220")
        set_win.configure(bg="#102A43")
        set_win.resizable(False,False)

        tk.Label(set_win, text="设备IP地址", font=("微软雅黑",10), fg="white", bg="#102A43").pack(pady=5)
        ip_entry = tk.Entry(set_win, font=("微软雅黑",12), width=25)
        ip_entry.pack()
        ip_entry.insert(0, self.ip)

        tk.Label(set_win, text="通信密钥", font=("微软雅黑",10), fg="white", bg="#102A43").pack(pady=5)
        key_entry = tk.Entry(set_win, font=("微软雅黑",12), width=25)
        key_entry.pack()
        key_entry.insert(0, self.key)

        def save():
            self.ip = ip_entry.get().strip()
            self.key = key_entry.get().strip()
            messagebox.showinfo("成功", "配置已保存")
            self.log(f"已切换设备IP：{self.ip}")
            set_win.destroy()

        tk.Button(set_win, text="保存配置", font=("微软雅黑",10),
                  bg="#2563EB", fg="white", command=save).pack(pady=10)
    def manual_refresh(self):
        self.log("手动刷新设备状态...")
        self.update_device_info()

    def update_device_info(self):
        threading.Thread(target=self._get_status, daemon=True).start()

    def _get_status(self):
        try:
            r = requests.get(f"http://{self.ip}/status.php?key={self.key}", timeout=5)
            txt = r.text.strip()
            self.sta_text.config(text=txt)
        except:
            self.sta_text.config(text="无法连接设备")
    def start_scan(self):
        if self.scanning:
            return
        self.scanning = True
        self.wifi_list.delete(0, tk.END)
        self.log("开始扫描WiFi...")
        threading.Thread(target=self._scan_task, daemon=True).start()

    def _scan_task(self):
        try:
            r = requests.get(f"http://{self.ip}/scan.php?key={self.key}", timeout=12)
            lines = [i.strip() for i in r.text.splitlines() if i.strip()]
            for line in lines:
                self.wifi_list.insert(tk.END, line)
            self.log(f"扫描完成：{len(lines)} 个WiFi")
        except Exception as e:
            self.log(f"扫描失败：{str(e)}")
        self.scanning = False
    def try_connect(self, event):
        try:
            ssid = self.wifi_list.get(self.wifi_list.curselection())
        except:
            messagebox.showwarning("提示","请选择一个WiFi")
            return

        pwd = simpledialog.askstring("连接WiFi", f"连接：{ssid}\n输入密码：", show="*")
        if not pwd:
            return

        self.log(f"尝试连接：{ssid}")
        threading.Thread(target=self._connect_task, args=(ssid, pwd), daemon=True).start()

    def _connect_task(self, ssid, pwd):
        try:
            url = f"http://{self.ip}/connect.php"
            params = {"key":self.key, "ssid":ssid, "pwd":pwd}
            r = requests.get(url, params=params, timeout=20)
            res = r.text.strip()

            if "成功" in res:
                self.log(f"✅ 连接成功：{ssid}")
                self.update_device_info()
            else:
                self.log(f"❌ 连接失败：密码错误或无法连接")
        except Exception as e:
            self.log(f"❌ 连接异常：{str(e)}")
	#by xiaolu 20260417

if __name__ == "__main__":
    root = tk.Tk()
    app = WifiControlApp(root)
    root.mainloop()