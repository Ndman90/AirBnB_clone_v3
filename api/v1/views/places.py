#!/usr/bin/python3
"""Places view module."""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.city import City
from models.user import User
from models.amenity import Amenity
from models.place_amenity import PlaceAmenity


@app_views.route(
        '/cities/<city_id>/places',
        methods=['GET'],
        strict_slashes=False
        )
def get_places_by_city(city_id):
    """Retrieves the list of all Place objects of a City."""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """Retrieves a Place object."""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route(
        '/places/<place_id>',
        methods=['DELETE'],
        strict_slashes=False
        )
def delete_place(place_id):
    """Deletes a Place object."""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route(
        '/cities/<city_id>/places',
        methods=['POST'],
        strict_slashes=False
        )
def create_place(city_id):
    """Creates a Place."""
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")

    user_id = data.get("user_id")
    if not user_id:
        abort(400, "Missing user_id")

    user = storage.get(User, user_id)
    if not user:
        abort(404)

    if "name" not in data:
        abort(400, "Missing name")

    data["city_id"] = city_id
    place = Place(**data)
    storage.new(place)
    storage.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """Updates a Place object."""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")

    ignore_keys = ["id", "user_id", "city_id", "created_at", "updated_at"]

    for key, value in data.items():
        if key not in ignore_keys:
            setattr(place, key, value)

    storage.save()
    return jsonify(place.to_dict()), 200

@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def places_search():
    """Searches for places based on JSON content in the request body."""
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")

    states_ids = data.get('states', [])
    cities_ids = data.get('cities', [])
    amenities_ids = data.get('amenities', [])

    places_list = []

    if not states_ids and not cities_ids:
        # If no states or cities specified, retrieve all places
        places_list = storage.all(Place).values()
    else:
        # Retrieve places based on states and cities
        for state_id in states_ids:
            state = storage.get(State, state_id)
            if state:
                places_list.extend(state.places)

        for city_id in cities_ids:
            city = storage.get(City, city_id)
            if city:
                places_list.extend(city.places)

    # Filter places based on amenities
    if amenities_ids:
        amenities = storage.all(Amenity)
        filtered_places = []
        for place in places_list:
            place_amenities = [pa.amenity_id for pa in place.amenities]
            if set(amenities_ids).issubset(place_amenities):
                filtered_places.append(place)
        places_list = filtered_places

    # Return the final list of places
    return jsonify([place.to_dict() for place in places_list])
