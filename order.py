from database.db_manager import get_connection
from models.order_item import OrderItem
from datetime import date
from models.console import Console
from models.accessory import Accessory

class Order:
    def __init__(self, id=None, client_id=None, order_date=None, total_amount=0.0):
        self.id = id
        self.client_id = client_id
        self.order_date = order_date
        self.total_amount = total_amount

    def save(self):
        conn = get_connection()
        cursor = conn.cursor()
        
        if self.id is None:
            cursor.execute("""
            INSERT INTO orders (client_id, order_date, total_amount)
            VALUES (?, ?, ?)
            """, (self.client_id, self.order_date, self.total_amount))
            self.id = cursor.lastrowid
        else:
            cursor.execute("""
            UPDATE orders SET client_id=?, order_date=?, total_amount=?
            WHERE id=?
            """, (self.client_id, self.order_date, self.total_amount, self.id))
        
        conn.commit()
        conn.close()

    def delete(self):
        if self.id:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM orders WHERE id=?", (self.id,))
            conn.commit()
            conn.close()

    def add_item(self, console_id=None, accessory_id=None, quantity=1):
        if console_id:
            console = Console.get_by_id(console_id)
            if not console or console.stock < quantity:
                print("❌ Недостаточно товара на складе")
                return
            
            item = OrderItem(
                order_id=self.id,
                console_id=console_id,
                accessory_id=None,
                quantity=quantity,
                price=console.price
            )
            
            console.stock -= quantity
            console.save()
            
        elif accessory_id:
            accessory = Accessory.get_by_id(accessory_id)
            if not accessory or accessory.stock < quantity:
                print("❌ Недостаточно товара на складе")
                return
            
            item = OrderItem(
                order_id=self.id,
                console_id=None,
                accessory_id=accessory_id,
                quantity=quantity,
                price=accessory.price
            )
            
            accessory.stock -= quantity
            accessory.save()
            
        else:
            print("❌ Не указан товар или аксессуар")
            return
            
        item.save()
        self.total_amount += item.price * item.quantity
        self.save()

    def remove_item(self, item_id):
        item = OrderItem.get_by_id(item_id)
        if item and item.order_id == self.id:
            if item.console_id:
                console = Console.get_by_id(item.console_id)
                console.stock += item.quantity
                console.save()
            elif item.accessory_id:
                accessory = Accessory.get_by_id(item.accessory_id)
                accessory.stock += item.quantity
                accessory.save()
                
            self.total_amount -= item.price * item.quantity
            self.save()
            item.delete()

    def get_items(self):
        return OrderItem.get_by_order(self.id)

    @staticmethod
    def get_all():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM orders")
        rows = cursor.fetchall()
        conn.close()
        return [Order(*row) for row in rows]

    @staticmethod
    def get_by_id(order_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM orders WHERE id=?", (order_id,))
        row = cursor.fetchone()
        conn.close()
        return Order(*row) if row else None