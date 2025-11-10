# streamlit_app.py
import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# Konfigirasyon paj la
st.set_page_config(
    page_title="Boutik Entèlijan Kreyòl",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

def init_database():
    """Inisyalize database a"""
    conn = sqlite3.connect('boutique.db', check_same_thread=False)
    cursor = conn.cursor()
    
    # Kreye tab pwodwi yo
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
    
    # Kreye tab kontak yo
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            non TEXT NOT NULL,
            pozisyon TEXT,
            telefon TEXT,
            email TEXT
        )
    ''')
    
    # Kreye tab kòmand yo
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS commandes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_nom TEXT,
            client_email TEXT,
            produits TEXT,
            total REAL,
            statut TEXT DEFAULT 'en attente',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Verifye si gen done deja
    cursor.execute('SELECT COUNT(*) FROM produits')
    count_produits = cursor.fetchone()[0]
    
    if count_produits == 0:
        # Ajoute pwodwi egzanp
        produits = [
            ('Diri', 'Diri blan bon kalite pou tout plat', 75.00, 50, 'debaz', '🫒'),
            ('Pwa', 'Pwa wouj fre ak bon gou', 60.00, 30, 'debaz', '🫘'),
            ('Lwil', 'Lwil mayi pou kwit manje', 120.00, 20, 'kondiman', '🫗'),
            ('Sik', 'Sik kristal pou prepare jus ak kafe', 45.00, 40, 'debaz', '🍬'),
            ('Kafe', 'Kafe Ayisyen bon kalite', 150.00, 15, 'bwason', '☕'),
            ('Bannann', 'Bannann mi pou fri oswa bouyi', 25.00, 100, 'legim', '🍌'),
            ('Patat', 'Patat dou pou bouyi oswa fri', 30.00, 80, 'legim', '🍠'),
            ('Sabon', 'Sabon pou lave men ak kò', 35.00, 60, 'entètye', '🧼'),
            ('Dlo', 'Dlo potab an bwat', 40.00, 45, 'bwason', '💧'),
            ('Let', 'Let an poud pou timoun', 85.00, 25, 'lètye', '🥛'),
            ('Fromaj', 'Fromaj lokal bon gou', 95.00, 20, 'lètye', '🧀'),
            ('Poul', 'Poul fre pou kwit', 200.00, 10, 'vyann', '🍗'),
            ('Pwason', 'Pwason fre nan mache', 180.00, 8, 'vyann', '🐟'),
            ('Zoranj', 'Zoranj fre pou jus', 15.00, 70, 'fwi', '🍊')
        ]
        
        cursor.executemany('''
            INSERT INTO produits (nom, description, prix, quantite, categorie, image_url)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', produits)
    
    cursor.execute('SELECT COUNT(*) FROM contacts')
    count_contacts = cursor.fetchone()[0]
    
    if count_contacts == 0:
        contacts = [
            ('Jean Pierre', 'Responsab Vant', '+509 1234-5678', 'jean@boutik.ht'),
            ('Marie Claude', 'Sèvis Kliyan', '+509 8765-4321', 'marie@boutik.ht'),
            ('Pierre Louis', 'Manager Jeneral', '+509 5555-6666', 'pierre@boutik.ht')
        ]
        
        cursor.executemany('''
            INSERT INTO contacts (non, pozisyon, telefon, email)
            VALUES (?, ?, ?, ?)
        ''', contacts)
    
    conn.commit()
    conn.close()

class ChatbotKreyol:
    def __init__(self):
        self.responses = {
            'bonjou': ['Bonjou! Kijan mwen ka ede w jodi a?', 'Bonjou! Sa mwen ka fè pou w?'],
            'bonsoir': ['Bonswa! Kijan nou ka sèvi w?', 'Bonswa! Mwen la pou ede w.'],
            'mesi': ['Mesi! Èske gen yon lòt bagay mwen ka ede w?', 'Pa gen pwoblèm!', 'Se pa anyen!'],
            'bye': ['Orevwa! Èske w ta renmen fè yon lòt kòmand?', 'Orevwa! Kenbe w la!', 'Orevwa! Mèsi pou vizit ou!']
        }
    
    def get_produits(self):
        conn = sqlite3.connect('boutique.db', check_same_thread=False)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM produits WHERE quantite > 0 ORDER BY nom')
        produits = cursor.fetchall()
        conn.close()
        return produits
    
    def get_produit_by_name(self, nom):
        conn = sqlite3.connect('boutique.db', check_same_thread=False)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM produits WHERE nom LIKE ? AND quantite > 0', (f'%{nom}%',))
        produit = cursor.fetchone()
        conn.close()
        return produit
    
    def get_contacts(self):
        conn = sqlite3.connect('boutique.db', check_same_thread=False)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM contacts')
        contacts = cursor.fetchall()
        conn.close()
        return contacts
    
    def search_produits(self, keyword):
        conn = sqlite3.connect('boutique.db', check_same_thread=False)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM produits 
            WHERE (nom LIKE ? OR description LIKE ? OR categorie LIKE ?) 
            AND quantite > 0
            ORDER BY nom
        ''', (f'%{keyword}%', f'%{keyword}%', f'%{keyword}%'))
        produits = cursor.fetchall()
        conn.close()
        return produits
    
    def get_categories(self):
        conn = sqlite3.connect('boutique.db', check_same_thread=False)
        cursor = conn.cursor()
        cursor.execute('SELECT DISTINCT categorie FROM produits WHERE quantite > 0')
        categories = [row[0] for row in cursor.fetchall()]
        conn.close()
        return categories
    
    def analyze_sentiment(self, message):
        message = message.lower()
        positive_words = ['bon', 'kontan', 'fèm', 'byen', 'mèsi', 'èlijan', 'bèl', 'ekselan', 'super', 'bèl bagay']
        negative_words = ['pa bon', 'fache', 'dekouraje', 'pwoblèm', 'pa ka', 'move', 'pa kontan', 'trist', 'dezagreyab']
        
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
            return self.search_produits("Kafe") or self.search_produits("bwason")[:3]
        elif sentiment == "trist":
            return self.search_produits("Sik") or self.search_produits("dous")[:3]
        else:
            return self.get_produits()[:4]
    
    def process_message(self, message):
        message_lower = message.lower()
        response = ""
        recommendations = []
        
        # Analize sentiman
        sentiment = self.analyze_sentiment(message)
        
        # Chèche pri
        if any(word in message_lower for word in ['pri', 'koute', 'kob', 'valè', 'konben', 'pri']):
            produits_trouves = []
            for produit in self.get_produits():
                if any(word in message_lower for word in produit[1].lower().split()):
                    produits_trouves.append(produit)
            
            if produits_trouves:
                if len(produits_trouves) == 1:
                    prod = produits_trouves[0]
                    response = f"{prod[6]} **{prod[1]}** koute **{prod[3]:.2f} goud**. Nou gen **{prod[4]}** nan depo."
                else:
                    response = "**Pwodwi yo ak pri yo:**\n\n"
                    for prod in produits_trouves[:5]:
                        response += f"{prod[6]} **{prod[1]}** - {prod[3]:.2f} goud\n"
            else:
                response = "Ki pwodwi w ta renmen konnen pri a? Mwen ka chèche pou w."
        
        # Chèche disponiblite
        elif any(word in message_lower for word in ['gen', 'disponib', 'ki genyen', 'èske gen', 'disponible']):
            for produit in self.get_produits():
                if any(word in message_lower for word in produit[1].lower().split()):
                    if produit[4] > 0:
                        response = f"✅ **Wi**, nou gen {produit[6]} **{produit[1]}** disponib. Pri: **{produit[3]:.2f} goud**"
                    else:
                        response = f"❌ **Non**, {produit[6]} **{produit[1]}** pa disponib kounye a."
                    break
            if not response:
                response = "Ki pwodwi w vle konnen si li disponib? Tape non pwodwi a."
        
        # Kontak
        elif any(word in message_lower for word in ['kontak', 'telefon', 'email', 'pale ak', 'moun', 'sipò']):
            contacts = self.get_contacts()
            response = "**📞 Moun pou kontakte nan boutik la:**\n\n"
            for contact in contacts:
                response += f"• **{contact[1]}** ({contact[2]})\n  📞 {contact[3]}\n  📧 {contact[4]}\n\n"
        
        # Rekòmandasyon
        elif any(word in message_lower for word in ['sijere', 'rekòmande', 'kisa', 'ki kalite', 'ide', 'suggerer']):
            recommendations = self.get_recommendations_by_sentiment(sentiment)
            if recommendations:
                response = f"**💡 Dapre santiman w, mwen rekòmande pou w:**"
            else:
                response = "Mwen pa jwenn pwodwi pou rekòmande kounye a."
        
        # Lis tout pwodwi
        elif any(word in message_lower for word in ['lis', 'tout', 'ki pwodwi', 'katalog', 'produits', 'lis pwodwi']):
            produits = self.get_produits()
            response = "**🛍️ Tout pwodwi nou yo:**\n\n"
            for prod in produits[:10]:
                response += f"{prod[6]} **{prod[1]}** - {prod[3]:.2f} goud ({prod[4]} disponib)\n"
            if len(produits) > 10:
                response += f"\n... ak {len(produits) - 10} lòt pwodwi. Chèche yon pwodwi espesifik!"
        
        # Kategori
        elif any(word in message_lower for word in ['kategori', 'kategorie', 'kalite', 'type']):
            categories = self.get_categories()
            response = "**📂 Kategori pwodwi nou yo:**\n\n"
            for cat in categories:
                produits_cat = self.search_produits(cat)
                response += f"• **{cat}** ({len(produits_cat)} pwodwi)\n"
        
        # Si pa gen repons espesifik
        if not response:
            for key, replies in self.responses.items():
                if key in message_lower:
                    import random
                    response = random.choice(replies)
                    break
            
            if not response:
                response = "🤔 Mwen pa byen konprann. Èske w ta ka repete oswa poze yon lòt kesyon? Ou kapab mande m:\n• Pri yon pwodwi\n• Si yon pwodwi disponib\n• Kontak boutik la\n• Rekòmandasyon"
        
        return {
            'response': response,
            'sentiment': sentiment,
            'recommendations': recommendations
        }

# Inisyalizasyon
init_database()
chatbot = ChatbotKreyol()

# Entèfas prensipal
def main():
    # Sidebar
    with st.sidebar:
        st.image("https://via.placeholder.com/150x50/2c5aa0/ffffff?text=Boutik+Kreyol", width=150)
        st.title("🛒 Boutik Entèlijan")
        st.markdown("---")
        
        st.markdown("### ⚡ Aksè rapid")
        if st.button("🏠 Paj Dakò"):
            st.session_state.current_tab = "Akèy"
        if st.button("💬 Chat ak Bot"):
            st.session_state.current_tab = "Chat"
        if st.button("🛍️ Katalog"):
            st.session_state.current_tab = "Pwodwi"
        
        st.markdown("---")
        st.markdown("### 📞 Èd rapid")
        contacts = chatbot.get_contacts()
        for contact in contacts[:2]:
            st.markdown(f"**{contact[1]}**")
            st.caption(f"{contact[3]}")
        
        st.markdown("---")
        st.markdown("### 📊 Statistik")
        produits = chatbot.get_produits()
        st.metric("Pwodwi Disponib", len(produits))
        total_quantite = sum(prod[4] for prod in produits)
        st.metric("Total Atik", total_quantite)
    
    # Kontni prensipal
    st.title("🛒 Boutik Entèlijan an Kreyòl")
    st.markdown("**Boutik manje ki konprann santiman w ak sèvis an Kreyòl!**")
    
    # Onglet yo
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["🏠 Akèy", "💬 Chat", "🛍️ Pwodwi", "📞 Kontak", "ℹ️ Sou Nou"])
    
    with tab1:
        st.header("🎯 Byenveni nan Boutik Entèlijan nou an!")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🌟 Poukisa nou?")
            st.markdown("""
            - ✅ **Pwodwi kalite** ak pri ki jis
            - 💬 **Sèvis an Kreyòl** pou w konfòtab
            - 🤖 **Asistan entèlijan** ki konprann santiman w
            - 🚚 **Livrezon rapid** nan zòn nou kouvri
            - 🛒 **Fasil pou kòmande** ak tout kalite peman
            """)
            
            st.subheader("🚀 Komanse kounye a")
            st.markdown("""
            1. 💬 **Chat** ak asistan nou an pou w jwenn enfòmasyon
            2. 🛍️ **Chwazi** pwodwi w renmen yo
            3. 📞 **Kontakte** nou pou w fini kòmand ou
            4. 🎉 **Resevwa** pwodwi ou yo lakay ou!
            """)
        
        with col2:
            st.subheader("📈 Pwodwi Popilè")
            produits_populaires = chatbot.get_produits()[:6]
            for prod in produits_populaires:
                with st.container():
                    col_a, col_b = st.columns([1, 3])
                    with col_a:
                        st.markdown(f"## {prod[6]}")
                    with col_b:
                        st.markdown(f"**{prod[1]}**")
                        st.markdown(f"*{prod[3]:.2f} goud*")
                        st.progress(min(prod[4] / 100, 1.0), text=f"{prod[4]} disponib")
                    st.markdown("---")
    
    with tab2:
        st.header("💬 Chat ak Asistan Nou an")
        st.markdown("Pale ak chatbot nou an an **Kreyòl** pou w jwenn enfòmasyon sou pwodwi, pri, ak plis!")
        
        # Inisyalize istorik chat
        if "messages" not in st.session_state:
            st.session_state.messages = [
                {"role": "assistant", "content": "👋 Bonjou! Mwen se asistan boutik la. Kijan mwen ka ede w jodi a? Mwen kapab reponn kesyon sou pri, disponiblite, ak sijere pwodwi!"}
            ]
        
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
            with st.spinner("Asistan an ap chèche repons pou w..."):
                result = chatbot.process_message(prompt)
            
            # Ajoute repons chatbot
            with st.chat_message("assistant"):
                st.markdown(result['response'])
                
                # Montre rekòmandasyon si genyen
                if result['recommendations']:
                    st.markdown("**🛒 Pwodwi rekòmande:**")
                    for prod in result['recommendations']:
                        with st.container():
                            st.markdown(f"{prod[6]} **{prod[1]}** - {prod[3]:.2f} goud")
                
                # Montre sentiman
                sentiment_emoji = {
                    "kontan": "😊 Kliyan kontan",
                    "trist": "😔 Kliyan tris", 
                    "net": "😐 Santiman net"
                }
                st.caption(f"**{sentiment_emoji[result['sentiment']]}**")
            
            st.session_state.messages.append({"role": "assistant", "content": result['response']})
            
            # Opsyon pou efase konvèsasyon an
            if st.button("🗑️ Efase konvèsasyon an", key="clear_chat"):
                st.session_state.messages = [
                    {"role": "assistant", "content": "👋 Konvèsasyon an efase! Kijan mwen ka ede w?"}
                ]
                st.rerun()
    
    with tab3:
        st.header("🛍️ Katalog Pwodwi Nou Yo")
        
        # Filtre ak rechèch
        col1, col2 = st.columns([2, 1])
        
        with col1:
            search_term = st.text_input("🔍 Chèche yon pwodwi...", placeholder="Ekri non yon pwodwi (egzanp: diri, pwa, kafe)")
        
        with col2:
            categories = chatbot.get_categories()
            selected_category = st.selectbox("📂 Filtre pa kategori", ["Tout kategori"] + categories)
        
        # Aplikasyon filtè yo
        if search_term:
            produits = chatbot.search_produits(search_term)
            st.subheader(f"🔍 Rezilta pou: '{search_term}'")
        elif selected_category != "Tout kategori":
            produits = chatbot.search_produits(selected_category)
            st.subheader(f"📂 Kategori: {selected_category}")
        else:
            produits = chatbot.get_produits()
            st.subheader("🛍️ Tout pwodwi disponib")
        
        # Montre pwodwi yo
        if not produits:
            st.warning("❌ Pa gen pwodwi ki koresponn ak kritè chèche ou yo.")
        else:
            st.markdown(f"**{len(produits)} pwodwi jwenn**")
            
            # Kreye kat pwodwi yo
            cols = st.columns(3)
            for idx, produit in enumerate(produits):
                with cols[idx % 3]:
                    with st.container():
                        st.markdown(f"### {produit[6]} {produit[1]}")
                        st.markdown(f"*{produit[2]}*")
                        st.markdown(f"**💰 Pri:** {produit[3]:.2f} goud")
                        st.markdown(f"**📦 Kantite:** {produit[4]} disponib")
                        st.markdown(f"**📂 Kategori:** {produit[5]}")
                        
                        # Endikateur disponiblite
                        if produit[4] > 20:
                            st.success("✅ An stock")
                        elif produit[4] > 0:
                            st.warning("⚠️ Stock limite")
                        else:
                            st.error("❌ Stock epuize")
                        
                        st.markdown("---")
    
    with tab4:
        st.header("📞 Kontak Nou")
        
        contacts = chatbot.get_contacts()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("👥 Ekip Nou an")
            for contact in contacts:
                with st.container():
                    st.markdown(f"### {contact[1]}")
                    st.markdown(f"**{contact[2]}**")
                    st.markdown(f"📞 **Telefòn:** {contact[3]}")
                    st.markdown(f"📧 **Email:** {contact[4]}")
                    st.markdown("---")
        
        with col2:
            st.subheader("📋 Fòm Kontak")
            
            with st.form("contact_form"):
                st.markdown("**Voye yon mesaj dirèkteman**")
                nom = st.text_input("Non konplè ou")
                email = st.text_input("Adrès imèl ou")
                sujet = st.selectbox("Sijè", ["Kesyon sou pwodwi", "Pwoblèm ak kòmand", "Sijesyon", "Lòt"])
                mesaj = st.text_area("Mesaj ou")
                
                submitted = st.form_submit_button("📤 Voye Mesaj")
                if submitted:
                    if nom and email and mesaj:
                        st.success("✅ Mesaj ou voye ak sikse! Nou pral reponn ou nan 24 èdtan.")
                    else:
                        st.error("❌ Tanpri ranpli tout chan yo.")
            
            st.subheader("📍 Enfòmasyon Boutik")
            st.markdown("""
            **🏢 Adrès fizik:**
            123 Avenue de la Liberté
            Port-au-Prince, Haiti
            
            **🕒 Lè ouvèti:**
            Lendi nan Vandredi: 8:00 AM - 6:00 PM
            Samdi: 8:00 AM - 4:00 PM
            Dimanch: Fèmen
            
            **📞 Nimewo Ansekirans:**
            +509 1234-5678
            """)
    
    with tab5:
        st.header("ℹ️ Sou Boutik Nou an")
        
        st.markdown("""
        ## 🎯 Boutik Entèlijan an Kreyòl
        
        ### 👨‍💼 Misyon Nou
        Nou vle fè komès elektwonik apwocheb pou tout Ayisyen atravè yon platfòm ki pale lang nou, 
        ki konprann kilti nou, epi ki adapte ak bezwen nou yo.
        
        ### 🌟 Sa Nou Fè
        - **🛒 Komès Elektwonik Aksesib**: Boutik anliy ki fasil pou itilize
        - **💬 Kominikasyon an Kreyòl**: Tout entèaksyon an lang matènèl nou
        - **🤖 Teknoloji Entèlijan**: Chatbot ki konprann santiman kliyan
        - **🚚 Sèvis Lokal**: Adapte pou kontèks Ayisyen
        
        ### 🔧 Teknoloji Dèyè Boutik la
        - **Python** ak **Streamlit** pou entèfas la
        - **SQLite** pou estoke done
        - **Algoritm Sentiman** pou rekòmandasyon pèsonalize
        - **Chatbot Kreyòl** pou konvèsasyon natirèl
        
        ### 📞 Kontribye
        Se yon pwojè ouvè! Si w vle kontribye:
        - ⭐ Sou GitHub: [github.com/username/boutik-kreyol](https://github.com/username/boutik-kreyol)
        - 💡 Sijere karakteristik nouvo
        - 🐟 Signale bug oswa pwoblèm
        
        *Nou kwè ke teknoloji dwe sèvi pèp la nan lang li pi byen konprann!*
        """)
        
        # Metrik boutik la
        st.subheader("📊 Statistik Boutik")
        col1, col2, col3, col4 = st.columns(4)
        
        produits = chatbot.get_produits()
        categories = chatbot.get_categories()
        contacts_list = chatbot.get_contacts()
        
        with col1:
            st.metric("Pwodwi Total", len(produits))
        with col2:
            st.metric("Kategori", len(categories))
        with col3:
            st.metric("Anplwaye", len(contacts_list))
        with col4:
            total_value = sum(prod[3] * prod[4] for prod in produits)
            st.metric("Valè Stock", f"{total_value:,.0f} G")

if __name__ == "__main__":
    main()
