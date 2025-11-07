from flask import Blueprint
from app.services import home_service , city_service

bp = Blueprint("routes", __name__)

bp.add_url_rule('/', 'home', home_service.index, methods=['GET'])


bp.add_url_rule('/cities', 'get_all_cities', city_service.get_all_cities, methods=['GET'])
bp.add_url_rule('/cities/<int:city_id>', 'get_city', city_service.get_city, methods=['GET'])
bp.add_url_rule('/cities', 'create_city', city_service.create_city, methods=['POST'])
bp.add_url_rule('/cities/<int:city_id>', 'update_city', city_service.update_city, methods=['PUT'])
bp.add_url_rule('/cities/<int:city_id>', 'delete_city', city_service.delete_city, methods=['DELETE'])