from database.db_manager import get_connection

class OrderItem:
    def __init__(self, id=None, order_id=None, console_id=None, accessory_id=None, quantity=1, price=0.0):
        self.id = id
        self.order_id = order_id
        self.console_id = console_id
        self.accessory_id = accessory_id
        self.quantity = quantity
        self.price = price

    def save(self):
        conn = get_connection()
        cursor = conn.cursor()
        
        if self.id is None:
            cursor.execute("""
            INSERT INTO order_items (order_id, console_id, accessory_id, quantity, price)
            VALUES (?, ?, ?, ?, ?)
            """, (self.order_id, self.console_id, self.accessory_id, self.quantity, self.price))
            self.id = cursor.lastrowid
        else:
            cursor.execute("""
            UPDATE order_items SET order_id=?, console_id=?, accessory_id=?, quantity=?, price=?
            WHERE id=?
            """, (self.order_id, self.console_id, self.accessory_id, self.quantity, self.price, self.id))
        
        conn.commit()
        conn.close()

    def delete(self):
        if self.id:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM order_items WHERE id=?", (self.id,))
            conn.commit()
            conn.close()

    @staticmethod
    def get_by_order(order_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM order_items WHERE order_id=?", (order_id,))
        rows = cursor.fetchall()
        conn.close()
        return [OrderItem(*row) for row in rows]

    @staticmethod
    def get_by_id(item_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM order_items WHERE id=?", (item_id,))
        row = cursor.fetchone()
        conn.close()
        return OrderItem(*row) if row else None