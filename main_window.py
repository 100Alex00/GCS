# ui/main_window.py

from PyQt5.QtWidgets import (QMainWindow, QTabWidget, QWidget, QVBoxLayout, 
                             QPushButton, QTableWidget, QTableWidgetItem, 
                             QFormLayout, QLineEdit, QSpinBox, QDoubleSpinBox,
                             QDateEdit, QHBoxLayout, QMessageBox, QLabel, 
                             QComboBox, QSplitter, QGroupBox, QScrollArea)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QFont, QIcon, QColor
from PyQt5.QtWidgets import QDialog
from models.console import Console
from models.accessory import Accessory
from models.client import Client
from models.order import Order, OrderItem
from datetime import date

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🎮 Магазин игровых консолей")
        self.setGeometry(100, 100, 1400, 900)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f2f5;
            }
            QTabWidget::pane {
                border: 1px solid #d6d9dc;
                background: white;
            }
            QTabBar::tab {
                background: #e0e3e7;
                padding: 12px 20px;
                margin-right: 2px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }
            QTabBar::tab:selected {
                background: white;
                border-bottom: 1px solid white;
            }
            QPushButton {
                padding: 8px 15px;
                border-radius: 4px;
                font-weight: bold;
                min-width: 100px;
            }
            QPushButton:hover {
                opacity: 0.9;
            }
            QTableWidget {
                gridline-color: #d6d9dc;
            }
            QHeaderView::section {
                background-color: #f8f9fa;
                padding: 8px;
                border: 1px solid #d6d9dc;
                font-weight: bold;
            }
            QGroupBox {
                font-weight: bold;
                border: 1px solid #d6d9dc;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subline-color: #495057;
                padding: 0 5px;
            }
        """)
        
        self.init_ui()
    
    def init_ui(self):
        # Создаем вкладки
        self.tabs = QTabWidget()
        self.tabs.setTabPosition(QTabWidget.North)
        self.tabs.setStyleSheet("""
            QTabBar::tab {
                background: #e0e3e7;
                padding: 12px 20px;
                margin-right: 2px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }
            QTabBar::tab:selected {
                background: white;
                border-bottom: 1px solid white;
            }
        """)
        self.setCentralWidget(self.tabs)
        
        # Добавляем вкладки
        self.add_console_tab()
        self.add_accessory_tab()
        self.add_client_tab()
        self.add_order_tab()
    
    def add_console_tab(self):
        # Создаем вкладку для консолей
        tab = QWidget()
        tab.setStyleSheet("QWidget { background-color: #ffffff; }")
        layout = QVBoxLayout()
        
        # Заголовок раздела
        header = QLabel("🎮 Управление игровыми консолями")
        header.setFont(QFont("Arial", 16, QFont.Bold))
        header.setStyleSheet("color: #2c3e50; padding: 10px;")
        layout.addWidget(header)
        
        # Разделитель
        layout.addWidget(self.create_separator())
        
        # Таблица с консолями
        self.console_table = QTableWidget()
        self.console_table.setColumnCount(7)
        self.console_table.setHorizontalHeaderLabels(["ID", "Название", "Производитель", "Год выпуска", "Цена", "В наличии", "Описание"])
        self.console_table.setSortingEnabled(True)
        self.console_table.setStyleSheet("""
            QTableWidget {
                gridline-color: #d6d9dc;
            }
            QTableWidget:item:selected {
                background-color: #e8f0fe;
            }
        """)
        layout.addWidget(self.console_table)
        
        # Форма добавления/редактирования
        form_group = QGroupBox("📝 Форма ввода")
        form_layout = QFormLayout()
        
        self.console_name = QLineEdit()
        self.console_manufacturer = QLineEdit()
        self.console_year = QSpinBox()
        self.console_year.setRange(1980, 2030)
        self.console_price = QDoubleSpinBox()
        self.console_price.setRange(0, 1000000)
        self.console_stock = QSpinBox()
        self.console_stock.setRange(0, 1000)
        self.console_description = QLineEdit()
        
        form_layout.addRow("Название:", self.console_name)
        form_layout.addRow("Производитель:", self.console_manufacturer)
        form_layout.addRow("Год выпуска:", self.console_year)
        form_layout.addRow("Цена:", self.console_price)
        form_layout.addRow("В наличии:", self.console_stock)
        form_layout.addRow("Описание:", self.console_description)
        
        form_group.setLayout(form_layout)
        layout.addWidget(form_group)
        
        # Кнопки действий
        button_layout = QHBoxLayout()
        self.add_console_btn = QPushButton("➕ Добавить")
        self.edit_console_btn = QPushButton("✏️ Редактировать")
        self.delete_console_btn = QPushButton("❌ Удалить")
        self.clear_console_btn = QPushButton("🧹 Очистить")
        
        self.add_console_btn.setStyleSheet("QPushButton { background-color: #28a745; color: white; }")
        self.edit_console_btn.setStyleSheet("QPushButton { background-color: #007bff; color: white; }")
        self.delete_console_btn.setStyleSheet("QPushButton { background-color: #dc3545; color: white; }")
        self.clear_console_btn.setStyleSheet("QPushButton { background-color: #6c757d; color: white; }")
        
        self.add_console_btn.clicked.connect(self.add_console)
        self.edit_console_btn.clicked.connect(self.edit_console)
        self.delete_console_btn.clicked.connect(self.delete_console)
        self.clear_console_btn.clicked.connect(self.clear_console_form)
        
        button_layout.addWidget(self.add_console_btn)
        button_layout.addWidget(self.edit_console_btn)
        button_layout.addWidget(self.delete_console_btn)
        button_layout.addWidget(self.clear_console_btn)
        button_layout.addStretch()
        
        layout.addLayout(button_layout)
        
        # Загружаем данные
        self.load_consoles()
        
        tab.setLayout(layout)
        self.tabs.addTab(tab, "🎮 Консоли")
    
    def create_separator(self):
        separator = QLabel()
        separator.setFrameStyle(QLabel.HLine)
        separator.setStyleSheet("background-color: #d6d9dc; min-height: 1px;")
        return separator
    
    def load_consoles(self):
        consoles = Console.get_all()
        self.console_table.setRowCount(len(consoles))
        for row, console in enumerate(consoles):
            self.console_table.setItem(row, 0, QTableWidgetItem(str(console.id)))
            self.console_table.setItem(row, 1, QTableWidgetItem(console.name))
            self.console_table.setItem(row, 2, QTableWidgetItem(console.manufacturer))
            self.console_table.setItem(row, 3, QTableWidgetItem(str(console.release_year)))
            self.console_table.setItem(row, 4, QTableWidgetItem(f"{console.price:.2f} ₽"))
            self.console_table.setItem(row, 5, QTableWidgetItem(str(console.stock)))
            self.console_table.setItem(row, 6, QTableWidgetItem(console.description))
    
    def add_console(self):
        if not self.console_name.text() or not self.console_manufacturer.text():
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, заполните обязательные поля!")
            return
            
        console = Console(
            name=self.console_name.text(),
            manufacturer=self.console_manufacturer.text(),
            release_year=self.console_year.value(),
            price=self.console_price.value(),
            stock=self.console_stock.value(),
            description=self.console_description.text()
        )
        console.save()
        self.clear_console_form()
        self.load_consoles()
        QMessageBox.information(self, "Успех", "✅ Консоль успешно добавлена")
    
    def edit_console(self):
        selected = self.console_table.currentRow()
        if selected >= 0:
            console_id = int(self.console_table.item(selected, 0).text())
            console = Console.get_by_id(console_id)
            
            console.name = self.console_name.text()
            console.manufacturer = self.console_manufacturer.text()
            console.release_year = self.console_year.value()
            console.price = self.console_price.value()
            console.stock = self.console_stock.value()
            console.description = self.console_description.text()
            
            console.save()
            self.clear_console_form()
            self.load_consoles()
            QMessageBox.information(self, "Успех", "✅ Консоль успешно обновлена")
    
    def delete_console(self):
        selected = self.console_table.currentRow()
        if selected >= 0:
            console_id = int(self.console_table.item(selected, 0).text())
            console = Console.get_by_id(console_id)
            console.delete()
            self.clear_console_form()
            self.load_consoles()
            QMessageBox.information(self, "Успех", "✅ Консоль успешно удалена")
    
    def clear_console_form(self):
        self.console_name.clear()
        self.console_manufacturer.clear()
        self.console_year.setValue(2023)
        self.console_price.setValue(0)
        self.console_stock.setValue(0)
        self.console_description.clear()

    def add_accessory_tab(self):
        # Создаем вкладку для аксессуаров
        tab = QWidget()
        tab.setStyleSheet("QWidget { background-color: #ffffff; }")
        layout = QVBoxLayout()
        
        # Заголовок раздела
        header = QLabel("🎯 Управление аксессуарами")
        header.setFont(QFont("Arial", 16, QFont.Bold))
        header.setStyleSheet("color: #2c3e50; padding: 10px;")
        layout.addWidget(header)
        
        # Разделитель
        layout.addWidget(self.create_separator())
        
        # Таблица с аксессуарами
        self.accessory_table = QTableWidget()
        self.accessory_table.setColumnCount(5)
        self.accessory_table.setHorizontalHeaderLabels(["ID", "Название", "Консоль", "Цена", "В наличии"])
        self.accessory_table.setSortingEnabled(True)
        self.accessory_table.setStyleSheet("""
            QTableWidget {
                gridline-color: #d6d9dc;
            }
            QTableWidget:item:selected {
                background-color: #e8f0fe;
            }
        """)
        layout.addWidget(self.accessory_table)
        
        # Форма добавления/редактирования
        form_group = QGroupBox("📝 Форма ввода")
        form_layout = QFormLayout()
        
        self.accessory_name = QLineEdit()
        self.accessory_console = QComboBox()
        self.load_consoles_for_combo(self.accessory_console)
        self.accessory_price = QDoubleSpinBox()
        self.accessory_price.setRange(0, 1000000)
        self.accessory_stock = QSpinBox()
        self.accessory_stock.setRange(0, 1000)
        
        form_layout.addRow("Название:", self.accessory_name)
        form_layout.addRow("Консоль:", self.accessory_console)
        form_layout.addRow("Цена:", self.accessory_price)
        form_layout.addRow("В наличии:", self.accessory_stock)
        
        form_group.setLayout(form_layout)
        layout.addWidget(form_group)
        
        # Кнопки действий
        button_layout = QHBoxLayout()
        self.add_accessory_btn = QPushButton("➕ Добавить")
        self.edit_accessory_btn = QPushButton("✏️ Редактировать")
        self.delete_accessory_btn = QPushButton("❌ Удалить")
        self.clear_accessory_btn = QPushButton("🧹 Очистить")
        
        self.add_accessory_btn.setStyleSheet("QPushButton { background-color: #28a745; color: white; }")
        self.edit_accessory_btn.setStyleSheet("QPushButton { background-color: #007bff; color: white; }")
        self.delete_accessory_btn.setStyleSheet("QPushButton { background-color: #dc3545; color: white; }")
        self.clear_accessory_btn.setStyleSheet("QPushButton { background-color: #6c757d; color: white; }")
        
        self.add_accessory_btn.clicked.connect(self.add_accessory)
        self.edit_accessory_btn.clicked.connect(self.edit_accessory)
        self.delete_accessory_btn.clicked.connect(self.delete_accessory)
        self.clear_accessory_btn.clicked.connect(self.clear_accessory_form)
        
        button_layout.addWidget(self.add_accessory_btn)
        button_layout.addWidget(self.edit_accessory_btn)
        button_layout.addWidget(self.delete_accessory_btn)
        button_layout.addWidget(self.clear_accessory_btn)
        button_layout.addStretch()
        
        layout.addLayout(button_layout)
        
        # Загружаем данные
        self.load_accessories()
        
        tab.setLayout(layout)
        self.tabs.addTab(tab, "🎯 Аксессуары")
    
    def load_consoles_for_combo(self, combo):
        consoles = Console.get_all()
        for console in consoles:
            combo.addItem(console.name, console.id)
    
    def load_accessories(self):
        accessories = Accessory.get_all()
        self.accessory_table.setRowCount(len(accessories))
        for row, accessory in enumerate(accessories):
            self.accessory_table.setItem(row, 0, QTableWidgetItem(str(accessory.id)))
            self.accessory_table.setItem(row, 1, QTableWidgetItem(accessory.name))
            
            console = Console.get_by_id(accessory.console_id)
            console_name = console.name if console else "Неизвестная консоль"
            self.accessory_table.setItem(row, 2, QTableWidgetItem(console_name))
            
            self.accessory_table.setItem(row, 3, QTableWidgetItem(f"{accessory.price:.2f} ₽"))
            self.accessory_table.setItem(row, 4, QTableWidgetItem(str(accessory.stock)))
    
    def add_accessory(self):
        if not self.accessory_name.text():
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, заполните обязательные поля!")
            return
            
        accessory = Accessory(
            name=self.accessory_name.text(),
            console_id=self.accessory_console.currentData(),
            price=self.accessory_price.value(),
            stock=self.accessory_stock.value()
        )
        accessory.save()
        self.clear_accessory_form()
        self.load_accessories()
        QMessageBox.information(self, "Успех", "✅ Аксессуар успешно добавлен")
    
    def edit_accessory(self):
        selected = self.accessory_table.currentRow()
        if selected >= 0:
            accessory_id = int(self.accessory_table.item(selected, 0).text())
            accessory = Accessory.get_by_id(accessory_id)
            
            accessory.name = self.accessory_name.text()
            accessory.console_id = self.accessory_console.currentData()
            accessory.price = self.accessory_price.value()
            accessory.stock = self.accessory_stock.value()
            
            accessory.save()
            self.clear_accessory_form()
            self.load_accessories()
            QMessageBox.information(self, "Успех", "✅ Аксессуар успешно обновлен")
    
    def delete_accessory(self):
        selected = self.accessory_table.currentRow()
        if selected >= 0:
            accessory_id = int(self.accessory_table.item(selected, 0).text())
            accessory = Accessory.get_by_id(accessory_id)
            accessory.delete()
            self.clear_accessory_form()
            self.load_accessories()
            QMessageBox.information(self, "Успех", "✅ Аксессуар успешно удален")
    
    def clear_accessory_form(self):
        self.accessory_name.clear()
        self.accessory_console.setCurrentIndex(0)
        self.accessory_price.setValue(0)
        self.accessory_stock.setValue(0)

    def add_client_tab(self):
        # Создаем вкладку для клиентов
        tab = QWidget()
        tab.setStyleSheet("QWidget { background-color: #ffffff; }")
        layout = QVBoxLayout()
        
        # Заголовок раздела
        header = QLabel("👥 Управление клиентами")
        header.setFont(QFont("Arial", 16, QFont.Bold))
        header.setStyleSheet("color: #2c3e50; padding: 10px;")
        layout.addWidget(header)
        
        # Разделитель
        layout.addWidget(self.create_separator())
        
        # Таблица с клиентами
        self.client_table = QTableWidget()
        self.client_table.setColumnCount(5)
        self.client_table.setHorizontalHeaderLabels(["ID", "ФИО", "Email", "Телефон", "Адрес"])
        self.client_table.setSortingEnabled(True)
        self.client_table.setStyleSheet("""
            QTableWidget {
                gridline-color: #d6d9dc;
            }
            QTableWidget:item:selected {
                background-color: #e8f0fe;
            }
        """)
        layout.addWidget(self.client_table)
        
        # Форма добавления/редактирования
        form_group = QGroupBox("📝 Форма ввода")
        form_layout = QFormLayout()
        
        self.client_name = QLineEdit()
        self.client_email = QLineEdit()
        self.client_phone = QLineEdit()
        self.client_address = QLineEdit()
        
        form_layout.addRow("ФИО:", self.client_name)
        form_layout.addRow("Email:", self.client_email)
        form_layout.addRow("Телефон:", self.client_phone)
        form_layout.addRow("Адрес:", self.client_address)
        
        form_group.setLayout(form_layout)
        layout.addWidget(form_group)
        
        # Кнопки действий
        button_layout = QHBoxLayout()
        self.add_client_btn = QPushButton("➕ Добавить")
        self.edit_client_btn = QPushButton("✏️ Редактировать")
        self.delete_client_btn = QPushButton("❌ Удалить")
        self.clear_client_btn = QPushButton("🧹 Очистить")
        
        self.add_client_btn.setStyleSheet("QPushButton { background-color: #28a745; color: white; }")
        self.edit_client_btn.setStyleSheet("QPushButton { background-color: #007bff; color: white; }")
        self.delete_client_btn.setStyleSheet("QPushButton { background-color: #dc3545; color: white; }")
        self.clear_client_btn.setStyleSheet("QPushButton { background-color: #6c757d; color: white; }")
        
        self.add_client_btn.clicked.connect(self.add_client)
        self.edit_client_btn.clicked.connect(self.edit_client)
        self.delete_client_btn.clicked.connect(self.delete_client)
        self.clear_client_btn.clicked.connect(self.clear_client_form)
        
        button_layout.addWidget(self.add_client_btn)
        button_layout.addWidget(self.edit_client_btn)
        button_layout.addWidget(self.delete_client_btn)
        button_layout.addWidget(self.clear_client_btn)
        button_layout.addStretch()
        
        layout.addLayout(button_layout)
        
        # Загружаем данные
        self.load_clients()
        
        tab.setLayout(layout)
        self.tabs.addTab(tab, "👥 Клиенты")
    
    def load_clients(self):
        clients = Client.get_all()
        self.client_table.setRowCount(len(clients))
        for row, client in enumerate(clients):
            self.client_table.setItem(row, 0, QTableWidgetItem(str(client.id)))
            self.client_table.setItem(row, 1, QTableWidgetItem(client.name))
            self.client_table.setItem(row, 2, QTableWidgetItem(client.email))
            self.client_table.setItem(row, 3, QTableWidgetItem(client.phone))
            self.client_table.setItem(row, 4, QTableWidgetItem(client.address))
    
    def add_client(self):
        if not self.client_name.text() or not self.client_phone.text():
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, заполните обязательные поля!")
            return
            
        client = Client(
            name=self.client_name.text(),
            email=self.client_email.text(),
            phone=self.client_phone.text(),
            address=self.client_address.text()
        )
        client.save()
        self.clear_client_form()
        self.load_clients()
        QMessageBox.information(self, "Успех", "✅ Клиент успешно добавлен")
    
    def edit_client(self):
        selected = self.client_table.currentRow()
        if selected >= 0:
            client_id = int(self.client_table.item(selected, 0).text())
            client = Client.get_by_id(client_id)
            
            client.name = self.client_name.text()
            client.email = self.client_email.text()
            client.phone = self.client_phone.text()
            client.address = self.client_address.text()
            
            client.save()
            self.clear_client_form()
            self.load_clients()
            QMessageBox.information(self, "Успех", "✅ Клиент успешно обновлен")
    
    def delete_client(self):
        selected = self.client_table.currentRow()
        if selected >= 0:
            client_id = int(self.client_table.item(selected, 0).text())
            client = Client.get_by_id(client_id)
            client.delete()
            self.clear_client_form()
            self.load_clients()
            QMessageBox.information(self, "Успех", "✅ Клиент успешно удален")
    
    def clear_client_form(self):
        self.client_name.clear()
        self.client_email.clear()
        self.client_phone.clear()
        self.client_address.clear()

    def add_order_tab(self):
        # Создаем вкладку для заказов
        tab = QWidget()
        tab.setStyleSheet("QWidget { background-color: #ffffff; }")
        layout = QVBoxLayout()
        
        # Заголовок раздела
        header = QLabel("🛒 Управление заказами")
        header.setFont(QFont("Arial", 16, QFont.Bold))
        header.setStyleSheet("color: #2c3e50; padding: 10px;")
        layout.addWidget(header)
        
        # Разделитель
        layout.addWidget(self.create_separator())
        
        # Горизонтальный разделитель
        h_splitter = QSplitter(Qt.Horizontal)
        
        # Левая часть - список заказов
        left_widget = QWidget()
        left_layout = QVBoxLayout()
        
        # Таблица заказов
        self.order_table = QTableWidget()
        self.order_table.setColumnCount(4)
        self.order_table.setHorizontalHeaderLabels(["ID", "Клиент", "Дата", "Сумма"])
        self.order_table.setSortingEnabled(True)
        self.order_table.setStyleSheet("""
            QTableWidget {
                gridline-color: #d6d9dc;
            }
            QTableWidget:item:selected {
                background-color: #e8f0fe;
            }
        """)
        left_layout.addWidget(self.order_table)
        
        # Кнопки управления заказами
        order_button_layout = QHBoxLayout()
        self.add_order_btn = QPushButton("➕ Новый заказ")
        self.delete_order_btn = QPushButton("❌ Удалить")
        self.manage_items_btn = QPushButton("🧩 Управление позициями")
        
        self.add_order_btn.setStyleSheet("QPushButton { background-color: #28a745; color: white; }")
        self.delete_order_btn.setStyleSheet("QPushButton { background-color: #dc3545; color: white; }")
        self.manage_items_btn.setStyleSheet("QPushButton { background-color: #007bff; color: white; }")
        
        self.add_order_btn.clicked.connect(self.add_order)
        self.delete_order_btn.clicked.connect(self.delete_order)
        self.manage_items_btn.clicked.connect(self.manage_order_items)
        
        order_button_layout.addWidget(self.add_order_btn)
        order_button_layout.addWidget(self.delete_order_btn)
        order_button_layout.addWidget(self.manage_items_btn)
        order_button_layout.addStretch()
        
        left_layout.addLayout(order_button_layout)
        
        left_widget.setLayout(left_layout)
        
        # Правая часть - детали заказа
        right_widget = QWidget()
        right_layout = QVBoxLayout()
        
        # Таблица позиций заказа
        self.order_items_table = QTableWidget()
        self.order_items_table.setColumnCount(4)
        self.order_items_table.setHorizontalHeaderLabels(["Товар", "Количество", "Цена", "Сумма"])
        self.order_items_table.setSortingEnabled(True)
        self.order_items_table.setStyleSheet("""
            QTableWidget {
                gridline-color: #d6d9dc;
            }
            QTableWidget:item:selected {
                background-color: #e8f0fe;
            }
        """)
        right_layout.addWidget(self.order_items_table)
        
        # Общая сумма
        total_layout = QHBoxLayout()
        total_label = QLabel("🧮 Общая сумма:")
        total_label.setFont(QFont("Arial", 12, QFont.Bold))
        self.total_amount = QLabel("0.00 ₽")
        self.total_amount.setFont(QFont("Arial", 12, QFont.Bold))
        self.total_amount.setStyleSheet("color: #28a745;")
        
        total_layout.addWidget(total_label)
        total_layout.addStretch()
        total_layout.addWidget(self.total_amount)
        total_layout.setContentsMargins(0, 10, 0, 0)
        
        right_layout.addLayout(total_layout)
        
        right_widget.setLayout(right_layout)
        
        # Добавляем левую и правую части в горизонтальный разделитель
        h_splitter.addWidget(left_widget)
        h_splitter.addWidget(right_widget)
        h_splitter.setSizes([int(self.width() * 0.6), int(self.width() * 0.4)])
        
        # Добавляем горизонтальный разделитель в основной макет
        layout.addWidget(h_splitter)
        
        # Загружаем данные
        self.load_orders()
        
        tab.setLayout(layout)
        self.tabs.addTab(tab, "🛒 Заказы")
    
    def load_orders(self):
        orders = Order.get_all()
        self.order_table.setRowCount(len(orders))
        for row, order in enumerate(orders):
            self.order_table.setItem(row, 0, QTableWidgetItem(str(order.id)))
            
            client = Client.get_by_id(order.client_id)
            client_name = client.name if client else "Неизвестный клиент"
            self.order_table.setItem(row, 1, QTableWidgetItem(client_name))
            
            self.order_table.setItem(row, 2, QTableWidgetItem(order.order_date))
            self.order_table.setItem(row, 3, QTableWidgetItem(f"{order.total_amount:.2f} ₽"))
    
    def add_order(self):
        # Создаем диалог выбора клиента
        client_dialog = QDialog(self)
        client_dialog.setWindowTitle("Выберите клиента")
        client_dialog.setStyleSheet("QDialog { background-color: #f8f9fa; }")
        client_layout = QVBoxLayout()
        
        client_combo = QComboBox()
        clients = Client.get_all()
        for client in clients:
            client_combo.addItem(client.name, client.id)
        
        button_layout = QHBoxLayout()
        ok_btn = QPushButton("✔️ OK")
        cancel_btn = QPushButton("❌ Отмена")
        
        ok_btn.clicked.connect(client_dialog.accept)
        cancel_btn.clicked.connect(client_dialog.reject)
        
        button_layout.addWidget(ok_btn)
        button_layout.addWidget(cancel_btn)
        
        client_layout.addWidget(QLabel("Выберите клиента для нового заказа:"))
        client_layout.addWidget(client_combo)
        client_layout.addLayout(button_layout)
        
        client_dialog.setLayout(client_layout)
        
        if client_dialog.exec_() == QDialog.Accepted:
            client_id = client_combo.currentData()
            order = Order(client_id=client_id, order_date=QDate.currentDate().toString("yyyy-MM-dd"))
            order.save()
            self.load_orders()
            self.load_order_details(order.id)
            QMessageBox.information(self, "Успех", "✅ Заказ успешно создан")
    
    def delete_order(self):
        selected = self.order_table.currentRow()
        if selected >= 0:
            order_id = int(self.order_table.item(selected, 0).text())
            order = Order.get_by_id(order_id)
            if order:
                order.delete()
                self.load_orders()
                self.clear_order_details()
                QMessageBox.information(self, "Успех", "✅ Заказ успешно удален")
    
    def manage_order_items(self):
        selected = self.order_table.currentRow()
        if selected >= 0:
            order_id = int(self.order_table.item(selected, 0).text())
            order = Order.get_by_id(order_id)
            if order:
                self.open_order_items_dialog(order)
    
    def open_order_items_dialog(self, order):
        dialog = QDialog(self)
        dialog.setWindowTitle(f"🧩 Управление позициями заказа #{order.id}")
        dialog.resize(800, 600)
        dialog.setStyleSheet("QDialog { background-color: #f8f9fa; }")
        
        layout = QVBoxLayout()
        
        # Таблица позиций
        self.order_items_dialog_table = QTableWidget()
        self.order_items_dialog_table.setColumnCount(5)
        self.order_items_dialog_table.setHorizontalHeaderLabels(["ID", "Товар", "Количество", "Цена", "Сумма"])
        self.order_items_dialog_table.setSortingEnabled(True)
        self.order_items_dialog_table.setStyleSheet("""
            QTableWidget {
                gridline-color: #d6d9dc;
            }
            QTableWidget:item:selected {
                background-color: #e8f0fe;
            }
        """)
        layout.addWidget(self.order_items_dialog_table)
        
        # Форма добавления
        form_group = QGroupBox("➕ Добавить товар")
        form_layout = QHBoxLayout()
        
        self.product_type = QComboBox()
        self.product_type.addItems(["Консоль", "Аксессуар"])
        self.product_type.currentIndexChanged.connect(self.update_products_list)
        
        self.product_combo = QComboBox()
        self.quantity_spin = QSpinBox()
        self.quantity_spin.setRange(1, 100)
        
        add_btn = QPushButton("Добавить")
        add_btn.setStyleSheet("QPushButton { background-color: #28a745; color: white; }")
        add_btn.clicked.connect(lambda: self.add_order_item(order, dialog))
        
        form_layout.addWidget(self.product_type)
        form_layout.addWidget(self.product_combo)
        form_layout.addWidget(QLabel("Кол-во:"))
        form_layout.addWidget(self.quantity_spin)
        form_layout.addWidget(add_btn)
        
        form_group.setLayout(form_layout)
        layout.addWidget(form_group)
        
        # Кнопки управления
        button_layout = QHBoxLayout()
        remove_btn = QPushButton("❌ Удалить выбранную позицию")
        remove_btn.setStyleSheet("QPushButton { background-color: #dc3545; color: white; }")
        remove_btn.clicked.connect(lambda: self.remove_order_item(order, dialog))
        close_btn = QPushButton("❌ Закрыть")
        close_btn.setStyleSheet("QPushButton { background-color: #6c757d; color: white; }")
        close_btn.clicked.connect(dialog.close)
        
        button_layout.addWidget(remove_btn)
        button_layout.addStretch()
        button_layout.addWidget(close_btn)
        
        layout.addLayout(button_layout)
        
        dialog.setLayout(layout)
        
        # Загружаем товары
        self.load_order_items(order)
        self.update_products_list()
        
        dialog.exec_()
    
    def update_products_list(self):
        self.product_combo.clear()
        if self.product_type.currentText() == "Консоль":
            consoles = Console.get_all()
            for console in consoles:
                self.product_combo.addItem(console.name, console.id)
        else:
            accessories = Accessory.get_all()
            for accessory in accessories:
                console = Console.get_by_id(accessory.console_id)
                console_name = console.name if console else "Неизвестная консоль"
                self.product_combo.addItem(f"{accessory.name} ({console_name})", accessory.id)
    
    def load_order_items(self, order):
        items = order.get_items()
        self.order_items_dialog_table.setRowCount(len(items))
        total = 0
        for row, item in enumerate(items):
            self.order_items_dialog_table.setItem(row, 0, QTableWidgetItem(str(item.id)))
            
            if item.console_id:
                console = Console.get_by_id(item.console_id)
                self.order_items_dialog_table.setItem(row, 1, QTableWidgetItem(console.name if console else "Неизвестная консоль"))
            else:
                accessory = Accessory.get_by_id(item.accessory_id)
                self.order_items_dialog_table.setItem(row, 1, QTableWidgetItem(accessory.name if accessory else "Неизвестный аксессуар"))
            
            self.order_items_dialog_table.setItem(row, 2, QTableWidgetItem(str(item.quantity)))
            self.order_items_dialog_table.setItem(row, 3, QTableWidgetItem(f"{item.price:.2f} ₽"))
            self.order_items_dialog_table.setItem(row, 4, QTableWidgetItem(f"{item.price * item.quantity:.2f} ₽"))
            
            total += item.price * item.quantity
        
        # Обновляем общую сумму заказа
        order.total_amount = total
        order.save()
        
        # Обновляем отображение
        self.load_orders()
        self.load_order_details(order.id)
    
    def add_order_item(self, order, dialog):
        product_id = self.product_combo.currentData()
        quantity = self.quantity_spin.value()
        
        if product_id:
            if self.product_type.currentText() == "Консоль":
                order.add_item(console_id=product_id, quantity=quantity)
            else:
                order.add_item(accessory_id=product_id, quantity=quantity)
            
            self.quantity_spin.setValue(1)
            self.load_order_items(order)
    
    def remove_order_item(self, order, dialog):
        selected = self.order_items_dialog_table.currentRow()
        if selected >= 0:
            item_id = int(self.order_items_dialog_table.item(selected, 0).text())
            order.remove_item(item_id)
            self.load_order_items(order)
    
    def load_order_details(self, order_id):
        order = Order.get_by_id(order_id)
        if order:
            items = order.get_items()
            self.order_items_table.setRowCount(len(items))
            total = 0
            
            for row, item in enumerate(items):
                if item.console_id:
                    console = Console.get_by_id(item.console_id)
                    self.order_items_table.setItem(row, 0, QTableWidgetItem(console.name if console else "Неизвестная консоль"))
                else:
                    accessory = Accessory.get_by_id(item.accessory_id)
                    self.order_items_table.setItem(row, 0, QTableWidgetItem(accessory.name if accessory else "Неизвестный аксессуар"))
                
                self.order_items_table.setItem(row, 1, QTableWidgetItem(str(item.quantity)))
                self.order_items_table.setItem(row, 2, QTableWidgetItem(f"{item.price:.2f} ₽"))
                self.order_items_table.setItem(row, 3, QTableWidgetItem(f"{item.price * item.quantity:.2f} ₽"))
                
                total += item.price * item.quantity
            
            self.total_amount.setText(f"{total:.2f} ₽")
            self.total_amount.setStyleSheet("color: #28a745; font-size: 14px;")
    
    def clear_order_details(self):
        self.order_items_table.setRowCount(0)
        self.total_amount.setText("0.00 ₽")
        self.total_amount.setStyleSheet("color: #28a745; font-size: 14px;")