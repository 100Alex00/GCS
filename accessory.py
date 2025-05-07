from database.db_manager import get_connection

class Accessory:
    def __init__(self, id=None, name=None, console_id=None, price=None, stock=None):
        self.id = id
        self.name = name
        self.console_id = console_id
        self.price = price
        self.stock = stock

    def save(self):
        conn = get_connection()
        cursor = conn.cursor()
        
        if self.id is None:
            cursor.execute("""
            INSERT INTO accessories (name, console_id, price, stock)
            VALUES (?, ?, ?, ?)
            """, (self.name, self.console_id, self.price, self.stock))
            self.id = cursor.lastrowid
        else:
            cursor.execute("""
            UPDATE accessories SET name=?, console_id=?, price=?, stock=?
            WHERE id=?
            """, (self.name, self.console_id, self.price, self.stock, self.id))
        
        conn.commit()
        conn.close()

    def delete(self):
        if self.id:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM accessories WHERE id=?", (self.id,))
            conn.commit()
            conn.close()

    @staticmethod
    def get_all():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM accessories")
        rows = cursor.fetchall()
        conn.close()
        return [Accessory(*row) for row in rows]

    @staticmethod
    def get_by_id(accessory_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM accessories WHERE id=?", (accessory_id,))
        row = cursor.fetchone()
        conn.close()
        return Accessory(*row) if row else None

    @staticmethod
    def get_by_console(console_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM accessories WHERE console_id=?", (console_id,))
        rows = cursor.fetchall()
        conn.close()
        return [Accessory(*row) for row in rows]