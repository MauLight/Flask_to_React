from flask import Blueprint, jsonify, request
from models import User, Trips, Activities


bpUser = Blueprint('bpUser', __name__)

#GET ENDPOINTS

#GET ALL USERS
@bpUser.route('/users', methods=['GET'])  # type: ignore
def all_users():
    users= User.query.all()
    users= list(map(lambda user: user.serialize(), users))
    return jsonify(users), 200

#GET USER BY ID
@bpUser.route('/users/<int:id>', methods= ['GET'])  # type: ignore
def user_by_id(id):
    user= User.query.get(id)
    return jsonify(user.serialize()), 200

#GET ALL USERS AND THEIR TRIPS
@bpUser.route('/users/mytrips', methods=['GET'])  # type: ignore
def all_users_with_trips():
    users= User.query.all()
    users= list(map(lambda user: user.serialize_with_trips(), users))
    return jsonify(users), 200

#GET USER AND TRIPS BY USER ID
@bpUser.route('/users/<int:id>/mytrips', methods=['GET'])  # type: ignore
def user_with_trips_with_id(id):
    user= User.query.get(id)
    return jsonify(user.serialize_with_trips()), 200

#GET ALL USERS WITH TRIPS AND ACTIVITIES
@bpUser.route('/users/mytrips/activities', methods=['GET'])  # type: ignore
def all_users_with_trips_with_activities():
    users= User.query.all()
    users= list(map(lambda user: user.serialize_with_trips_with_activities(), users))
    return jsonify(users), 200

#GET USER WITH TRIPS AND ACTIVITIES BY USER ID
@bpUser.route('/users/<int:id>/mytrips/activities', methods=['GET'])  # type: ignore
def user_with_trips_with_activities_with_id(id):
    user= User.query.get(id)
    return jsonify(user.serialize_with_trips_with_activities()), 200

#GET TRIP AND ACTIVITIES BY USER ID AND TRIP ID
@bpUser.route('/users/<int:id>/mytrips/<int:mytrips_id>/activities', methods=['GET'])
def get_trips_with_activities_by_user_id_and_trip_id(id, mytrips_id):
    mytrips = Trips.query.filter_by(users_id=id, id=mytrips_id).first()
    return jsonify(mytrips.serialize_with_activities()), 200

#POST ENDPOINTS

#POST NEW USER
@bpUser.route('/users', methods=['POST'])  # type: ignore
def store_user():
    firstname = request.json.get('firstname') # type: ignore
    lastname = request.json.get('lastname') # type: ignore
    birthdate = request.json.get('birthdate') # type: ignore
    email = request.json.get('email') # type: ignore
    password = request.json.get('password') # type: ignore
    verified = request.json.get('verified') # type: ignore

    user = User()
    user.firstname = firstname
    user.lastname = lastname
    user.birthdate = birthdate
    user.email = email
    user.password = password
    user.verified = verified
    user.save()
    return jsonify(user.serialize()), 201

#POST NEW TRIP BY USER ID
@bpUser.route('/users/<int:id>/mytrips', methods=['POST'])
def store_mytrip_by_user_id(id):
    user = User.query.get(id)

    travelling = request.json.get('travelling') # type: ignore
    with_children = request.json.get('with_children') # type: ignore
    gender_specific = request.json.get('gender_specific') # type: ignore
    stay = request.json.get('stay') # type: ignore
    budget = request.json.get('budget') # type: ignore
    partner_age = request.json.get('partner_age') # type: ignore
    users_id = request.json.get('users_id') # type: ignore

    mytrips = Trips()
    mytrips.travelling = travelling
    mytrips.with_children = with_children
    mytrips.gender_specific = gender_specific
    mytrips.stay = stay
    mytrips.budget = budget
    mytrips.partner_age = partner_age
    mytrips.users_id = users_id
    user.mytrips.append(mytrips)
    user.update()

    return jsonify(user.serialize_with_trips()), 200

#POST NEW ACTIVITY BY USER ID AND TRIP ID
@bpUser.route('/users/<int:id>/mytrips/<int:mytrips_id>/activities', methods=['POST'])  # type: ignore
def store_activities_by_trip_by_user_id(id, mytrips_id):
    mytrips = Trips.query.filter_by(users_id=id, id=mytrips_id).first()

    trekking = request.json.get('trekking') # type: ignore
    gastronomy = request.json.get('gastronomy') # type: ignore
    cultural = request.json.get('cultural') # type: ignore
    nightlife = request.json.get('nightlife') # type: ignore
    shopping = request.json.get('shopping') # type: ignore
    trips_id = request.json.get('trips_id') # type: ignore

    activities = Activities()
    activities.trekking = trekking
    activities.gastronomy = gastronomy
    activities.cultural = cultural
    activities.nightlife = nightlife
    activities.shopping = shopping
    activities.trips_id = trips_id
    mytrips.activities.append(activities)
    mytrips.update()

    return jsonify(mytrips.serialize_with_activities()), 200

#PUT ENDPOINTS

#UPDATE USER BY ID
@bpUser.route('/users/<int:id>/update', methods = ['PUT'])
def update_user(id):
    
    firstname = request.json.get('firstname') # type: ignore
    lastname = request.json.get('lastname') # type: ignore
    birthdate = request.json.get('birthdate') # type: ignore
    email = request.json.get('email') # type: ignore
    password = request.json.get('password') # type: ignore
    verified = request.json.get('verified')  # type: ignore

    user = User.query.get(id)
    user.firstname = firstname
    user.lastname = lastname
    user.birthdate = birthdate
    user.email = email
    user.password = password
    user.verified = verified

    user.save()
    return jsonify(user.serialize()), 200

#UPDATE TRIPS BY USER ID AND TRIP ID
@bpUser.route('/users/<int:id>/mytrips/<int:mytrips_id>/update', methods=['PUT'])
def update_mytrip_by_user_id_and_trip_id(id, mytrips_id):
    mytrips = Trips.query.filter_by(users_id=id, id=mytrips_id).first()

    travelling = request.json.get('travelling') # type: ignore
    with_children = request.json.get('with_children') # type: ignore
    gender_specific = request.json.get('gender_specific') # type: ignore
    stay = request.json.get('stay') # type: ignore
    budget = request.json.get('budget') # type: ignore
    partner_age = request.json.get('partner_age') # type: ignore
    users_id = request.json.get('users_id') # type: ignore

    mytrips = Trips.query.get(mytrips_id)
    mytrips.travelling = travelling
    mytrips.with_children = with_children
    mytrips.gender_specific = gender_specific
    mytrips.stay = stay
    mytrips.budget = budget
    mytrips.partner_age = partner_age
    mytrips.users_id = users_id

    mytrips.save()
    return jsonify(mytrips.serialize_with_activities()), 200

#UPDATE ACTIVITY BY USER ID, TRIP ID AND ACTIVITY ID
@bpUser.route('/users/<int:id>/mytrips/<int:mytrips_id>/activities/<int:act_id>/update', methods=['PUT'])  # type: ignore
def update_activity_by_user_id_trip_id_and_activity_id(mytrips_id, act_id, id):
    activity = Activities.query.filter_by(trips_id= mytrips_id, id= act_id).first()

    trekking = request.json.get('trekking') # type: ignore
    gastronomy = request.json.get('gastronomy') # type: ignore
    cultural = request.json.get('cultural') # type: ignore
    nightlife = request.json.get('nightlife') # type: ignore
    shopping = request.json.get('shopping') # type: ignore
    trips_id = request.json.get('trips_id') # type: ignore

    activity = Activities.query.get(act_id)
    activity.trekking = trekking
    activity.gastronomy = gastronomy
    activity.cultural = cultural
    activity.nightlife = nightlife
    activity.shopping = shopping
    activity.trips_id = trips_id

    activity.save()
    return jsonify(activity.serialize()), 200
