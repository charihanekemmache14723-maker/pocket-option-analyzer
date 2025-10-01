import tkinter as tk
from tkinter import filedialog, messagebox
import requests
from PIL import Image, ImageTk
from io import BytesIO

# --- عدّل هذا إلى رابط الـ Space الخاص بك إذا اختلف ---
API_URL = "https://charihanekemmache14723-pocket-option-ai.hf.space/run/predict"

def send_image_to_api(image_path):
    try:
        with open(image_path, "rb") as f:
            files = {"data": f}  # بعض إصدارات Gradio تقبل 'data' أو 'files' — نجرب 'data' أولاً
            r = requests.post(API_URL, files={"file": f}, timeout=30)
        # نعيد النص كما هو (API يرجع نص عادي)
        return r.status_code, r.text, r.content
    except Exception as e:
        return None, f"❌ خطأ في الاتصال: {e}", None

def select_image():
    global img_path, img_display
    path = filedialog.askopenfilename(filetypes=[("Images", "*.png;*.jpg;*.jpeg")])
    if not path:
        return
    img_path = path
    img = Image.open(path)
    img.thumbnail((400, 300))
    img_display = ImageTk.PhotoImage(img)
    img_label.config(image=img_display)
    status_label.config(text="✅ صورة جاهزة")

def analyze_image():
    if not img_path:
        messagebox.showwarning("تحذير", "اختر صورة أولاً")
        return
    status_label.config(text="⏳ جارٍ الإرسال...")
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

    # عرض النص الملون
    txt = text.strip()
    # ابحث عن كلمات CALL / PUT / NO_TRADE (حسّاسية غير مهمة)
    up = txt.upper()
    if "CALL" in up:
        result_label.config(text=txt, fg="green")
    elif "PUT" in up:
        result_label.config(text=txt, fg="red")
    else:
        result_label.config(text=txt, fg="gray")
    status_label.config(text="✅ التحليل مكتمل")

    # إن كان السيرفر أعاد صورة (وهي محتوى ثانٍ) حاول فتحها:
    # بعض Gradio returns image inside HTML/text — لكن إن أعاد السيرفر بايتس لصورة:
    try:
        # إذا كان المحتوى ثنائي (raw) ويشبه صورة صغيرة، نفتحها
        if raw and len(raw) > 100 and raw[:10].find(b'PNG') != -1 or raw[:3] == b'\xff\xd8\xff':
            im = Image.open(BytesIO(raw))
            im.show()
    except Exception:
        # لا مشكلة إن لم تنجح طريقة فتح الصورة — الرسالة النصية الأهم
        pass

# === واجهة المستخدم ===
root = tk.Tk()
root.title("PO Analyzer")
root.geometry("520x520")
root.resizable(False, False)

img_path = None
img_display = None

tk.Button(root, text="📁 اختر صورة", width=20, command=select_image).pack(pady=10)
tk.Button(root, text="🔍 تحليل الصورة", width=20, command=analyze_image).pack(pady=5)

img_label = tk.Label(root, bd=2, relief="sunken", width=400, height=300)
img_label.pack(padx=10, pady=10)

result_label = tk.Label(root, text="", font=("Arial", 16, "bold"))
result_label.pack(pady=8)

status_label = tk.Label(root, text="🟢 جاهز", anchor="w")
status_label.pack(fill="x", padx=10, pady=4)

root.mainloop()


