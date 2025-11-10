import sqlite3
import datetime
import os

# Itilize yon chemen relatif pou database
DB_PATH = "boutique.db"

def init_database():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    # ... rès kòd laclass Database:
    def __init__(self, db_name="boutique.db"):
        self.db_name = db_name
        self.init_database()
    
    def init_database(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        # Tab pou pwodwi
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS produits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nom TEXT NOT NULL,
                description TEXT,
                prix REAL NOT NULL,
                quantite INTEGER NOT NULL,
                categorie TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tab pou kliyan
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS clients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                non TEXT NOT NULL,
                email TEXT UNIQUE,
                sentiment TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tab pou kontak
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS contacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                non TEXT NOT NULL,
                pozisyon TEXT,
                telefon TEXT,
                email TEXT
            )
        ''')
        
        # Ensère kèk done egzanp
        self.insert_sample_data(cursor)
        
        conn.commit()
        conn.close()
    
    def insert_sample_data(self, cursor):
        # Ajoute pwodwi egzanp
        produits = [
            ('Diri', 'Diri blan bon kalite', 75.00, 50, 'debaz'),
            ('Pwa', 'Pwa wouj fre', 60.00, 30, 'debaz'),
            ('Lwil', 'Lwil mayi', 120.00, 20, 'kondiman'),
            ('Sik', 'Sik kristal', 45.00, 40, 'debaz'),
            ('Kafe', 'Kafe Ayisyen', 150.00, 15, 'bwason'),
            ('Bannann', 'Bannann mi', 25.00, 100, 'legim'),
            ('Patat', 'Patat dou', 30.00, 80, 'legim')
        ]
        
        cursor.executemany('''
            INSERT OR IGNORE INTO produits (nom, description, prix, quantite, categorie)
            VALUES (?, ?, ?, ?, ?)
        ''', produits)
        
        # Ajoute kontak egzanp
        contacts = [
            ('Jean Pierre', 'Responsab Vant', '+50912345678', 'jean@boutique.ht'),
            ('Marie Claude', 'Sèvis Kliyan', '+50987654321', 'marie@boutique.ht')
        ]
        
        cursor.executemany('''
            INSERT OR IGNORE INTO contacts (non, pozisyon, telefon, email)
            VALUES (?, ?, ?, ?)
        ''', contacts)
    
    def get_produits(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM produits WHERE quantite > 0')
        produits = cursor.fetchall()
        conn.close()
        return produits
    
    def get_produit_by_name(self, nom):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM produits WHERE nom LIKE ? AND quantite > 0', (f'%{nom}%',))
        produit = cursor.fetchone()
        conn.close()
        return produit
    
    def get_contacts(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM contacts')
        contacts = cursor.fetchall()
        conn.close()
        return contacts
    
    def search_produits(self, keyword):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM produits 
            WHERE (nom LIKE ? OR description LIKE ? OR categorie LIKE ?) 
            AND quantite > 0
        ''', (f'%{keyword}%', f'%{keyword}%', f'%{keyword}%'))
        produits = cursor.fetchall()
        conn.close()
        return produits
