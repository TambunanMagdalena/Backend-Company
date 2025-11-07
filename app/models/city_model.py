from app import db, get_redis
import json

class City(db.Model):
    __tablename__ = 'cities'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    country = db.Column(db.String(100))

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "country": self.country
        }

    @classmethod
    def get_cached_cities(cls, page=1, page_size=10):
        """Get cities from cache"""
        redis_client = get_redis()
        if not redis_client:
            return None
            
        cache_key = f"cities:page:{page}:size:{page_size}"
        cached = redis_client.get(cache_key)
        
        if cached:
            print(f"✅ Cache HIT: {cache_key}")
            return json.loads(cached)
        
        print(f"❌ Cache MISS: {cache_key}")
        return None

    @classmethod
    def set_cached_cities(cls, data, page=1, page_size=10):
        """Set cities to cache"""
        redis_client = get_redis()
        if not redis_client:
            return
            
        cache_key = f"cities:page:{page}:size:{page_size}"
        redis_client.setex(cache_key, 300, json.dumps(data))  # Cache 5 minutes
        print(f"💾 Cache SET: {cache_key}")

    @classmethod
    def get_cached_city(cls, city_id):
        """Get single city from cache"""
        redis_client = get_redis()
        if not redis_client:
            return None
            
        cache_key = f"city:{city_id}"
        cached = redis_client.get(cache_key)
        
        if cached:
            print(f"✅ Cache HIT: {cache_key}")
            return json.loads(cached)
        
        print(f"❌ Cache MISS: {cache_key}")
        return None

    @classmethod
    def set_cached_city(cls, city_data, city_id):
        """Set single city to cache"""
        redis_client = get_redis()
        if not redis_client:
            return
            
        cache_key = f"city:{city_id}"
        redis_client.setex(cache_key, 300, json.dumps(city_data))  # Cache 5 minutes
        print(f"💾 Cache SET: {cache_key}")

    @classmethod
    def invalidate_cities_cache(cls):
        """Invalidate all cities cache"""
        redis_client = get_redis()
        if not redis_client:
            return
            
        # Delete all cities cache patterns
        keys = redis_client.keys("cities:page:*")
        keys += redis_client.keys("city:*")
        
        if keys:
            redis_client.delete(*keys)
            print(f"🗑️  Cache CLEARED: {len(keys)} keys")