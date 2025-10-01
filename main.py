import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import requests
import io

# === عدّل هذا بالرابط الصحيح لمساحتك على HuggingFace (بدون "/" في النهاية) ===
SPACE_URL = "https://charihanekemmache14723-pocket-option-analyzer-api.hf.space"

API_ENDPOINT = SPACE_URL + "/run/predict"  # مسار الواجهة الافتراضي في Gradio

def send_image_to_api(image_path):
    try:
        with open(image_path, "rb") as f:
            files = {"data": f}  # بعض النسخ تستخدم "data"، وإذا لم تعمل سنجرب "file" تلقائياً
            response = requests.post(API_ENDPOINT, files=files, timeout=30)

        if response.status_code != 200:
            # جرب صيغة أخرى للملف
            with open(image_path, "rb") as f:
                files = {"file": f}
                response = requests.post(API_ENDPOINT, files=files, timeout=30)

        return response.status_code, response.text, response.content

    except Exception as e:
        return None, f"❌ Connection error: {e}", None


def select_image():
        global img_path, img_display
        path = filedialog.askopenfilename(filetypes=[("Images", "*.png;*.jpg;*.jpeg")])
        if not path:
            return
        img_path = path
        img = Image.open(path)
        img.thumbnail((420, 320))
        img_display = ImageTk.PhotoImage(img)
        img_label.config(image=img_display)
        status_label.config(text="✅ صورة جاهزة")


def analyze_image():
    if not img_path:
        messagebox.showwarning("Warning", "اختر صورة أولاً")
        return
    status_label.config(text="⏳ جاري الإرسال...")
    root.update_idletasks()

    code, text, raw = send_image_to_api(img_path)
    if code is None:
        result_label.config(text=text, fg="red")
        status_label.config(text="❌ فشل الاتصال")
        return
    if code != 200:
        result_label.config(text=f"HTTP {code} — {text}", fg="red")
        status_label.config(text="❌ رد غير متوقع")
        return

    # عرض النص مع ألوان ورموز
    up = text.upper()
    if "CALL" in up:
        result_label.config(text=text, fg="green")
    elif "PUT" in up:
        result_label.config(text=text, fg="red")
    else:
        result_label.config(text=text, fg="gray")

    status_label.config(text="✅ التحليل مكتمل")


# === واجهة المستخدم ===
root = tk.Tk()
root.title("PO Analyzer")
root.geometry("560x560")
root.resizable(False, False)

img_path = None
img_display = None

tk.Button(root, text="📁 اختر صورة", width=22, command=select_image).pack(pady=12)
tk.Button(root, text="🔍 تحليل الصورة", width=22, command=analyze_image).pack(pady=6)

img_label = tk.Label(root, bd=2, relief="sunken", width=440, height=340)
img_label.pack(padx=10, pady=10)

result_label = tk.Label(root, text="", font=("Arial", 18, "bold"))
result_label.pack(pady=8)

status_label = tk.Label(root, text="🟢 جاهز", anchor="w")
status_label.pack(fill="x", padx=10, pady=6)

root.mainloop()
