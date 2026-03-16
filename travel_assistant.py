"""
AI Travel Voice Assistant - Local Model Version
No API required - Uses local ML models and datasets
"""

import speech_recognition as sr
import pyttsx3
import os
import sys
from typing import List, Dict
import pandas as pd
from transformers import pipeline
import warnings
warnings.filterwarnings('ignore')

class TravelVoiceAssistant:
    def __init__(self):
        """Initialize the travel voice assistant with local models."""
        print("\n🚀 Initializing Travel Voice Assistant (Local Mode)...\n")
        
        # Initialize speech recognition
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Initialize text-to-speech
        self.tts_engine = pyttsx3.init()
        self.tts_engine.setProperty('rate', 165)
        self.tts_engine.setProperty('volume', 0.9)
        
        # Load travel dataset
        print("📊 Loading travel knowledge dataset...")
        self.travel_data = self.load_travel_dataset()
        print(f"✅ Loaded {len(self.travel_data)} travel destinations\n")
        
        # Initialize local language model
        print("🤖 Loading local AI model (this may take a minute)...")
        try:
            self.qa_pipeline = pipeline(
                "text2text-generation",
                model="google/flan-t5-small",
                device=-1
            )
            print("✅ AI model loaded successfully!\n")
        except Exception as e:
            print(f"⚠️  Could not load transformer model: {e}")
            print("Falling back to rule-based responses...\n")
            self.qa_pipeline = None
        
        # Conversation history
        self.conversation_history: List[Dict[str, str]] = []
        
        # Calibrate microphone
        print("🎤 Calibrating microphone for ambient noise...")
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=2)
        print("✅ Microphone calibrated!\n")
    
    def load_travel_dataset(self) -> pd.DataFrame:
        """Load travel destinations dataset from CSV file."""
        csv_path = './travel_data/travel_destinations.csv'
        
        if os.path.exists(csv_path):
            print(f"📂 Loading dataset from: {csv_path}")
            df = pd.read_csv(csv_path)
            return df
        
        print("⚠️  CSV not found. Using sample dataset.")
        print("💡 Run 'python create_dataset.py' to create full dataset\n")
        
        travel_data = {
            'destination': [
                'Thailand', 'Italy', 'Japan', 'France', 'Spain', 
                'Greece', 'Vietnam', 'Mexico', 'India', 'Turkey'
            ],
            'food': [
                'Pad Thai, Tom Yum, Mango Sticky Rice, incredible street food',
                'Pizza, Pasta, Gelato, Risotto, regional Italian cuisine',
                'Sushi, Ramen, Tempura, Yakitori, traditional kaiseki',
                'Croissants, Cheese, Wine, French pastries, fine dining',
                'Paella, Tapas, Jamón Ibérico, fresh seafood',
                'Moussaka, Gyros, Greek salad, fresh Mediterranean cuisine',
                'Pho, Banh Mi, Spring Rolls, amazing street food culture',
                'Tacos, Mole, Tamales, vibrant street food scene',
                'Curry, Biryani, Dosa, incredibly diverse regional cuisines',
                'Kebabs, Baklava, Turkish breakfast, mezze platters'
            ],
            'best_time': [
                'November to February (cool and dry)',
                'April to June, September to October (mild weather)',
                'March to May, September to November (cherry blossoms)',
                'April to June, September to October (pleasant weather)',
                'May to June, September to October (warm)',
                'April to June, September to October (beautiful weather)',
                'February to April, August to October (dry season)',
                'December to April (dry season)',
                'October to March (cooler weather)',
                'April to May, September to October (mild temperatures)'
            ],
            'highlights': [
                'Beautiful beaches, temples, vibrant nightlife, island hopping',
                'Ancient ruins, art museums, beautiful architecture',
                'Traditional temples, modern cities, Mount Fuji, hot springs',
                'Eiffel Tower, Louvre Museum, wine regions, villages',
                'Gothic architecture, beaches, flamenco, vibrant culture',
                'Ancient ruins, stunning islands, white-washed villages',
                'Halong Bay, ancient towns, beautiful landscapes',
                'Mayan ruins, beaches, colorful culture, cenotes',
                'Taj Mahal, palaces, diverse landscapes, spiritual sites',
                'Historic sites, hot air balloons, bazaars, coastal beauty'
            ],
            'budget': [
                'Low to Medium ($30-60/day)',
                'Medium to High ($80-150/day)',
                'Medium to High ($70-130/day)',
                'Medium to High ($90-160/day)',
                'Medium ($60-110/day)',
                'Medium ($50-100/day)',
                'Low ($25-50/day)',
                'Low to Medium ($40-80/day)',
                'Low ($20-50/day)',
                'Low to Medium ($35-70/day)'
            ]
        }
        
        return pd.DataFrame(travel_data)
    
    def speak(self, text: str):
        """Convert text to speech and play it."""
        print(f"\n🤖 Assistant: {text}\n")
        self.tts_engine.say(text)
        self.tts_engine.runAndWait()
    
    def listen(self) -> str:
        """Listen to user's voice input and convert to text."""
        with self.microphone as source:
            print("🎤 Listening... (speak now)")
            try:
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=15)
                print("🔄 Processing your speech...")
                
                text = self.recognizer.recognize_google(audio)
                print(f"👤 You said: {text}")
                return text
            
            except sr.WaitTimeoutError:
                print("⏱️  No speech detected. Please try again.")
                return ""
            except sr.UnknownValueError:
                print("❌ Sorry, I couldn't understand that. Please try again.")
                return ""
            except sr.RequestError as e:
                print(f"❌ Speech recognition error: {e}")
                return ""
    
    def search_destinations(self, query: str) -> List[Dict]:
        """Search travel dataset based on query keywords."""
        query_lower = query.lower()
        results = []
        
        for idx, row in self.travel_data.iterrows():
            destination = row['destination'].lower()
            
            if destination in query_lower:
                results.append({
                    'destination': row['destination'],
                    'food': row['food'],
                    'best_time': row['best_time'],
                    'highlights': row['highlights'],
                    'budget': row['budget'],
                    'relevance': 10
                })
        
        results.sort(key=lambda x: x['relevance'], reverse=True)
        return results[:3]
    
    def generate_response(self, user_query: str) -> str:
        """Generate response using dataset."""
        search_results = self.search_destinations(user_query)
        query_lower = user_query.lower()
        
        if 'food' in query_lower or 'eat' in query_lower:
            return self.generate_food_response(search_results)
        elif 'when' in query_lower or 'time' in query_lower:
            return self.generate_timing_response(search_results)
        elif 'budget' in query_lower or 'cheap' in query_lower:
            return self.generate_budget_response(search_results)
        else:
            return self.generate_general_response(search_results)
    
    def generate_food_response(self, results: List[Dict]) -> str:
        """Generate response about food."""
        if not results:
            return "I'd love to help with food recommendations! Could you mention a specific destination?"
        
        return f"For amazing food experiences, I'd recommend {results[0]['destination']}! You must try: {results[0]['food']}."
    
    def generate_timing_response(self, results: List[Dict]) -> str:
        """Generate response about timing."""
        if not results:
            return "Which destination are you interested in?"
        
        dest = results[0]['destination']
        time = results[0]['best_time']
        return f"The best time to visit {dest} is {time}. Perfect weather for exploring!"
    
    def generate_budget_response(self, results: List[Dict]) -> str:
        """Generate response about budget."""
        if not results:
            return "For budget-friendly travel, I recommend Vietnam, Thailand, or India!"
        
        dest = results[0]['destination']
        budget = results[0]['budget']
        return f"For {dest}, you're looking at approximately {budget}."
    
    def generate_general_response(self, results: List[Dict]) -> str:
        """Generate general response."""
        if results:
            dest = results[0]['destination']
            highlights = results[0]['highlights']
            return f"I highly recommend {dest}! {highlights} What would you like to know more about?"
        
        return "I can help you plan your travels! Ask me about destinations, food, timing, or budget."
    
    def run(self):
        """Run the voice assistant main loop."""
        print("=" * 70)
        print("🌍 AI TRAVEL VOICE ASSISTANT 🌍".center(70))
        print("=" * 70)
        print("\nCommands: 'exit', 'quit', or 'goodbye' to end")
        print("=" * 70)
        
        self.speak("Hello! I'm your travel assistant. How can I help you plan your adventure?")
        
        while True:
            try:
                user_input = self.listen()
                
                if not user_input:
                    continue
                
                if user_input.lower() in ['exit', 'quit', 'goodbye', 'bye']:
                    self.speak("Safe travels! Goodbye!")
                    print("\n👋 Session ended.\n")
                    break
                
                print("\n💭 Thinking...")
                response = self.generate_response(user_input)
                self.speak(response)
                
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!\n")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")


def main():
    """Main function."""
    print("\n" + "="*70)
    print("TRAVEL VOICE ASSISTANT - LOCAL MODE".center(70))
    print("="*70)
    print("\n✅ No API keys required!")
    print("✅ Uses local datasets and models\n")
    print("="*70 + "\n")
    
    try:
        assistant = TravelVoiceAssistant()
        assistant.run()
    except Exception as e:
        print(f"\n❌ Failed to start: {e}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()