import tkinter as tk
from tkinter import filedialog
import requests
import json
from PIL import Image, ImageTk
from io import BytesIO

# ==============================
# رابط الـ API (Hugging Face Space)
# ==============================
API_URL = "https://charihanekemmache14723-pocket-option-ai.hf.space/api/predict/"

def send_image_to_api(image_path):
    """يرسل الصورة إلى API ويستقبل JSON + صورة تحليلية"""
    try:
        with open(image_path, "rb") as img_file:
            response = requests.post(API_URL, files={"files": img_file})
        
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"HTTP {response.status_code}", "details": response.text}
    except Exception as e:
        return {"error": str(e)}

def select_image():
    """اختيار صورة من الجهاز"""
    global img_path, img_display
    img_path = filedialog.askopenfilename(filetypes=[("Images", "*.png;*.jpg;*.jpeg")])
    if img_path:
        img = Image.open(img_path)
        img = img.resize((300, 200))
        img_display = ImageTk.PhotoImage(img)
        img_label.config(image=img_display)
        status_label.config(text="✅ صورة جاهزة للتحليل")

def analyze_image():
    """إرسال الصورة إلى السيرفر وعرض النتيجة"""
    if not img_path:
        status_label.config(text="❌ الرجاء اختيار صورة أولاً")
        return

    status_label.config(text="⏳ جاري إرسال الصورة للسيرفر...")
    root.update()

    result = send_image_to_api(img_path)

    if "error" in result:
        result_text.config(fg="red")
        result_text.config(text=f"❌ خطأ: {result['error']}\n{result.get('details', '')}")
        return

    # جلب نوع الإشارة والثقة
    signal = result[0].get("signal_type", "UNKNOWN")
    confidence = result[0].get("confidence", 0)

    # تحديد اللون حسب الإشارة
    if signal == "CALL":
        result_text.config(fg="green")
        result_text.config(text=f"🟢 CALL ({confidence*100:.0f}% Confidence)")
    elif signal == "PUT":
        result_text.config(fg="red")
        result_text.config(text=f"🔴 PUT ({confidence*100:.0f}% Confidence)")
    else:
        result_text.config(fg="gray")
        result_text.config(text=f"⚪ NO_TRADE")

    status_label.config(text="✅ التحليل مكتمل")

    # عرض الصورة التحليلية في نافذة منفصلة
    if len(result) > 1:
        try:
            processed_img_data = result[1]
            img = Image.fromarray(processed_img_data)
            img.show()  # تفتح الصورة في نافذة مستقلة
        except:
            pass

# ==============================
# تصميم واجهة البرنامج
# ==============================
root = tk.Tk()
root.title("Pocket Option Analyzer (Online)")

img_path = None

tk.Button(root, text="📁 اختر صورة", command=select_image).pack(pady=10)
tk.Button(root, text="🔍 تحليل الصورة", command=analyze_image).pack(pady=10)

img_label = tk.Label(root)
img_label.pack()

result_text = tk.Label(root, text="", font=("Arial", 16))
result_text.pack(pady=10)

status_label = tk.Label(root, text="🟢 جاهز")
status_label.pack()

root.mainloop()
