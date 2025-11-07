from app import db
from app.models.city_model import City
from sqlalchemy import text

class CityUseCase:
    pagination = None

    def get_list_city(self, page=1, page_size=10):
        # Try to get from cache first
        cached_data = City.get_cached_cities(page, page_size)
        if cached_data:
            self.pagination = cached_data.get('pagination')
            return cached_data.get('data')

        # Calculate offset
        offset = (page - 1) * page_size
        
        # For SQL Server, we need to use ORDER BY with OFFSET/FETCH
        cities = City.query.order_by(City.id).offset(offset).limit(page_size).all()
        total_count = City.query.count()

        if not cities:
            return None

        result = [city.to_dict() for city in cities]

        # Calculate pagination info manually
        total_pages = (total_count + page_size - 1) // page_size  # Ceiling division

        self.pagination = {
            "page": page,
            "per_page": page_size,
            "pages": total_pages,
            "total": total_count,
        }

        # Cache the result
        cache_data = {
            "data": result,
            "pagination": self.pagination
        }
        City.set_cached_cities(cache_data, page, page_size)
        
        return result

    def get_city_by_id(self, city_id):
        # Try cache first
        cached_city = City.get_cached_city(city_id)
        if cached_city:
            return cached_city

        # Query database
        city = City.query.get(city_id)
        if not city:
            return None

        result = city.to_dict()
        
        # Cache the result
        City.set_cached_city(result, city_id)
        
        return result
    
    def create_city(self, name, country):
        city = City(name=name, country=country)
        db.session.add(city)
        db.session.commit()

        # Invalidate cache when new data is added
        City.invalidate_cities_cache()
        
        return city.to_dict()  
    
    def update_city(self, city_id, name, country):
        city = City.query.get(city_id)
        if not city:
            return None
        
        city.name = name
        city.country = country
        db.session.commit()

        # Invalidate cache when data is updated
        City.invalidate_cities_cache()
        
        return city.to_dict()
    
    def delete_city(self, city_id):
        city = City.query.get(city_id)
        if not city:
            return None
        
        db.session.delete(city)
        db.session.commit()

        # Invalidate cache when data is deleted
        City.invalidate_cities_cache()
        
        return {"message": "City deleted successfully"}