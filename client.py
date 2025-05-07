from database.db_manager import get_connection

class Client:
    def __init__(self, id=None, name=None, email=None, phone=None, address=None):
        self.id = id
        self.name = name
        self.email = email
        self.phone = phone
        self.address = address

    def save(self):
        conn = get_connection()
        cursor = conn.cursor()
        
        if self.id is None:
            cursor.execute("""
            INSERT INTO clients (name, email, phone, address)
            VALUES (?, ?, ?, ?)
            """, (self.name, self.email, self.phone, self.address))
            self.id = cursor.lastrowid
        else:
            cursor.execute("""
            UPDATE clients SET name=?, email=?, phone=?, address=?
            WHERE id=?
            """, (self.name, self.email, self.phone, self.address, self.id))
        
        conn.commit()
        conn.close()

    def delete(self):
        if self.id:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM clients WHERE id=?", (self.id,))
            conn.commit()
            conn.close()

    @staticmethod
    def get_all():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM clients")
        rows = cursor.fetchall()
        conn.close()
        return [Client(*row) for row in rows]

    @staticmethod
    def get_by_id(client_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM clients WHERE id=?", (client_id,))
        row = cursor.fetchone()
        conn.close()
        return Client(*row) if row else None