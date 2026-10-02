
import sqlite3
from datetime import datetime, date
from pathlib import Path

from kivy.app import App
from kivy.lang import Builder
from kivy.properties import StringProperty, NumericProperty
from kivy.uix.screenmanager import Screen
from kivy.metrics import dp
from kivy.utils import get_color_from_hex

DB_PATH = Path(App.user_data_dir) / "finance.db"

KV = r"""
#:import hex kivy.utils.get_color_from_hex

<NavButton@Button>:
    background_normal: ""
    background_color: 0,0,0,0
    color: hex("#AEB8D0")
    font_size: "12sp"

<DashboardCard@BoxLayout>:
    orientation: "vertical"
    padding: dp(16)
    spacing: dp(4)
    canvas.before:
        Color:
            rgba: hex("#182033")
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [dp(18),]

<Root>:
    orientation: "vertical"
    canvas.before:
        Color:
            rgba: hex("#0B1020")
        Rectangle:
            pos: self.pos
            size: self.size

    ScreenManager:
        id: sm

        Screen:
            name: "home"
            BoxLayout:
                orientation: "vertical"
                padding: dp(18)
                spacing: dp(14)

                BoxLayout:
                    size_hint_y: None
                    height: dp(55)
                    Label:
                        text: "مدیریت مالی"
                        color: hex("#F5F7FF")
                        font_size: "25sp"
                        bold: True
                        halign: "right"
                        text_size: self.size
                    Label:
                        text: "گزارش مالی شخصی"
                        color: hex("#8994AD")
                        font_size: "12sp"
                        halign: "left"
                        valign: "middle"
                        text_size: self.size

                BoxLayout:
                    size_hint_y: None
                    height: dp(135)
                    spacing: dp(10)
                    DashboardCard:
                        Label:
                            text: "هزینه این ماه"
                            color: hex("#8F9AB5")
                            font_size: "13sp"
                            halign: "right"
                            text_size: self.size
                        Label:
                            text: root.month_total
                            color: hex("#FFFFFF")
                            font_size: "23sp"
                            bold: True
                            halign: "right"
                            text_size: self.size
                        Label:
                            text: "تومان"
                            color: hex("#5FD6B3")
                            font_size: "12sp"
                            halign: "right"
                            text_size: self.size
                    DashboardCard:
                        Label:
                            text: "امروز"
                            color: hex("#8F9AB5")
                            font_size: "13sp"
                            halign: "right"
                            text_size: self.size
                        Label:
                            text: root.today_total
                            color: hex("#FFFFFF")
                            font_size: "23sp"
                            bold: True
                            halign: "right"
                            text_size: self.size
                        Label:
                            text: "تومان"
                            color: hex("#F0B35A")
                            font_size: "12sp"
                            halign: "right"
                            text_size: self.size

                BoxLayout:
                    orientation: "vertical"
                    padding: dp(18)
                    spacing: dp(8)
                    canvas.before:
                        Color:
                            rgba: hex("#12192A")
                        RoundedRectangle:
                            pos: self.pos
                            size: self.size
                            radius: [dp(20),]
                    Label:
                        text: "تحلیل سریع"
                        color: hex("#FFFFFF")
                        font_size: "18sp"
                        bold: True
                        halign: "right"
                        text_size: self.size
                    Label:
                        text: root.insight
                        color: hex("#B9C3D9")
                        font_size: "13sp"
                        halign: "right"
                        valign: "top"
                        text_size: self.size

                Button:
                    text: "+  ثبت هزینه جدید"
                    size_hint_y: None
                    height: dp(58)
                    background_normal: ""
                    background_color: hex("#5FD6B3")
                    color: hex("#07121A")
                    font_size: "16sp"
                    bold: True
                    on_release: root.go_add()

                Widget:

        Screen:
            name: "add"
            BoxLayout:
                orientation: "vertical"
                padding: dp(20)
                spacing: dp(14)
                Label:
                    text: "ثبت هزینه"
                    size_hint_y: None
                    height: dp(55)
                    color: hex("#FFFFFF")
                    font_size: "25sp"
                    bold: True
                    halign: "right"
                    text_size: self.size
                TextInput:
                    id: amount
                    hint_text: "مبلغ به تومان"
                    input_filter: "int"
                    multiline: False
                    size_hint_y: None
                    height: dp(55)
                    font_size: "16sp"
                    halign: "right"
                TextInput:
                    id: category
                    hint_text: "دسته‌بندی؛ مثال: غذا"
                    multiline: False
                    size_hint_y: None
                    height: dp(55)
                    font_size: "16sp"
                    halign: "right"
                TextInput:
                    id: note
                    hint_text: "توضیح هزینه"
                    multiline: False
                    size_hint_y: None
                    height: dp(55)
                    font_size: "16sp"
                    halign: "right"
                Label:
                    id: add_status
                    text: ""
                    color: hex("#F0B35A")
                    size_hint_y: None
                    height: dp(35)
                    halign: "right"
                    text_size: self.size
                Button:
                    text: "ذخیره هزینه"
                    size_hint_y: None
                    height: dp(58)
                    background_normal: ""
                    background_color: hex("#5FD6B3")
                    color: hex("#07121A")
                    font_size: "16sp"
                    bold: True
                    on_release: root.save_expense(amount.text, category.text, note.text)
                Button:
                    text: "بازگشت"
                    size_hint_y: None
                    height: dp(48)
                    background_normal: ""
                    background_color: hex("#182033")
                    color: hex("#DCE4F5")
                    on_release: root.go_home()
                Widget:

        Screen:
            name: "reports"
            BoxLayout:
                orientation: "vertical"
                padding: dp(18)
                spacing: dp(12)
                Label:
                    text: "گزارش مالی"
                    size_hint_y: None
                    height: dp(55)
                    color: hex("#FFFFFF")
                    font_size: "25sp"
                    bold: True
                    halign: "right"
                    text_size: self.size
                Label:
                    text: root.report_text
                    color: hex("#C4CEE2")
                    font_size: "14sp"
                    halign: "right"
                    valign: "top"
                    text_size: self.size
                Button:
                    text: "به‌روزرسانی گزارش"
                    size_hint_y: None
                    height: dp(52)
                    background_normal: ""
                    background_color: hex("#182033")
                    color: hex("#FFFFFF")
                    on_release: root.refresh()
                Widget:

    BoxLayout:
        size_hint_y: None
        height: dp(72)
        padding: dp(8)
        spacing: dp(6)
        canvas.before:
            Color:
                rgba: hex("#111827")
            Rectangle:
                pos: self.pos
                size: self.size
        NavButton:
            text: "خانه"
            on_release: root.go_home()
        NavButton:
            text: "ثبت هزینه"
            on_release: root.go_add()
        NavButton:
            text: "گزارش"
            on_release: root.go_reports()
"""

class Root(Screen):
    month_total = StringProperty("0")
    today_total = StringProperty("0")
    insight = StringProperty("هنوز هزینه‌ای ثبت نشده است.")
    report_text = StringProperty("هنوز داده‌ای برای گزارش وجود ندارد.")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.init_db()
        self.refresh()

    def init_db(self):
        DB_PATH.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(DB_PATH) as c:
            c.execute("""
                CREATE TABLE IF NOT EXISTS expenses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    amount INTEGER NOT NULL,
                    category TEXT NOT NULL,
                    note TEXT,
                    expense_date TEXT NOT NULL
                )
            """)
            c.execute("""
                CREATE TABLE IF NOT EXISTS budgets (
                    id INTEGER PRIMARY KEY,
                    monthly_budget INTEGER NOT NULL DEFAULT 0
                )
            """)
            c.execute("INSERT OR IGNORE INTO budgets(id, monthly_budget) VALUES(1, 0)")

    def money(self, n):
        return f"{int(n):,}"

    def refresh(self):
        now = datetime.now()
        month = now.strftime("%Y-%m")
        today = now.strftime("%Y-%m-%d")
        with sqlite3.connect(DB_PATH) as c:
            mt = c.execute(
                "SELECT COALESCE(SUM(amount),0) FROM expenses WHERE substr(expense_date,1,7)=?",
                (month,)
            ).fetchone()[0]
            tt = c.execute(
                "SELECT COALESCE(SUM(amount),0) FROM expenses WHERE expense_date=?",
                (today,)
            ).fetchone()[0]
            rows = c.execute("""
                SELECT category, SUM(amount) total
                FROM expenses
                WHERE substr(expense_date,1,7)=?
                GROUP BY category ORDER BY total DESC
            """, (month,)).fetchall()
        self.month_total = self.money(mt)
        self.today_total = self.money(tt)
        if rows:
            top_cat, top_val = rows[0]
            self.insight = f"بیشترین هزینه این ماه: {top_cat} با {self.money(top_val)} تومان.\n" \
                           f"تعداد دسته‌های فعال: {len(rows)}\n" \
                           f"پیشنهاد: برای کاهش هزینه، ابتدا همین دسته را بررسی کن."
        else:
            self.insight = "هنوز هزینه‌ای ثبت نشده است.\nاولین هزینه‌ات را ثبت کن تا تحلیل مالی شروع شود."
        self.make_report(rows, mt)

    def make_report(self, rows, mt):
        if not rows:
            self.report_text = "برای نمایش گزارش، حداقل یک هزینه ثبت کن."
            return
        lines = [f"مجموع هزینه این ماه: {self.money(mt)} تومان", "", "هزینه بر اساس دسته:"]
        for cat, val in rows:
            pct = (val / mt * 100) if mt else 0
            lines.append(f"• {cat}: {self.money(val)} تومان  —  {pct:.1f}%")
        if rows:
            lines += ["", "تحلیل:", f"• تمرکز اصلی هزینه روی «{rows[0][0]}» است.",
                      "• اگر می‌خواهی هزینه‌ها کمتر شود، سقف ماهانه برای دسته‌های پرهزینه تعیین کن.",
                      "• در نسخه بعدی، روند ماه‌به‌ماه و پیشنهاد هوشمند اضافه می‌شود."]
        self.report_text = "\n".join(lines)

    def save_expense(self, amount, category, note):
        screen = self.manager.get_screen("add")
        try:
            value = int(amount.replace(",", "").strip())
        except:
            screen.ids.add_status.text = "مبلغ را به صورت عدد وارد کن."
            return
        category = category.strip()
        if value <= 0 or not category:
            screen.ids.add_status.text = "مبلغ و دسته‌بندی الزامی است."
            return
        with sqlite3.connect(DB_PATH) as c:
            c.execute(
                "INSERT INTO expenses(amount,category,note,expense_date) VALUES(?,?,?,?)",
                (value, category, note.strip(), datetime.now().strftime("%Y-%m-%d"))
            )
        screen.ids.amount.text = ""
        screen.ids.category.text = ""
        screen.ids.note.text = ""
        screen.ids.add_status.text = "هزینه با موفقیت ثبت شد."
        self.refresh()

    def go_home(self):
        self.refresh()
        self.manager.current = "home"

    def go_add(self):
        self.manager.current = "add"

    def go_reports(self):
        self.refresh()
        self.manager.current = "reports"

class FinanceApp(App):
    title = "مدیریت مالی شخصی"

    def build(self):
        Builder.load_string(KV)
        return Root()

if __name__ == "__main__":
    FinanceApp().run()
