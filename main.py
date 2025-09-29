import tkinter as tk
from tkinter import filedialog
import requests
from PIL import Image, ImageTk
from io import BytesIO

API_URL = "https://charihanekemmache14723-pocket-option-ai.hf.space/run/predict"

def send_image_to_api(image_path):
    try:
        with open(image_path, "rb") as img_file:
            response = requests.post(API_URL, files={"files": img_file})
        return response.text  # لأنها نص عادي وليست JSON
    except Exception as e:
        return f"❌ خطأ في الاتصال بالسيرفر: {str(e)}"

def select_image():
        global img_path, img_display
        img_path = filedialog.askopenfilename(filetypes=[("Images", "*.png;*.jpg;*.jpeg")])
        if img_path:
            img = Image.open(img_path)
            img = img.resize((300, 200))
            img_display = ImageTk.PhotoImage(img)
            img_label.config(image=img_display)
            status_label.config(text="✅ صورة جاهزة للتحليل")

def analyze_image():
    if not img_path:
        status_label.config(text="❌ الرجاء اختيار صورة أولاً")
        return

    status_label.config(text="⏳ جاري تحليل الصورة...")
    root.update()

    result = send_image_to_api(img_path)

    # تحديد اللون بناءً على النتيجة
    if "CALL" in result.upper():
        result_text.config(fg="green")
    elif "PUT" in result.upper():
        result_text.config(fg="red")
    else:
        result_text.config(fg="gray")

    result_text.config(text=result.strip())

# تصميم الواجهة
root = tk.Tk()
root.title("Pocket Option Analyzer (Online)")

img_path = None

tk.Button(root, text="📁 اختر صورة", command=select_image).pack(pady=10)
tk.Button(root, text="🔍 تحليل الصورة", command=analyze_image).pack(pady=10)

img_label = tk.Label(root)
img_label.pack()

result_text = tk.Label(root, text="", font=("Arial", 18, "bold"))
result_text.pack(pady=10)

status_label = tk.Label(root, text="🟢 جاهز")
status_label.pack()

root.mainloop()

