# main.py — Desktop GUI (Tkinter) — PO Analyzer (يتصل بـ Hugging Face Space)
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from gradio_client import Client
import os, sys, shutil
import gradio_client

# إصلاح مشكلة types.json مع PyInstaller
def ensure_types_json():
    try:
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        src = os.path.join(os.path.dirname(gradio_client.__file__), "types.json")
        dst = os.path.join(base_path, "gradio_client", "types.json")
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        if not os.path.exists(dst):
            shutil.copy(src, dst)
    except Exception as e:
        print("Warning: could not ensure types.json", e)

ensure_types_json()

# عدّل هذا حسب اسم المستخدم واسم المساحة بالضبط:
# الصيغة: https://<username>-<space-name>.hf.space
SPACE_URL = "https://charihanekemmache14723-pocket-option-analyzer.hf.space"

# إنشاء عميل Gradio
client = Client(SPACE_URL)

def send_image_to_api(image_path):
    try:
        # predict endpoint: "/predict" (Gradio standard for Interface)
        result = client.predict(image_path, api_name="/predict")
        # result هو ما أرجعه الـ app.py؛ في الكود أعلاه نرجع (text, image)
        # gradio_client يعيد قيم مراعية: هنا نتعامل مع النص فقط لأننا نعرض الصورة محليًا إن لزم
        # إذا result هو قائمة/tuple: نحوله لنص واضح
        if isinstance(result, (list, tuple)):
            # حالة: [text, image] or similar
            text = result[0] if len(result) > 0 else str(result)
            return 200, str(text), result[1] if len(result) > 1 else None
        else:
            return 200, str(result), None
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

    code, text, preview = send_image_to_api(img_path)
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

    # إذا رجع preview (numpy array) نحولها ونفتحها في نافذة منفصلة
    try:
        if preview is not None:
            # preview may be PIL Image or numpy array; gradio_client sometimes returns a PIL image path/array
            from PIL import Image
            if isinstance(preview, (bytes, bytearray)):
                im = Image.open(io.BytesIO(preview))
                im.show()
            else:
                # try to open via Gradio client if it's a temp path or array
                # simplest: open the preview via PIL if possible
                preview_img = preview
                # if it's a list/tuple maybe base64 — skip complex conversions for now
                # Fallback: open original image
                Image.open(img_path).show()
    except Exception:
        pass

# UI
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
