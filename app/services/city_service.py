from flask import jsonify, request
from app import db
from app.utils import response
from app.usecases.city_use_case import CityUseCase

def get_all_cities():
    try:
        page = request.args.get('page', default=1, type=int)
        page_size = request.args.get('page_size', default=10, type=int)

        cityUseCase = CityUseCase()
        cities = cityUseCase.get_list_city(page=page, page_size=page_size)

        if not cities:
            return response([], None, status="error", message="No data found.")

        # Return successful response
        return response(cities, cityUseCase.pagination, status="success", message="Request successful.")

    except Exception as e:
        return response([], None, status="error", message=f"An error occurred: {str(e)}")

def get_city(city_id):
    try:
        cityUseCase = CityUseCase()
        city = cityUseCase.get_city_by_id(city_id)

        if city:
            return response(city, None, status="success", message="City retrieved successfully")
        else:
            return response([], None, status="error", message="City not found")
    except Exception as e:
        return response([], None, status="error", message=f"An error occurred: {str(e)}")

def create_city():
    try:
        data = request.get_json()
        cityUseCase = CityUseCase()
        new_city = cityUseCase.create_city(data['name'], data['country'])

        return response(new_city, None, status="success", message="City created successfully")
    except Exception as e:
        return response([], None, status="error", message=f"An error occurred: {str(e)}")

def update_city(city_id):
    try:
        data = request.get_json()
        cityUseCase = CityUseCase()
        city = cityUseCase.update_city(city_id, data['name'], data['country'])

        if city:
            return response(city, None, status="success", message="City updated successfully")
        else:
            return response([], None, status="error", message="City not found")
    except Exception as e:
        return response([], None, status="error", message=f"An error occurred: {str(e)}")

def delete_city(city_id):
    try:
        cityUseCase = CityUseCase()
        city = cityUseCase.delete_city(city_id)

        if city:
            return response([], None, status="success", message="City deleted successfully")
        else:
            return response([], None, status="error", message="City not found")
    except Exception as e:
        return response([], None, status="error", message=f"An error occurred: {str(e)}")