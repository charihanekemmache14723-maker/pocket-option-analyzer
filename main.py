import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
import json
from datetime import datetime

class PocketOptionAnalyzer:
    def __init__(self):
        self.signals = []

    def dummy_analysis(self, file_path):
        # هذه فقط محاكاة – لاحقاً ممكن نضيف التحليل الحقيقي
        self.signals = [
            {
                "signal_type": "CALL",
                "confidence": 0.82,
                "entry_price": 1.2345,
                "recommended_expiry": "5 دقائق",
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }
        ]
        return True


class PocketOptionGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Pocket Option Analyzer")
        self.root.geometry("700x500")
        self.analyzer = PocketOptionAnalyzer()
        self.create_widgets()

    def create_widgets(self):
        frame = tk.Frame(self.root)
        frame.pack(pady=10)

        upload_btn = tk.Button(frame, text="📁 اختر صورة", command=self.load_image)
        upload_btn.pack(side="left", padx=5)

        analyze_btn = tk.Button(frame, text="🔍 تحليل", command=self.run_analysis)
        analyze_btn.pack(side="left", padx=5)

        save_btn = tk.Button(frame, text="💾 حفظ النتائج", command=self.save_results)
        save_btn.pack(side="left", padx=5)

        self.results_text = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, height=20)
        self.results_text.pack(fill="both", expand=True, padx=10, pady=10)

    def load_image(self):
        self.file_path = filedialog.askopenfilename(
            title="اختر صورة", filetypes=[("Image files", "*.png *.jpg *.jpeg")]
        )
        if self.file_path:
            messagebox.showinfo("تم", f"تم اختيار الصورة: {self.file_path}")

    def run_analysis(self):
        if not hasattr(self, "file_path"):
            messagebox.showwarning("تحذير", "اختر صورة أولاً")
            return
        if self.analyzer.dummy_analysis(self.file_path):
            self.display_results()

    def display_results(self):
        self.results_text.delete(1.0, tk.END)
        for signal in self.analyzer.signals:
            self.results_text.insert(tk.END, f"🚨 إشارة جديدة:\n")
            self.results_text.insert(tk.END, f"• النوع: {signal['signal_type']}\n")
            self.results_text.insert(tk.END, f"• الثقة: {signal['confidence']:.1%}\n")
            self.results_text.insert(tk.END, f"• سعر الدخول: {signal['entry_price']:.4f}\n")
            self.results_text.insert(tk.END, f"• المدة: {signal['recommended_expiry']}\n")
            self.results_text.insert(tk.END, f"• الوقت: {signal['timestamp']}\n\n")

    def save_results(self):
        if not self.analyzer.signals:
            messagebox.showwarning("تحذير", "لا توجد نتائج لحفظها")
            return
        filename = f"signals_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(self.analyzer.signals, f, ensure_ascii=False, indent=2)
        messagebox.showinfo("تم", f"تم حفظ النتائج في {filename}")

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    gui = PocketOptionGUI()
    gui.run()
