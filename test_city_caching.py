from app import create_app
from app.models.city_model import City
from app.usecases.city_use_case import CityUseCase

def test_city_caching():
    app = create_app()
    
    with app.app_context():
        print(" Testing City Caching Implementation...")
        
        city_uc = CityUseCase()
        
        # Test 1: Create city (should invalidate cache)
        print("\n1. Testing city creation...")
        new_city = city_uc.create_city("Bandung", "Indonesia")
        print(f" Created: {new_city}")
        
        # Test 2: Get cities (should cache)
        print("\n2. Testing get cities (first call - should cache)...")
        cities = city_uc.get_list_city(page=1, page_size=10)
        print(f" Cities: {len(cities)} items")
        
        # Test 3: Get cities again (should use cache)
        print("\n3. Testing get cities (second call - should use cache)...")
        cities_cached = city_uc.get_list_city(page=1, page_size=10)
        print(f" Cities from cache: {len(cities_cached)} items")
        
        # Test 4: Get single city
        print("\n4. Testing get single city...")
        city = city_uc.get_city_by_id(new_city['id'])
        print(f" Single city: {city}")
        
        # Test 5: Update city (should invalidate cache)
        print("\n5. Testing city update...")
        updated = city_uc.update_city(new_city['id'], "Bandung Updated", "Indonesia")
        print(f" Updated: {updated}")
        
        print("\n City caching test completed!")

if __name__ == "__main__":
    test_city_caching()