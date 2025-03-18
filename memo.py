# -*- coding: utf-8 -*-
import sys
import json
import csv
import platform
import winreg
from datetime import datetime, date, timedelta
from PyQt5.QtCore import Qt, QDate, QTimer, QSettings, QPoint, QSize, pyqtSignal
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem,
                             QDialog, QLabel, QSlider, QCheckBox, QColorDialog,
                             QFileDialog, QComboBox, QHeaderView, QMenu, QAction, QGridLayout)
from PyQt5.QtGui import QColor, QFont

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QIcon

class DesktopMemoApp(QMainWindow):
    def __init__(self):
        super().__init__()
        # 必须设置应用ID（Windows任务栏图标需要）
        if sys.platform == 'win32':
            import ctypes
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("DesktopMemo.1.0")
        
        # 设置窗口图标
        self.setWindowIcon(QIcon(":/app.ico"))  # 从资源文件加载

    ...
SETTINGS_FILE = "config.ini"
MEMOS_FILE = "memos.json"

class ModernCalendar(QWidget):
    dateChanged = pyqtSignal(QDate)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.current_date = QDate.currentDate()
        self.selected_date = self.current_date
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # 导航栏布局
        nav_layout = QHBoxLayout()
        nav_layout.setContentsMargins(10, 0, 10, 0)
        self.prev_btn = QPushButton("‹")
        self.next_btn = QPushButton("›")
        self.month_label = QLabel()
        self.prev_btn.setFixedSize(40, 40)
        self.next_btn.setFixedSize(40, 40)
        nav_layout.addWidget(self.prev_btn)
        nav_layout.addStretch()
        nav_layout.addWidget(self.month_label)
        nav_layout.addStretch()
        nav_layout.addWidget(self.next_btn)
        
        # 星期标签布局
        week_layout = QHBoxLayout()
        week_layout.setSpacing(0)
        weeks = ["一", "二", "三", "四", "五", "六", "日"]
        for week in weeks:
            label = QLabel(week)
            label.setAlignment(Qt.AlignCenter)
            label.setStyleSheet("font-weight: bold;")
            week_layout.addWidget(label)
            
        # 日历网格布局
        self.days_grid = QGridLayout()
        self.days_grid.setSpacing(12)
        self.days = []
        for i in range(42):
            day = QPushButton()
            day.setFixedSize(50, 50)
            day.setStyleSheet("""
                QPushButton {
                    background: transparent;
                    border-radius: 25px;
                    font-size: 16px;
                    color: #666;
                }
                QPushButton:hover { background: rgba(0,0,0,0.05); }
            """)
            day.clicked.connect(lambda _, x=i: self.select_day(x))
            self.days.append(day)
            self.days_grid.addWidget(day, i//7, i%7)
            self.days_grid.setColumnStretch(i%7, 1)
        
        layout.addLayout(nav_layout)
        layout.addLayout(week_layout)
        layout.addLayout(self.days_grid)
        self.setLayout(layout)
        
        self.prev_btn.clicked.connect(self.prev_month)
        self.next_btn.clicked.connect(self.next_month)
        self.update_calendar()
        
    def update_calendar(self):
        self.month_label.setText(self.current_date.toString("yyyy年MM月"))
        first_day = self.current_date.addDays(-self.current_date.dayOfWeek() + 1)
        
        for i, day_btn in enumerate(self.days):
            day_date = first_day.addDays(i)
            day_btn.setText(str(day_date.day()))
            
            # 检查是否有备忘录
            has_memo = False
            date_str = day_date.toString("yyyy-MM-dd")
            if self.parent and date_str in self.parent.memos:
                has_memo = len(self.parent.memos[date_str]) > 0
            
            style = []
            if day_date.dayOfWeek() in [6, 7]:
                style.append("color: #8B0000;")
            
            if day_date == self.selected_date:
                style.append("background: #2196F3; color: white;")
            elif day_date.month() != self.current_date.month():
                style.append("color: #999;")
            if has_memo:
                style.append("font-weight: bold; border: 2px solid #FF5722;")
            if day_date == QDate.currentDate():
                style.append("border: 2px solid #4CAF50;")
                
            day_btn.setStyleSheet(f"""
                QPushButton {{
                    {' '.join(style)}
                    border-radius: 25px;
                }}
            """)
                
    def prev_month(self):
        self.current_date = self.current_date.addMonths(-1)
        self.update_calendar()
        
    def next_month(self):
        self.current_date = self.current_date.addMonths(1)
        self.update_calendar()
        
    def select_day(self, index):
        selected_day = self.current_date.addDays(-self.current_date.dayOfWeek() + 1).addDays(index)
        if selected_day.month() == self.current_date.month():
            self.selected_date = selected_day
            self.update_calendar()
            self.dateChanged.emit(self.selected_date)

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.settings = QSettings(SETTINGS_FILE, QSettings.IniFormat)
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)
        self.init_ui()
        self.load_settings()
        
    def init_ui(self):
        self.setWindowTitle("设置")
        self.setFixedSize(500, 650)
        self.setStyleSheet("""
            QDialog {
                background: rgba(245, 245, 245, 0.95);
                border-radius: 18px;
                border: 1px solid rgba(0,0,0,0.08);
                font-size: 16px;
            }
            QLabel {
                font-size: 16px;
                color: #333;
            }
            QPushButton {
                font-size: 16px;
                background: #2196F3;
                color: white;
                border-radius: 8px;
                padding: 8px;
            }
            QPushButton:hover {
                background: #1976D2;
            }
        """)
        
        self.startup_check = QCheckBox("开机自动启动")
        self.opacity_slider = QSlider(Qt.Horizontal)
        self.bg_color_btn = QPushButton("选择背景颜色")
        self.font_combo = QComboBox()
        self.font_size_slider = QSlider(Qt.Horizontal)
        self.font_color_btn = QPushButton("选择字体颜色")
        
        self.create_section("外观设置", [
            self.startup_check,
            self.create_row("透明度调节", self.opacity_slider),
            self.bg_color_btn,
        ])
        
        self.create_section("字体设置", [
            self.create_row("字体类型", self.font_combo),
            self.create_row("字体大小", self.font_size_slider),
            self.font_color_btn,
        ])
        
        btn_layout = QHBoxLayout()
        save_btn = QPushButton("保存设置")
        export_btn = QPushButton("导出数据")
        cancel_btn = QPushButton("取消")
        save_btn.setFixedSize(120, 40)
        export_btn.setFixedSize(120, 40)
        cancel_btn.setFixedSize(120, 40)
        btn_layout.addStretch()
        btn_layout.addWidget(save_btn)
        btn_layout.addWidget(export_btn)
        btn_layout.addWidget(cancel_btn)
        self.main_layout.addLayout(btn_layout)
        
        save_btn.clicked.connect(self.save_settings)
        export_btn.clicked.connect(self.parent.export_data)
        cancel_btn.clicked.connect(self.reject)
        self.bg_color_btn.clicked.connect(self.choose_bg_color)
        self.font_color_btn.clicked.connect(self.choose_font_color)
        
        self.font_combo.addItems(["Microsoft YaHei", "Arial", "Times New Roman", "宋体", "Segoe UI"])
        self.opacity_slider.setRange(30, 100)
        self.font_size_slider.setRange(14, 30)
        
    def create_section(self, title, widgets):
        section = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)
        title_label = QLabel(title)
        title_label.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: #333;
            border-bottom: 2px solid #eee;
            padding-bottom: 5px;
        """)
        layout.addWidget(title_label)
        for widget in widgets:
            layout.addWidget(widget)
        section.setLayout(layout)
        self.main_layout.addWidget(section)
        
    def create_row(self, label_text, control):
        row = QWidget()
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        label = QLabel(label_text)
        label.setFixedWidth(120)
        label.setStyleSheet("color: #666; font-size: 16px;")
        layout.addWidget(label)
        layout.addWidget(control)
        row.setLayout(layout)
        return row
    
    def load_settings(self):
        self.startup_check.setChecked(self.settings.value("startup", False, type=bool))
        self.opacity_slider.setValue(self.settings.value("opacity", 80, type=int))
        self.font_combo.setCurrentText(self.settings.value("font_family", "Microsoft YaHei", type=str))
        self.font_size_slider.setValue(self.settings.value("font_size", 18, type=int))
        
    def save_settings(self):
        self.settings.setValue("startup", self.startup_check.isChecked())
        self.settings.setValue("opacity", self.opacity_slider.value())
        self.settings.setValue("font_size", self.font_size_slider.value())
        self.settings.setValue("font_family", self.font_combo.currentText())
        
        if platform.system() == "Windows":
            key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
            app_name = "DesktopMemo"
            app_path = sys.executable
            try:
                with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE) as key:
                    if self.startup_check.isChecked():
                        winreg.SetValueEx(key, app_name, 0, winreg.REG_SZ, app_path)
                    else:
                        try:
                            winreg.DeleteValue(key, app_name)
                        except FileNotFoundError:
                            pass
            except OSError as e:
                self.parent.show_error(f"系统设置失败: {e}")
                
        self.parent.apply_settings()
        self.accept()
        
    def choose_font_color(self):
        color = QColorDialog.getColor(QColor(self.settings.value("font_color", "#000000")))
        if color.isValid():
            self.settings.setValue("font_color", color.name())
            self.parent.apply_settings()
            
    def choose_bg_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.settings.setValue("bg_color", color.name())
            self.parent.apply_settings()

class DesktopMemoApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.settings = QSettings(SETTINGS_FILE, QSettings.IniFormat)
        self.memos = self.load_memos()
        self.drag_position = None
        self.init_ui()
        self.apply_settings()
        self.setup_midnight_timer()
        
    def init_ui(self):
        self.setWindowTitle("桌面备忘录")
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setMinimumSize(800, 900)
        
        main_widget = QWidget()
        main_widget.setObjectName("MainWidget")
        self.setCentralWidget(main_widget)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # 标题栏
        title_bar = QHBoxLayout()
        self.title_label = QLabel("柘记")
        self.title_label.setObjectName("TitleLabel")
        
        self.pin_top_btn = QPushButton("📌")
        self.pin_top_btn.setFixedSize(40, 40)
        self.pin_top_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                border-radius: 20px;
                font-size: 24px;
                color: #666;
            }
            QPushButton:hover { background: rgba(0,0,0,0.1); }
        """)
        self.pin_top_btn.clicked.connect(self.toggle_pin_top)
        
        self.minimize_btn = QPushButton("➖")
        self.settings_btn = QPushButton("⚙️")
        self.close_btn = QPushButton("❌")
        
        buttons = [self.pin_top_btn, self.minimize_btn, self.settings_btn, self.close_btn]
        for btn in buttons:
            btn.setFixedSize(40, 40)
            btn.setStyleSheet("""
                QPushButton {
                    background: transparent;
                    border-radius: 20px;
                    font-size: 24px;
                    color: #666;
                }
                QPushButton:hover { background: rgba(0,0,0,0.1); }
            """)
            
        title_bar.addWidget(self.pin_top_btn)
        title_bar.addWidget(self.title_label)
        title_bar.addStretch()
        title_bar.addWidget(self.minimize_btn)
        title_bar.addWidget(self.settings_btn)
        title_bar.addWidget(self.close_btn)
        
        # 倒计时区域
        countdown_area = QWidget()
        countdown_area.setObjectName("CountdownArea")
        countdown_layout = QHBoxLayout()
        countdown_layout.setSpacing(10)
        self.todo_labels = [QLabel() for _ in range(4)]
        for label in self.todo_labels:
            label.setAlignment(Qt.AlignCenter)
            label.setMinimumSize(150, 100)
            label.setWordWrap(True)
            label.setStyleSheet("""
                border: 2px solid #2196F3;
                border-radius: 10px;
                font-weight: bold;
                font-size: 14px;
                padding: 10px;
            """)
            countdown_layout.addWidget(label)
        countdown_area.setLayout(countdown_layout)
        
        # 日历区域
        calendar_area = QWidget()
        calendar_area.setObjectName("CalendarArea")
        calendar_layout = QVBoxLayout()
        calendar_layout.setAlignment(Qt.AlignCenter)
        calendar_layout.setContentsMargins(0, 0, 0, 0)
        self.calendar = ModernCalendar(self)
        self.calendar.setFixedSize(700, 380)
        calendar_layout.addWidget(self.calendar)
        calendar_area.setLayout(calendar_layout)
        
        # 备忘录区域
        memo_area = QWidget()
        memo_area.setObjectName("MemoArea")
        memo_layout = QVBoxLayout()
        memo_layout.setSpacing(10)
        
        memo_title = QLabel("当日备忘：")
        memo_title.setObjectName("MemoTitle")
        
        self.memo_table = QTableWidget(0, 1)
        self.memo_table.horizontalHeader().setVisible(False)
        self.memo_table.verticalHeader().setVisible(False)
        self.memo_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.memo_table.setMinimumHeight(400)
        self.memo_table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.memo_table.customContextMenuRequested.connect(self.show_context_menu)
        
        btn_layout = QHBoxLayout()
        self.add_btn = QPushButton("📝 添加")
        self.save_btn = QPushButton("💾 保存")
        btn_layout.addWidget(self.add_btn)
        btn_layout.addStretch()
        btn_layout.addWidget(self.save_btn)
        
        self.add_btn.setStyleSheet("""
            QPushButton {
                background: #4CAF50;
                color: white;
                border: 2px solid #45a049;
                border-radius: 15px;
                padding: 8px 16px;
                font-size: 16px;
            }
            QPushButton:hover {
                background: #45a049;
            }
        """)
        
        self.save_btn.setStyleSheet("""
            QPushButton {
                background: #2196F3;
                color: white;
                border: 2px solid #1976D2;
                border-radius: 15px;
                padding: 8px 16px;
                font-size: 16px;
            }
            QPushButton:hover {
                background: #1976D2;
            }
        """)
        
        memo_layout.addWidget(memo_title)
        memo_layout.addWidget(self.memo_table)
        memo_layout.addLayout(btn_layout)
        memo_area.setLayout(memo_layout)
        
        # 主布局
        layout.addLayout(title_bar)
        layout.addWidget(countdown_area)
        layout.addWidget(calendar_area)
        layout.addWidget(memo_area)
        
        main_widget.setLayout(layout)
        
        self.minimize_btn.clicked.connect(self.showMinimized)
        self.settings_btn.clicked.connect(self.show_settings)
        self.close_btn.clicked.connect(self.close)
        self.add_btn.clicked.connect(self.add_memo)
        self.save_btn.clicked.connect(self.save_memos)
        self.calendar.dateChanged.connect(self.load_daily_memos)
        self.memo_table.itemChanged.connect(self.update_memo_status)
        
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.drag_position is not None:
            self.move(event.globalPos() - self.drag_position)
            event.accept()
    
    def apply_settings(self):
        opacity = self.settings.value("opacity", 80, type=int) / 100
        font_size = self.settings.value("font_size", 18, type=int)
        font_family = self.settings.value("font_family", "Microsoft YaHei", type=str)
        bg_color = self.settings.value("bg_color", "#F5F5F5", type=str)
        font_color = self.settings.value("font_color", "#000000", type=str)
        
        base_color = QColor(bg_color)
        text_color = QColor(font_color)
        
        brightness = base_color.redF() * 0.299 + base_color.greenF() * 0.587 + base_color.blueF() * 0.114
        text_color = QColor("#FFFFFF" if brightness < 0.5 else "#333333")
            
        style = f"""
            * {{
                font-family: {font_family};
                font-size: {font_size}px;
                color: {text_color.name()};
            }}
            #MainWidget {{
                background: rgba({base_color.red()}, {base_color.green()}, {base_color.blue()}, {opacity});
                border-radius: 15px;
                border: 1px solid {base_color.darker(120).name()};
            }}
            #CountdownArea, #CalendarArea, #MemoArea {{
                background: rgba({base_color.red()}, {base_color.green()}, {base_color.blue()}, {opacity * 0.85});
                border-radius: 12px;
                padding: 15px;
                margin: 5px 0;
            }}
            QLabel {{
                background: transparent;
                border-radius: 8px;
                padding: 10px;
            }}
            #MemoTitle {{
                font-size: 16px;
                font-weight: bold;
                margin-bottom: 10px;
            }}
            QTableWidget {{
                background: transparent;
                border: none;
            }}
            QTableWidget::item {{
                border-bottom: 1px solid {base_color.darker(110).name()};
            }}
            QPushButton {{
                background: transparent;
                border-radius: 20px;
                font-size: 24px;
                color: {text_color.name()};
            }}
        """
        self.setStyleSheet(style)
        self.update_todo_display()
        
    def update_todo_display(self):
        all_memos = []
        for date_str in self.memos:
            # 获取目标日期
            target_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            for memo in self.memos[date_str]:
                all_memos.append((target_date, memo))

        # 过滤过期项并计算剩余天数
        valid_memos = []
        today = datetime.now().date()
        for target_date, memo in all_memos:
            days_left = (target_date - today).days
            if days_left >= 0:
                valid_memos.append((days_left, memo))
        
        # 按置顶状态和日期排序
        sorted_memos = sorted(valid_memos, key=lambda x: (-x[1].get("pinned", False), x[0]))
        display_memos = sorted_memos[:4]

        for i in range(4):
            label = self.todo_labels[i]
            if i < len(display_memos):
                days_left, memo = display_memos[i]
                content = memo['content'][:12] + "..." if len(memo['content']) > 12 else memo['content']
                label.setText(f"距【{content}】还有\n{days_left}天")
                label.setStyleSheet(f"""
                    border: 2px solid {'#4CAF50' if memo["done"] else '#2196F3'};
                    border-radius: 10px;
                    font-weight: bold;
                    font-size: {int(self.settings.value('font_size', 18)) * 0.7}px;
                    padding: 10px;
                """)
            else:
                label.setText("")
                label.setStyleSheet("border: none;")
                
    def load_daily_memos(self, qdate):
        date_str = qdate.toString("yyyy-MM-dd")
        self.memo_table.setRowCount(0)
        if date_str in self.memos and isinstance(self.memos[date_str], list):
            sorted_memos = sorted(
                self.memos[date_str],
                key=lambda x: (-x["pinned"], x["timestamp"])
            )
            for memo in sorted_memos:
                row = self.memo_table.rowCount()
                self.memo_table.insertRow(row)
                content_item = QTableWidgetItem(memo["content"])
                content_item.setFlags(content_item.flags() | Qt.ItemIsUserCheckable)
                content_item.setCheckState(Qt.Checked if memo["done"] else Qt.Unchecked)
                self.memo_table.setItem(row, 0, content_item)
                
    def show_context_menu(self, pos):
        menu = QMenu(self)
        current_memo = self.get_current_memo()
        pin_action = QAction("📌 置顶" if not current_memo.get("pinned", False) else "📌 取消置顶", self)
        delete_action = QAction("🗑️ 删除", self)
        menu.addAction(pin_action)
        menu.addAction(delete_action)
        pin_action.triggered.connect(self.toggle_pin_status)
        delete_action.triggered.connect(self.del_memo)
        menu.exec_(self.memo_table.viewport().mapToGlobal(pos))
        
    def get_current_memo(self):
        row = self.memo_table.currentRow()
        date_str = self.calendar.selected_date.toString("yyyy-MM-dd")
        if date_str in self.memos and 0 <= row < len(self.memos[date_str]):
            return self.memos[date_str][row]
        return {}
    
    def toggle_pin_status(self):
        row = self.memo_table.currentRow()
        date_str = self.calendar.selected_date.toString("yyyy-MM-dd")
        if date_str in self.memos and 0 <= row < len(self.memos[date_str]):
            memo = self.memos[date_str][row]
            memo["pinned"] = not memo.get("pinned", False)
            if memo["pinned"]:
                self.memos[date_str].insert(0, self.memos[date_str].pop(row))
            self.save_memos()
            self.load_daily_memos(self.calendar.selected_date)
            self.update_todo_display()
            
    def load_memos(self):
        try:
            with open(MEMOS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, dict):
                    for date_key in data:
                        memos = data[date_key]
                        if not isinstance(memos, list):
                            memos = []
                        for memo in memos:
                            # 兼容旧数据
                            if 'target_date' not in memo:
                                memo_date = datetime.fromisoformat(memo['timestamp']).date()
                                memo['target_date'] = memo_date.isoformat()
                            if 'pinned' not in memo:
                                memo['pinned'] = False
                        data[date_key] = memos
                    return data
        except (FileNotFoundError, json.JSONDecodeError):
            return {}
        
    def save_memos(self):
        with open(MEMOS_FILE, "w", encoding="utf-8") as f:
            json.dump(self.memos, f, ensure_ascii=False)
        self.update_todo_display()
        self.calendar.update_calendar()
        
    def add_memo(self):
        date_str = self.calendar.selected_date.toString("yyyy-MM-dd")
        if date_str not in self.memos:
            self.memos[date_str] = []
        new_memo = {
            "id": str(len(self.memos[date_str]) + 1),
            "content": "新备忘内容",
            "done": False,
            "pinned": False,
            "target_date": date_str,
            "timestamp": datetime.now().isoformat()
        }
        self.memos[date_str].append(new_memo)
        row = self.memo_table.rowCount()
        self.memo_table.insertRow(row)
        content_item = QTableWidgetItem(new_memo["content"])
        content_item.setCheckState(Qt.Unchecked)
        self.memo_table.setItem(row, 0, content_item)
        self.save_memos()
        
    def del_memo(self):
        row = self.memo_table.currentRow()
        if row >= 0:
            date_str = self.calendar.selected_date.toString("yyyy-MM-dd")
            if date_str in self.memos and row < len(self.memos[date_str]):
                del self.memos[date_str][row]
                self.memo_table.removeRow(row)
                self.save_memos()
                self.update_todo_display()
                
    def update_memo_status(self, item):
        row = item.row()
        date_str = self.calendar.selected_date.toString("yyyy-MM-dd")
        if date_str in self.memos and row < len(self.memos[date_str]):
            memo = self.memos[date_str][row]
            if item.column() == 0:
                memo["content"] = item.text()
                memo["done"] = item.checkState() == Qt.Checked
                self.save_memos()
                self.update_todo_display()
                
    def export_data(self):
        path, _ = QFileDialog.getSaveFileName(self, "导出数据", "", "CSV文件 (*.csv)")
        if path:
            try:
                with open(path, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(["日期", "内容", "完成状态", "置顶状态", "创建时间"])
                    for date_key, memos in self.memos.items():
                        if isinstance(memos, list):
                            for memo in memos:
                                writer.writerow([
                                    date_key,
                                    memo.get("content", ""),
                                    "是" if memo.get("done", False) else "否",
                                    "是" if memo.get("pinned", False) else "否",
                                    memo.get("timestamp", "")
                                ])
            except Exception as e:
                self.show_error(f"导出失败: {str(e)}")
                
    def show_settings(self):
        dialog = SettingsDialog(self)
        dialog.exec_()
        
    def show_error(self, message):
        error_label = QLabel(message)
        error_label.setStyleSheet("""
            background: rgba(255, 235, 238, 0.9);
            color: #b71c1c;
            padding: 12px;
            border-radius: 8px;
            border: 1px solid #ffcdd2;
        """)
        error_label.setWindowFlags(Qt.ToolTip)
        error_label.show()
        QTimer.singleShot(5000, error_label.deleteLater)
        
    def setup_midnight_timer(self):
        now = datetime.now()
        midnight = datetime.combine(now.date() + timedelta(days=1), datetime.min.time())
        delta = (midnight - now).total_seconds() * 1000
        
        self.midnight_timer = QTimer(self)
        self.midnight_timer.setSingleShot(True)
        self.midnight_timer.timeout.connect(lambda: [
            self.update_todo_display(),
            self.setup_midnight_timer()
        ])
        self.midnight_timer.start(int(delta))
    
    def toggle_pin_top(self):
        if self.windowFlags() & Qt.WindowStaysOnTopHint:
            self.setWindowFlags(self.windowFlags() & ~Qt.WindowStaysOnTopHint)
            self.pin_top_btn.setText("📌")
        else:
            self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
            self.pin_top_btn.setText("📍")
        self.show()
        
    def closeEvent(self, event):
        self.save_memos()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setFont(QFont("Microsoft YaHei", 14))
    window = DesktopMemoApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(":/app.ico"))  # 设置应用级图标
    window = DesktopMemoApp()
    window.show()
    sys.exit(app.exec_())