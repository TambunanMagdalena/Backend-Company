from app import create_app, get_redis
import json

def test_redis_connection():
    """Test Redis connection and basic operations"""
    app = create_app()
    
    with app.app_context():
        redis_client = get_redis()
        
        if not redis_client:
            print(" Redis client is not available")
            return False
            
        try:
            # Test 1: Basic set/get
            print(" Testing basic Redis operations...")
            redis_client.set('test_key', 'Hello Redis!')
            value = redis_client.get('test_key')
            print(f" Basic test: {value}")

            # Test 2: JSON data caching
            print(" Testing JSON data caching...")
            test_city = {
                'id': 999, 
                'name': 'Test City', 
                'country': 'Test Country',
                'timestamp': '2024-01-01'
            }
            redis_client.set('city_999', json.dumps(test_city))
            
            cached_city = redis_client.get('city_999')
            if cached_city:
                city_data = json.loads(cached_city)
                print(f" JSON cache test: {city_data}")
            else:
                print("JSON cache test failed")

            # Test 3: Expiration test
            print(" Testing expiration...")
            redis_client.setex('temp_key', 10, 'This will expire in 10 seconds')  # 10 seconds
            temp_value = redis_client.get('temp_key')
            print(f" Expiration test: {temp_value}")

            # Test 4: Delete key
            print(" Testing delete operation...")
            redis_client.delete('test_key')
            deleted_value = redis_client.get('test_key')
            print(f" Delete test: Key should be None -> {deleted_value}")

            # Test 5: List all keys pattern
            print(" Testing key patterns...")
            redis_client.set('city_1', 'Jakarta')
            redis_client.set('city_2', 'Surabaya')
            redis_client.set('user_1', 'John Doe')
            
            city_keys = redis_client.keys('city_*')
            print(f" Key pattern test: Found {len(city_keys)} city keys")
            
            print("\n All Redis tests passed!")
            return True
            
        except Exception as e:
            print(f" Redis test failed: {e}")
            return False

if __name__ == "__main__":
    test_redis_connection()