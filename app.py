import streamlit as st
import sqlite3
from datetime import datetime
import re

# Konfigirasyon paj la
st.set_page_config(
    page_title="Boutik Entèlijan Kreyòl",
    page_icon="🛒",
    layout="wide"
)

# Inisyalizasyon database
def init_database():
    conn = sqlite3.connect('boutique.db')
    cursor = conn.cursor()
    
    # Kreye tab si yo pa egziste
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
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            non TEXT NOT NULL,
            pozisyon TEXT,
            telefon TEXT,
            email TEXT
        )
    ''')
    
    # Ajoute done egzanp
    produits = [
        ('Diri', 'Diri blan bon kalite', 75.00, 50, 'debaz'),
        ('Pwa', 'Pwa wouj fre', 60.00, 30, 'debaz'),
        ('Lwil', 'Lwil mayi', 120.00, 20, 'kondiman'),
        ('Sik', 'Sik kristal', 45.00, 40, 'debaz'),
        ('Kafe', 'Kafe Ayisyen', 150.00, 15, 'bwason'),
        ('Bannann', 'Bannann mi', 25.00, 100, 'legim'),
        ('Patat', 'Patat dou', 30.00, 80, 'legim'),
        ('Sabon', 'Sabon pou lave men', 35.00, 60, 'entètye'),
        ('Dlo', 'Dlo potab', 40.00, 45, 'bwason')
    ]
    
    cursor.executemany('''
        INSERT OR IGNORE INTO produits (nom, description, prix, quantite, categorie)
        VALUES (?, ?, ?, ?, ?)
    ''', produits)
    
    contacts = [
        ('Neize Sadrac', 'Responsab Vant', '+50912345678', 'nsadrac@boutique.ht'),
        ('Phito Dorjuste, 'Sèvis Kliyan', '+509'8785674', 'dphito@boutique.ht'),
        ('Harold Narcisse', 'Manager', '+50955556666', 'hnarcisse@boutique.ht')
    ]
    
    cursor.executemany('''
        INSERT OR IGNORE INTO contacts (non, pozisyon, telefon, email)
        VALUES (?, ?, ?, ?)
    ''', contacts)
    
    conn.commit()
    conn.close()

# Klas Chatbot
class ChatbotKreyol:
    def __init__(self):
        self.responses = {
            'bonjou': ['Bonjou! Kijan mwen ka ede w jodi a?', 'Bonjou! Sa mwen ka fè pou w?'],
            'mesi': ['Mesi! Èske gen yon lòt bagay mwen ka ede w?', 'Pa gen pwoblèm!'],
            'bye': ['Orevwa! Èske w ta renmen fè yon lòt kòmand?', 'Orevwa! Kenbe w la!']
        }
    
    def get_produits(self):
        conn = sqlite3.connect('boutique.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM produits WHERE quantite > 0')
        produits = cursor.fetchall()
        conn.close()
        return produits
    
    def get_produit_by_name(self, nom):
        conn = sqlite3.connect('boutique.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM produits WHERE nom LIKE ? AND quantite > 0', (f'%{nom}%',))
        produit = cursor.fetchone()
        conn.close()
        return produit
    
    def get_contacts(self):
        conn = sqlite3.connect('boutique.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM contacts')
        contacts = cursor.fetchall()
        conn.close()
        return contacts
    
    def search_produits(self, keyword):
        conn = sqlite3.connect('boutique.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM produits 
            WHERE (nom LIKE ? OR description LIKE ? OR categorie LIKE ?) 
            AND quantite > 0
        ''', (f'%{keyword}%', f'%{keyword}%', f'%{keyword}%'))
        produits = cursor.fetchall()
        conn.close()
        return produits
    
    def analyze_sentiment(self, message):
        message = message.lower()
        positive_words = ['bon', 'kontan', 'fèm', 'byen', 'mèsi', 'èlijan', 'bèl', 'ekselan']
        negative_words = ['pa bon', 'fache', 'dekouraje', 'pwoblèm', 'pa ka', 'move', 'pa kontan']
        
        positive_count = sum(1 for word in positive_words if word in message)
        negative_count = sum(1 for word in negative_words if word in message)
        
        if positive_count > negative_count:
            return "kontan"
        elif negative_count > positive_count:
            return "trist"
        else:
            return "net"
    
    def get_recommendations_by_sentiment(self, sentiment):
        if sentiment == "kontan":
            return self.search_produits("Kafe") or self.search_produits("bwason")
        elif sentiment == "trist":
            return self.search_produits("Sik") or self.search_produits("dous")
        else:
            return self.get_produits()[:3]
    
    def process_message(self, message):
        message_lower = message.lower()
        response = ""
        recommendations = []
        
        # Analize sentiman
        sentiment = self.analyze_sentiment(message)
        
        # Chèche pri
        if any(word in message_lower for word in ['pri', 'koute', 'kob', 'valè', 'konben']):
            for produit in self.get_produits():
                if any(word in message_lower for word in produit[1].lower().split()):
                    response = f"🛒 **{produit[1]}** koute **{produit[3]} goud**. Nou gen **{produit[4]}** nan depo."
                    break
            if not response:
                response = "Ki pwodwi w ta renmen konnen pri a? Mwen ka chèche pou w."
        
        # Chèche disponiblite
        elif any(word in message_lower for word in ['gen', 'disponib', 'ki genyen', 'èske gen']):
            for produit in self.get_produits():
                if any(word in message_lower for word in produit[1].lower().split()):
                    if produit[4] > 0:
                        response = f"✅ **Wi**, nou gen **{produit[1]}** disponib. Pri: **{produit[3]} goud**"
                    else:
                        response = f"❌ **Non**, **{produit[1]}** pa disponib kounye a."
                    break
            if not response:
                response = "Ki pwodwi w vle konnen si li disponib?"
        
        # Kontak
        elif any(word in message_lower for word in ['kontak', 'telefon', 'email', 'pale ak', 'moun']):
            contacts = self.get_contacts()
            response = "**📞 Moun pou kontakte:**\n\n"
            for contact in contacts:
                response += f"• **{contact[1]}** ({contact[2]}): {contact[3]} - {contact[4]}\n"
        
        # Rekòmandasyon
        elif any(word in message_lower for word in ['sijere', 'rekòmande', 'kisa', 'ki kalite', 'ide']):
            recommendations = self.get_recommendations_by_sentiment(sentiment)
            if recommendations:
                response = f"**💡 Dapre santiman w, mwen rekòmande pou w:**"
            else:
                response = "Mwen pa jwenn pwodwi pou rekòmande kounye a."
        
        # Lis tout pwodwi
        elif any(word in message_lower for word in ['lis', 'tout', 'ki pwodwi', 'katalog']):
            produits = self.get_produits()
            response = "**🛍️ Tout pwodwi nou yo:**\n\n"
            for prod in produits:
                response += f"• **{prod[1]}** - {prod[3]} goud ({prod[4]} disponib)\n"
        
        # Si pa gen repons espesifik
        if not response:
            for key, replies in self.responses.items():
                if key in message_lower:
                    response = replies[0]
                    break
            
            if not response:
                response = "🤔 Mwen pa byen konprann. Èske w ta ka repete oswa poze yon lòt kesyon?"
        
        return {
            'response': response,
            'sentiment': sentiment,
            'recommendations': recommendations
        }

# Inisyalizasyon
init_database()
chatbot = ChatbotKreyol()

# Entèfas Streamlit
def main():
    st.title("🛒 Boutik Entèlijan an Kreyòl")
    st.markdown("Boutik manje ki konprann santiman w ak sèvis an Kreyòl!")
    
    # Kreye onglet yo
    tab1, tab2, tab3, tab4 = st.tabs(["💬 Chat", "🛍️ Pwodwi", "📞 Kontak", "ℹ️ Sou Nou"])
    
    with tab1:
        st.header("Chat ak Asistan Nou an")
        st.markdown("Pale ak chatbot nou an an Kreyòl pou w jwenn enfòmasyon!")
        
        # Inisyalize istorik chat
        if "messages" not in st.session_state:
            st.session_state.messages = []
        
        # Montre istorik chat
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Input mesaj
        if prompt := st.chat_input("Tape mesaj ou an Kreyòl isit..."):
            # Ajoute mesaj kliyan an
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Jwenn repons chatbot
            result = chatbot.process_message(prompt)
            
            # Ajoute repons chatbot
            with st.chat_message("assistant"):
                st.markdown(result['response'])
                
                # Montre rekòmandasyon si genyen
                if result['recommendations']:
                    st.markdown("**Pwodwi rekòmande:**")
                    for prod in result['recommendations']:
                        st.markdown(f"• **{prod[1]}** - {prod[3]} goud")
                
                # Montre sentiman
                sentiment_emoji = "😊" if result['sentiment'] == "kontan" else "😔" if result['sentiment'] == "trist" else "😐"
                st.caption(f"Santiman detekte: {sentiment_emoji}")
            
            st.session_state.messages.append({"role": "assistant", "content": result['response']})
    
    with tab2:
        st.header("Katalog Pwodwi Nou Yo")
        
        # Bar rechèch
        search_term = st.text_input("Chèche yon pwodwi...", placeholder="Ekri non yon pwodwi")
        
        if search_term:
            produits = chatbot.search_produits(search_term)
            st.subheader(f"Rezilta pou: {search_term}")
        else:
            produits = chatbot.get_produits()
            st.subheader("Tout pwodwi disponib")
        
        # Montre pwodwi yo
        cols = st.columns(3)
        for idx, produit in enumerate(produits):
            with cols[idx % 3]:
                st.card()
                st.markdown(f"**{produit[1]}**")
                st.markdown(f"*{produit[2]}*")
                st.markdown(f"**Pri:** {produit[3]} goud")
                st.markdown(f"**Kantite:** {produit[4]}")
                st.markdown(f"**Kategori:** {produit[5]}")
    
    with tab3:
        st.header("Kontak Nou")
        contacts = chatbot.get_contacts()
        
        for contact in contacts:
            with st.expander(f"📞 {contact[1]} - {contact[2]}"):
                st.markdown(f"**Telefòn:** {contact[3]}")
                st.markdown(f"**Email:** {contact[4]}")
        
        st.info("📧 Ou kapab tou pose kesyon ou yo nan chat la!")
    
    with tab4:
        st.header("Sou Boutik Nou an")
        st.markdown("""
        ## 🎯 Boutik Entèlijan an Kreyòl
        
        **Nou ofri:**
        - ✅ Pwodwi manje kalite
        - 💬 Sèvis an Kreyòl
        - 🤖 Asistan entèlijan ki konprann santiman w
        - 🛒 Komande fasil
        
        **Fonksyonalite:**
        - Chèche pri ak disponiblite pwodwi
        - Jwenn rekòmandasyon pèsonalize
        - Kontakte èkíp nou an
        - Chat an Kreyòl ak chatbot
        
        *Nou la pou sèvi w pi byen!*
        """)

if __name__ == "__main__":
    main()
