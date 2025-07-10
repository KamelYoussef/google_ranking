import requests
import time

#API_KEY =
BASE_URL = 'https://maps.googleapis.com/maps/api/place/textsearch/json'

TARGET_KEYWORDS = [
    'western financial',
    'western coast',
    'wyatt dowling'
]

def get_insurance_brokers_by_city(cities):
    results = {}

    for city in cities:
        query = f"broker insurance in {city}"
        params = {
            'query': query,
            'key': API_KEY
        }

        response = requests.get(BASE_URL, params=params)
        data = response.json()

        city_results = []
        for place in data.get("results", []):
            name = place.get("name")
            rating = place.get("rating")
            reviews = place.get("user_ratings_total")
            city_results.append({
                "name": name,
                "rating": rating,
                "reviews": reviews
            })

        results[city] = city_results

        time.sleep(1)  # avoid rate limit

    return results


def find_target_rank_in_cities(results_by_city):
    target_ranks = {}

    for city, places in results_by_city.items():
        found_rank = None
        matched_name = None
        matched_rating = None
        matched_reviews = None

        for i, place in enumerate(places, start=1):
            name = place["name"]
            rating = place.get("rating")
            reviews = place.get("reviews")
            name_lower = name.lower()
            if any(keyword in name_lower for keyword in TARGET_KEYWORDS):
                found_rank = i
                matched_name = name
                matched_rating = rating
                matched_reviews = reviews
                break

        target_ranks[city] = {
            "rank": found_rank,
            "name": matched_name,
            "rating": matched_rating,
            "reviews": matched_reviews
        }

    return target_ranks


# Example usage
cities = ['Okotoks', 'calgary']
results = get_insurance_brokers_by_city(cities)
print(results)
ranks = find_target_rank_in_cities(results)
print(ranks)
