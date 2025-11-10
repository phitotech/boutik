import re
from database import Database

class ChatbotKreyol:
    def __init__(self):
        self.db = Database()
        self.responses = {
            'bonjou': ['Bonjou! Kijan mwen ka ede w jodi a?', 'Bonjou! Sa mwen ka fè pou w?'],
            'mesi': ['Mesi! Èske gen yon lòt bagay mwen ka ede w?', 'Pa gen pwoblèm!'],
            'bye': ['Orevwa! Èske w ta renmen fè yon lòt kòmand?', 'Orevwa! Kenbe w la!']
        }
    
    def analyze_sentiment(self, message):
        message = message.lower()
        positive_words = ['bon', 'kontan', 'fèm', 'byen', 'mèsi', 'èlijan']
        negative_words = ['pa bon', 'fache', 'dekouraje', 'pwoblèm', 'pa ka']
        
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
            return self.db.search_produits("Kafe") or self.db.search_produits("bwason")
        elif sentiment == "trist":
            return self.db.search_produits("Sik") or self.db.search_produits("dous")
        else:
            return self.db.get_produits()[:3]
    
    def process_message(self, message):
        message_lower = message.lower()
        response = ""
        recommendations = []
        
        # Analize sentiman
        sentiment = self.analyze_sentiment(message)
        
        # Chèche infòmasyon sou pwodwi
        if any(word in message_lower for word in ['pri', 'koute', 'kob', 'valè']):
            for produit in self.db.get_produits():
                if any(word in message_lower for word in produit[1].lower().split()):
                    response = f"{produit[1]} koute {produit[3]} goud. Nou gen {produit[4]} nan depo."
                    break
        
        # Chèche si pwodwi disponib
        elif any(word in message_lower for word in ['gen', 'disponib', 'ki genyen']):
            for produit in self.db.get_produits():
                if any(word in message_lower for word in produit[1].lower().split()):
                    if produit[4] > 0:
                        response = f"Wi, nou gen {produit[1]} disponib. Pri: {produit[3]} goud"
                    else:
                        response = f"Non, {produit[1]} pa disponib kounye a."
                    break
        
        # Kontak
        elif any(word in message_lower for word in ['kontak', 'telefon', 'email', 'pale ak']):
            contacts = self.db.get_contacts()
            response = "Moun pou kontakte:\n"
            for contact in contacts:
                response += f"{contact[1]} ({contact[2]}): {contact[3]} - {contact[4]}\n"
        
        # Rekòmandasyon selon sentiman
        elif any(word in message_lower for word in ['sijere', 'rekòmande', 'kisa', 'ki kalite']):
            recommendations = self.get_recommendations_by_sentiment(sentiment)
            response = f"Dapre santiman w, mwen rekòmande pou w:"
        
        # Si pa gen repons espesifik, bay repons jeneral
        if not response:
            for key, replies in self.responses.items():
                if key in message_lower:
                    response = replies[0]
                    break
            
            if not response:
                response = "Mwen pa byen konprann. Èske w ta ka repete oswa poze yon lòt kesyon?"
        
        return {
            'response': response,
            'sentiment': sentiment,
            'recommendations': recommendations
        }
