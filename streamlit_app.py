# streamlit_app.py
import streamlit as st
import sqlite3
import os
import pandas as pd
from datetime import datetime

# Konfigirasyon
st.set_page_config(
    page_title="Boutik Entèlijan Kreyòl",
    page_icon="🛒",
    layout="wide"
)

# Chemen database
DB_PATH = "boutique.db"

def init_database():
    """Inisyalize database a ak fòs"""
    try:
        conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        cursor = conn.cursor()
        
        # Tab pwodwi
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS produits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nom TEXT NOT NULL,
                description TEXT,
                prix REAL NOT NULL,
                quantite INTEGER NOT NULL,
                categorie TEXT,
                image_url TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tab kontak
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS contacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                non TEXT NOT NULL,
                pozisyon TEXT,
                telefon TEXT,
                email TEXT
            )
        ''')
        
        # Verifye si gen done
        cursor.execute('SELECT COUNT(*) FROM produits')
        if cursor.fetchone()[0] == 0:
            # Ajoute done egzanp
            produits = [
                ('Diri', 'Diri blan bon kalite', 75.00, 50, 'debaz', '🫒'),
                ('Pwa', 'Pwa wouj fre', 60.00, 30, 'debaz', '🫘'),
                ('Lwil', 'Lwil mayi', 120.00, 20, 'kondiman', '🫗'),
                ('Sik', 'Sik kristal', 45.00, 40, 'debaz', '🍬'),
                ('Kafe', 'Kafe Ayisyen', 150.00, 15, 'bwason', '☕')
            ]
            cursor.executemany('INSERT INTO produits (nom, description, prix, quantite, categorie, image_url) VALUES (?,?,?,?,?,?)', produits)
            
            contacts = [
                ('Jean Pierre', 'Responsab Vant', '+50912345678', 'jean@boutik.ht'),
                ('Marie Claude', 'Sèvis Kliyan', '+50987654321', 'marie@boutik.ht')
            ]
            cursor.executemany('INSERT INTO contacts (non, pozisyon, telefon, email) VALUES (?,?,?,?)', contacts)
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        st.error(f"Erè nan inisyalizasyon database: {e}")
        return False

# Klas Chatbot senp
class ChatbotKreyol:
    def __init__(self):
        self.responses = {
            'bonjou': 'Bonjou! Kijan mwen ka ede w?',
            'mesi': 'Mesi! Gen yon lòt bagay?',
            'bye': 'Orevwa! Kenbe w la!'
        }
    
    def get_produits(self):
        try:
            conn = sqlite3.connect(DB_PATH, check_same_thread=False)
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM produits WHERE quantite > 0')
            produits = cursor.fetchall()
            conn.close()
            return produits
        except:
            return []
    
    def process_message(self, message):
        message = message.lower()
        
        if 'pri' in message or 'konben' in message:
            produits = self.get_produits()
            for prod in produits:
                if any(word in message for word in prod[1].lower().split()):
                    return f"{prod[6]} {prod[1]} koute {prod[3]} goud"
            return "Ki pwodwi w vle konnen pri a?"
        
        elif 'disponib' in message or 'gen' in message:
            return "Nou gen anpil pwodwi disponib. Gade nan onglet 'Pwodwi'!"
        
        for key, response in self.responses.items():
            if key in message:
                return response
        
        return "Mwen pa konprann. Èske w ta ka repete?"

# Aplikasyon prensipal
def main():
    st.title("🛒 Boutik Entèlijan an Kreyòl")
    
    # Inisyalize database
    if init_database():
        st.success("✅ Database inisyalize ak sikse!")
    else:
        st.error("❌ Pwoblèm ak database")
        return
    
    chatbot = ChatbotKreyol()
    
    tab1, tab2, tab3 = st.tabs(["💬 Chat", "🛍️ Pwodwi", "📞 Kontak"])
    
    with tab1:
        st.header("Chat ak Bot")
        
        if "messages" not in st.session_state:
            st.session_state.messages = [{"role": "assistant", "content": "Bonjou! Kijan mwen ka ede w?"}]
        
        for msg in st.session_state.messages:
            st.chat_message(msg["role"]).write(msg["content"])
        
        if prompt := st.chat_input("Pale ak mwen..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            response = chatbot.process_message(prompt)
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun()
    
    with tab2:
        st.header("Pwodwi Nou Yo")
        produits = chatbot.get_produits()
        
        for prod in produits:
            col1, col2 = st.columns([1, 4])
            with col1:
                st.write(f"## {prod[6]}")
            with col2:
                st.write(f"**{prod[1]}** - {prod[3]} goud")
                st.write(f"*{prod[2]}*")
                st.write(f"Kantite: {prod[4]}")
            st.divider()
    
    with tab3:
        st.header("Kontak Nou")
        st.write("""
        **Jean Pierre** - Responsab Vant
        📞 +509 1234-5678
        📧 jean@boutik.ht
        
        **Marie Claude** - Sèvis Kliyan  
        📞 +509 8765-4321
        📧 marie@boutik.ht
        """)

if __name__ == "__main__":
    main()
