from database.db_manager import get_connection

class Console:
    def __init__(self, id=None, name=None, manufacturer=None, release_year=None, price=None, stock=None, description=None):
        self.id = id
        self.name = name
        self.manufacturer = manufacturer
        self.release_year = release_year
        self.price = price
        self.stock = stock
        self.description = description

    def save(self):
        conn = get_connection()
        cursor = conn.cursor()
        
        if self.id is None:
            cursor.execute("""
            INSERT INTO consoles (name, manufacturer, release_year, price, stock, description)
            VALUES (?, ?, ?, ?, ?, ?)
            """, (self.name, self.manufacturer, self.release_year, self.price, self.stock, self.description))
            self.id = cursor.lastrowid
        else:
            cursor.execute("""
            UPDATE consoles SET name=?, manufacturer=?, release_year=?, 
                            price=?, stock=?, description=?
            WHERE id=?
            """, (self.name, self.manufacturer, self.release_year, 
                  self.price, self.stock, self.description, self.id))
        
        conn.commit()
        conn.close()

    def delete(self):
        if self.id:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM consoles WHERE id=?", (self.id,))
            conn.commit()
            conn.close()

    @staticmethod
    def get_all():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM consoles")
        rows = cursor.fetchall()
        conn.close()
        return [Console(*row) for row in rows]

    @staticmethod
    def get_by_id(console_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM consoles WHERE id=?", (console_id,))
        row = cursor.fetchone()
        conn.close()
        return Console(*row) if row else None