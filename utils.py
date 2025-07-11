import requests
import time
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('APIKEY')
BASE_URL = 'https://maps.googleapis.com/maps/api/place/textsearch/json'


def get_insurance_brokers_by_city(cities, keywords):
    results = {}

    for city in cities:
        results[city] = []  # Initialize empty list for each city

        for keyword in keywords:
            query = f"{keyword} insurance in {city}"
            params = {
                'query': query,
                'key': API_KEY
            }

            response = requests.get(BASE_URL, params=params)
            data = response.json()

            for place in data.get("results", []):
                name = place.get("name")
                rating = place.get("rating")
                reviews = place.get("user_ratings_total")

                results[city].append({
                    "keyword": keyword,
                    "name": name,
                    "rating": rating,
                    "reviews": reviews
                })

            time.sleep(1)  # avoid hitting API rate limits

    return results


def find_target_rank_by_city_and_keyword(results_by_city, target_kewords):
    target_ranks = {}

    for city, places in results_by_city.items():
        # Group places by keyword
        places_by_keyword = {}
        for place in places:
            keyword = place.get("keyword", "unknown")
            places_by_keyword.setdefault(keyword, []).append(place)

        for keyword, keyword_places in places_by_keyword.items():
            found_rank = None
            matched_name = None
            matched_rating = None
            matched_reviews = None

            for i, place in enumerate(keyword_places, start=1):
                name = place["name"]
                rating = place.get("rating")
                reviews = place.get("reviews")
                name_lower = name.lower()
                if any(target in name_lower for target in target_kewords):
                    found_rank = i
                    matched_name = name
                    matched_rating = rating
                    matched_reviews = reviews
                    break

            # Use a tuple key (city, keyword)
            target_ranks[(city, keyword)] = {
                "rank": found_rank,
                "name": matched_name,
                "rating": matched_rating,
                "reviews": matched_reviews
            }

    return target_ranks


def export_to_excel(target_ranks, filename='output.xlsx'):
    # Convert the dictionary to a list of rows
    data = []
    for (city, keyword), info in target_ranks.items():
        data.append({
            'City': city,
            'Keyword': keyword,
            'Rank': info.get('rank', 'None'),
            'Rating': info.get('rating', 'None'),
            'Reviews': info.get('reviews', 'None')
        })

    # Create a DataFrame
    df = pd.DataFrame(data)
    df = df.fillna('None')

    # Export to Excel
    df.to_excel(filename, index=False)
    print(f"Exported to {filename}")
