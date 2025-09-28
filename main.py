import tkinter as tk
from tkinter import filedialog
import requests
import json
from PIL import Image, ImageTk
from io import BytesIO

# ==============================
# إعداد رابط الـ API الخاص بـ Hugging Face
# ==============================
API_URL = "https://charihanekemmache14723-pocket-option-analyzer-api.hf.space/api/predict/"

def send_image_to_api(image_path):
    """
    يرسل الصورة إلى API ويعيد الاستجابة على شكل JSON
    """
    try:
        with open(image_path, "rb") as img_file:
            response = requests.post(API_URL, files={"files": img_file})
        
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"HTTP {response.status_code}", "details": response.text}
    except Exception as e:
        return {"error": str(e)}

# ==============================
# واجهة المستخدم
# ==============================
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

    status_label.config(text="⏳ جاري إرسال الصورة إلى السيرفر...")
    root.update()

    result = send_image_to_api(img_path)

    if "error" in result:
        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, f"❌ خطأ: {result['error']}\n{result.get('details', '')}")
    else:
        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, json.dumps(result, indent=4, ensure_ascii=False))
        status_label.config(text="✅ التحليل مكتمل")

# ==============================
# تصميم الواجهة
# ==============================
root = tk.Tk()
root.title("Pocket Option Analyzer (Online)")

img_path = None

tk.Button(root, text="📁 اختر صورة", command=select_image).pack(pady=10)
tk.Button(root, text="🔍 تحليل الصورة", command=analyze_image).pack(pady=10)

img_label = tk.Label(root)
img_label.pack()

result_text = tk.Text(root, height=15, width=50)
result_text.pack()

status_label = tk.Label(root, text="🟢 جاهز")
status_label.pack()

root.mainloop()
