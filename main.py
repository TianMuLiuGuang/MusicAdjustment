import tkinter as tk
from tkinter import ttk, scrolledtext

class LyricsAdjuster:
    def __init__(self, root):
        self.root = root
        self.root.title("🎵 歌词调整工具")
        self.root.geometry("1200x720")
        self.root.configure(bg="#8acdd2")
        self.left_placeholder = "粘贴或输入歌词原文（每行一句）"
        self.right_placeholder = "粘贴或输入歌词译文（每行一句）"

        # 设置样式
        self.setup_styles()

        # 创建主布局
        self.create_widgets()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")

        # 自定义按钮样式
        style.configure("Clip.TButton",
                        font=("Segoe UI", 13, "bold"),
                        padding=(16, 8),
                        borderwidth=0,
                        background="#6c757d",
                        foreground="white")
        style.map("Clip.TButton",
                  background=[("active", "#5a6268"), ("pressed", "#495057")])
        
        style.configure("Action.TButton",
                        font=("Segoe UI", 13, "bold"),
                        padding=(16, 8),
                        borderwidth=0,
                        focusthickness=0,
                        background="#4a90d9",
                        foreground="white")
        style.map("Action.TButton",
                  background=[("active", "#357abd"), ("pressed", "#2a5f8a")])

        style.configure("Merge.TButton",
                        font=("Segoe UI", 13, "bold"),
                        padding=(16, 8),
                        borderwidth=0,
                        background="#27ae60",
                        foreground="white")
        style.map("Merge.TButton",
                  background=[("active", "#1e8449"), ("pressed", "#145a32")])

        style.configure("Card.TFrame",relief="solid", borderwidth=1)
        
    def create_widgets(self):
        # 主容器
        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # 水平分割：使用PanedWindow
        paned = ttk.PanedWindow(main_frame, orient=tk.HORIZONTAL)
        paned.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        # 左侧原文框
        left_frame = ttk.Frame(paned, relief=tk.SOLID, borderwidth=2,style="Card.TFrame")
        paned.add(left_frame, weight=1)

        self.left_text = scrolledtext.ScrolledText(
            left_frame,
            font=("Consolas", 12),
            wrap=tk.WORD,
            bg="#f8fafc",
            fg="#94a3b8",
            relief=tk.FLAT,
            highlightthickness=2,
            highlightcolor="#4a90d9",
            highlightbackground="#4a90d9"
        )
        self.left_text.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        self.left_text.insert("1.0", self.left_placeholder)
        self.left_text.bind("<FocusIn>", lambda e: self.clear_placeholder(self.left_text, self.left_placeholder))
        self.left_text.bind("<FocusOut>", lambda e: self.restore_placeholder(self.left_text, self.left_placeholder))

        # 右侧翻译框
        right_frame = ttk.Frame(paned, relief=tk.SOLID, borderwidth=2, style="Card.TFrame")
        paned.add(right_frame, weight=1)

        self.right_text = scrolledtext.ScrolledText(
            right_frame,
            font=("Consolas", 12),
            wrap=tk.WORD,
            bg="#f0fff4",
            fg="#94a3b8",
            relief=tk.FLAT,
            highlightthickness=2,
            highlightcolor="#27ae60",
            highlightbackground="#27ae60"
        )
        self.right_text.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        self.right_text.insert("1.0", self.right_placeholder)
        self.right_text.bind("<FocusIn>", lambda e: self.clear_placeholder(self.right_text, self.right_placeholder))
        self.right_text.bind("<FocusOut>", lambda e: self.restore_placeholder(self.right_text, self.right_placeholder))

        # IO按钮
        btn_paste1 = ttk.Button(
            left_frame,
            text="📥 粘贴原文",
            style="Clip.TButton",
            command=lambda: self.paste_text(self.left_text)
        )
        btn_paste1.pack(side=tk.LEFT, padx=5)
        btn_copy = ttk.Button(
            left_frame,
            text="📋 复制原文",
            style="Clip.TButton",
            command=self.copy_text
        )
        btn_copy.pack(side=tk.LEFT, padx=5)

        btn_paste2 = ttk.Button(
            right_frame,
            text="📥 粘贴译文",
            style="Clip.TButton",
            command=lambda: self.paste_text(self.right_text)
        )
        btn_paste2.pack(side=tk.LEFT, padx=5)

        # 四个按钮
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=5)

        # 内层居中容器（不填充，只放按钮）
        center_frame = ttk.Frame(btn_frame)
        center_frame.pack(anchor='center')

        btn_time = ttk.Button(
            center_frame, text="⏱ 时间精度调整",
            style="Action.TButton",
            command=self.adjust_time_precision
        )
        btn_time.pack(side=tk.LEFT, padx=5)

        btn_empty = ttk.Button(
            center_frame, text="🗑 去除空行",
            style="Action.TButton",
            command=self.remove_empty_lines
        )
        btn_empty.pack(side=tk.LEFT, padx=5)

        btn_wrong = ttk.Button(
            center_frame, text="↕ 错行调整",
            style="Action.TButton",
            command=self.adjust_wrong_lines
        )
        btn_wrong.pack(side=tk.LEFT, padx=5)

        btn_merge = ttk.Button(
            center_frame, text="🔗 合并原文和译文",
            style="Merge.TButton",
            command=self.merge_translation
        )
        btn_merge.pack(side=tk.RIGHT, padx=5)

        self.root.update()

    # ---------- 占位符处理（模拟placeholder） ----------
    def clear_placeholder(self, widget, placeholder):
        if widget.get("1.0", "end-1c") == placeholder:
            widget.delete("1.0", tk.END)
            widget.configure(fg="#000000")

    def restore_placeholder(self, widget, placeholder):
        if not widget.get("1.0", "end-1c"):
            widget.insert("1.0", placeholder)
            widget.configure(fg="#94a3b8")

    # --------------- 功能方法 ---------------
    def copy_text(self):
        """将左侧处理框的内容复制到系统剪贴板"""
        content = self.left_text.get("1.0", tk.END).strip()
        if content == self.left_placeholder:
            return
        self.root.clipboard_clear()
        self.root.clipboard_append(content)

    def paste_text(self, widget):
        """将系统剪贴板的内容覆盖式粘贴到指定的文本框"""
        try:
            clipboard_content = self.root.clipboard_get()
        except tk.TclError:
            return
        widget.delete("1.0", tk.END)
        widget.insert("1.0", clipboard_content)
        widget.configure(fg="#000000")

    def adjust_time_precision(self):
        """时间精度调整"""
        text = self.left_text.get("1.0", tk.END).strip()
        if text == self.left_placeholder :
            return

        lyric_lines = text.splitlines(True)
        lyric_lines[-1] += "\n"
        time_end = lyric_lines[0].find(']')
        min_length = time_end + 2

        if time_end <= 9:
            return
        
        processed_text=""
        for line in lyric_lines:
            if len(line) <= min_length:
                continue
            processed_text += line[:9] + line[time_end:]
        self.left_text.delete("1.0", tk.END)
        self.left_text.insert("1.0", processed_text.strip())

    def remove_empty_lines(self):
        """去除空行"""
        text = self.left_text.get("1.0", tk.END).strip()
        if text==self.left_placeholder :
            return

        lyric_lines = text.splitlines(True)
        lyric_lines[-1] += "\n"
        min_length = lyric_lines[0].find(']') + 2
        if min_length < 11: 
            return

        processed_text = ""
        for line in lyric_lines:
            if len(line) <= min_length:
                continue
            processed_text += line

        self.left_text.delete("1.0", tk.END)
        self.left_text.insert("1.0", processed_text.strip())

    def adjust_wrong_lines(self):
        """错行调整"""
        text = self.left_text.get("1.0", tk.END).strip()
        if text == self.left_placeholder :
            return

        lyric_lines = text.splitlines(True)
        lyric_lines[-1] += "\n"
        min_length = len(lyric_lines[0])
        time_end = lyric_lines[0].find(']')
        if time_end +2 != min_length: 
            return

        processed_text=""
        for i in range(1,len(lyric_lines)):
            if len(lyric_lines[i]) <= min_length:
                continue
            processed_text += lyric_lines[i-1][:9] + lyric_lines[i][time_end:]
        self.left_text.delete("1.0", tk.END)
        self.left_text.insert("1.0", processed_text.strip())

    def merge_translation(self):
        """合并翻译：将右侧翻译逐行插入到左侧原文的下一行"""
        left_text = self.left_text.get("1.0", tk.END).strip()
        right_text = self.right_text.get("1.0", tk.END).strip()
        if left_text==self.left_placeholder or right_text==self.right_placeholder:
            return
        
        left_lines = left_text.splitlines(True)
        left_lines[-1] += "\n"
        right_lines = right_text.splitlines(True)
        if len(left_lines) != len(right_lines): 
            return

        result=""
        for i in range(len(left_lines)):
            result += left_lines[i]
            result += right_lines[i]

        self.left_text.delete("1.0", tk.END)
        self.left_text.insert("1.0", result)

if __name__ == "__main__":
    root = tk.Tk()
    app = LyricsAdjuster(root)
    root.mainloop()
