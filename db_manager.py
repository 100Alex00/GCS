import sqlite3
from config import DB_NAME

def get_connection():
    return sqlite3.connect(DB_NAME)

def initialize_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    # Таблица игровых консолей
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS consoles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        manufacturer TEXT NOT NULL,
        release_year INTEGER,
        price REAL NOT NULL,
        stock INTEGER NOT NULL,
        description TEXT
    )
    ''')
    
    # Таблица аксессуаров
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS accessories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        console_id INTEGER,
        price REAL NOT NULL,
        stock INTEGER NOT NULL,
        FOREIGN KEY (console_id) REFERENCES consoles(id)
    )
    ''')
    
    # Таблица клиентов
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS clients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT,
        phone TEXT NOT NULL,
        address TEXT
    )
    ''')
    
    # Таблица заказов
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        client_id INTEGER,
        order_date DATE NOT NULL,
        total_amount REAL DEFAULT 0,
        FOREIGN KEY (client_id) REFERENCES clients(id)
    )
    ''')
    
    # Таблица элементов заказа
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS order_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER,
        console_id INTEGER,
        accessory_id INTEGER,
        quantity INTEGER NOT NULL,
        price REAL NOT NULL,
        FOREIGN KEY (order_id) REFERENCES orders(id),
        FOREIGN KEY (console_id) REFERENCES consoles(id),
        FOREIGN KEY (accessory_id) REFERENCES accessories(id)
    )
    ''')
    
    conn.commit()
    conn.close()