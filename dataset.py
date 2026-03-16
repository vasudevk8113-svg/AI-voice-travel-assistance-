import pandas as pd
import os
from pathlib import Path

def create_travel_dataset():
    """Create comprehensive travel dataset."""
    print("\n" + "="*70)
    print("TRAVEL DATASET CREATOR".center(70))
    print("="*70 + "\n")
    
    print("📝 Creating curated travel dataset...")
    
    travel_data = {
        'destination': [
            'Thailand', 'Italy', 'Japan', 'France', 'Spain', 'Greece',
            'Vietnam', 'Mexico', 'India', 'Turkey', 'Portugal', 'Indonesia',
            'Morocco', 'Peru', 'Egypt', 'Brazil', 'Croatia', 'New Zealand',
            'Iceland', 'South Korea', 'Argentina', 'Costa Rica', 'Netherlands',
            'Switzerland', 'Norway', 'Australia', 'Austria', 'Ireland',
            'United Kingdom', 'Germany', 'Canada', 'Chile', 'Colombia'
        ],
        'food': [
            'Pad Thai, Tom Yum, Mango Sticky Rice, street food',
            'Pizza, Pasta, Gelato, Risotto, Italian cuisine',
            'Sushi, Ramen, Tempura, Yakitori, kaiseki',
            'Croissants, Cheese, Wine, French pastries',
            'Paella, Tapas, Jamón Ibérico, fresh seafood',
            'Moussaka, Gyros, Greek salad, Mediterranean cuisine',
            'Pho, Banh Mi, Spring Rolls, street food',
            'Tacos, Mole, Tamales, street food',
            'Curry, Biryani, Dosa, regional cuisines',
            'Kebabs, Baklava, Turkish breakfast, mezze',
            'Bacalhau, Pastéis de Nata, seafood, Port wine',
            'Nasi Goreng, Satay, Rendang, tropical fruits',
            'Tagine, Couscous, Mint tea, spices',
            'Ceviche, Lomo Saltado, Peruvian fusion',
            'Koshari, Falafel, Ful medames, Egyptian food',
            'Feijoada, Pão de Queijo, Açaí, Churrasco',
            'Fresh seafood, Truffles, Peka, Croatian wine',
            'Lamb, Seafood, Pavlova, Hangi feast',
            'Fresh fish, Lamb, Skyr, Nordic cuisine',
            'Korean BBQ, Kimchi, Bibimbap, Street food',
            'Asado, Empanadas, Dulce de Leche, Malbec',
            'Gallo Pinto, Casado, Fresh tropical fruits',
            'Stroopwafels, Cheese, Herring, Indonesian cuisine',
            'Fondue, Rösti, Chocolate, Alpine cuisine',
            'Fresh seafood, Brunost cheese, Nordic food',
            'BBQ, Meat pies, Vegemite, Fresh seafood',
            'Wiener Schnitzel, Sachertorte, Coffee',
            'Irish stew, Soda bread, Guinness, Seafood',
            'Fish and chips, Roast dinner, Afternoon tea',
            'Bratwurst, Pretzels, Beer, Sauerkraut',
            'Poutine, Maple syrup, Tourtière, Fresh salmon',
            'Empanadas, Pastel de choclo, Fresh seafood',
            'Arepas, Bandeja paisa, Fresh coffee, Empanadas'
        ],
        'best_time': [
            'November to February', 'April to June, September to October',
            'March to May, September to November', 'April to June, September to October',
            'May to June, September to October', 'April to June, September to October',
            'February to April, August to October', 'December to April',
            'October to March', 'April to May, September to October',
            'March to May, September to October', 'April to October',
            'March to May, September to November', 'April to November',
            'October to April', 'December to March',
            'May to September', 'December to February',
            'June to August', 'March to May, September to November',
            'September to November, March to May', 'December to April',
            'April to September', 'June to September',
            'May to September', 'September to February',
            'April to October', 'May to September',
            'May to September', 'May to September',
            'May to September', 'December to March',
            'December to March'
        ],
        'highlights': [
            'Beautiful beaches, temples, vibrant nightlife',
            'Ancient ruins, art museums, beautiful architecture',
            'Traditional temples, modern cities, Mount Fuji',
            'Eiffel Tower, Louvre Museum, wine regions',
            'Gothic architecture, beaches, flamenco',
            'Ancient ruins, stunning islands, white villages',
            'Halong Bay, ancient towns, landscapes',
            'Mayan ruins, beaches, colorful culture',
            'Taj Mahal, palaces, diverse landscapes',
            'Historic sites, hot air balloons, bazaars',
            'Historic cities, beaches, wine valleys',
            'Bali beaches, temples, rice terraces',
            'Medinas, Sahara desert, Atlas mountains',
            'Machu Picchu, Amazon rainforest, Andes',
            'Pyramids, Nile River, ancient temples',
            'Amazon rainforest, Iguazu Falls, Rio beaches',
            'Plitvice Lakes, Dubrovnik walls, islands',
            'Fjords, glaciers, Hobbiton, adventure sports',
            'Northern lights, glaciers, waterfalls',
            'Modern cities, ancient palaces, DMZ',
            'Wine regions, Patagonia, Iguazu Falls',
            'Rainforests, beaches, volcanoes, wildlife',
            'Canals, museums, tulip fields, windmills',
            'Alps, lakes, charming villages, skiing',
            'Fjords, northern lights, Viking history',
            'Great Barrier Reef, Outback, Sydney Opera',
            'Vienna, Salzburg, Alps, classical music',
            'Cliffs of Moher, Dublin, Ring of Kerry',
            'London, Stonehenge, Scottish Highlands',
            'Berlin Wall, Neuschwanstein, Rhine Valley',
            'Niagara Falls, Rocky Mountains, Quebec',
            'Torres del Paine, Atacama Desert, Easter Island',
            'Cartagena, Coffee region, Amazon rainforest'
        ],
        'budget': [
            'Low to Medium ($30-60/day)', 'Medium to High ($80-150/day)',
            'Medium to High ($70-130/day)', 'Medium to High ($90-160/day)',
            'Medium ($60-110/day)', 'Medium ($50-100/day)',
            'Low ($25-50/day)', 'Low to Medium ($40-80/day)',
            'Low ($20-50/day)', 'Low to Medium ($35-70/day)',
            'Low to Medium ($45-90/day)', 'Low to Medium ($30-70/day)',
            'Low to Medium ($35-75/day)', 'Low to Medium ($40-80/day)',
            'Low to Medium ($30-65/day)', 'Low to Medium ($40-85/day)',
            'Medium ($55-105/day)', 'Medium to High ($75-140/day)',
            'High ($100-180/day)', 'Medium ($50-95/day)',
            'Low to Medium ($45-90/day)', 'Medium ($50-100/day)',
            'Medium to High ($70-130/day)', 'High ($120-200/day)',
            'High ($110-190/day)', 'Medium to High ($80-150/day)',
            'Medium to High ($75-140/day)', 'Medium to High ($85-155/day)',
            'Medium to High ($80-150/day)', 'Medium to High ($70-140/day)',
            'Medium to High ($80-160/day)', 'Medium ($50-100/day)',
            'Low to Medium ($40-85/day)'
        ]
    }
    
    df = pd.DataFrame(travel_data)
    
    # Create directory
    data_dir = Path('./travel_data')
    data_dir.mkdir(exist_ok=True)
    
    # Save to CSV
    output_path = data_dir / 'travel_destinations.csv'
    df.to_csv(output_path, index=False)
    
    print(f"✅ Dataset saved to: {output_path}")
    print(f"📊 Total destinations: {len(df)}")
    
    print("\n" + "="*70)
    print("DATASET PREVIEW".center(70))
    print("="*70)
    print(df.head(10))
    print("\n" + "="*70)
    print(f"✅ Dataset ready with {len(df)} destinations!")
    print("="*70 + "\n")
    
    return df


if __name__ == "__main__":
    create_travel_dataset()