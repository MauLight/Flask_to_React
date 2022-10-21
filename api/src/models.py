from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):  # type: ignore
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key= True)
    firstname = db.Column(db.String(50), nullable= False)
    lastname = db.Column(db.String(50), nullable= False)
    birthdate = db.Column(db.String(50))
    email = db.Column(db.String(50), nullable= False, unique = True)
    password = db.Column(db.String(50), nullable= False)
    verified = db.Column(db.Boolean(), default = True)
    mytrips = db.relationship('Trips', cascade = 'all, delete', backref= 'user')

    def serialize(self):
        return {
            'id': self.id,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'birthdate': self.birthdate,
            'email': self.email,
            'password' : self.password,
            'verified': self.verified
        }

    def serialize_with_trips(self):
        return {
            'id': self.id,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'birthdate': self.birthdate,
            'email': self.email,
            'password' : self.password,
            'verified': self.verified,
            'mytrips' : [trip.serialize() for trip in self.mytrips]
        }
    
    def serialize_with_trips_with_activities(self):
        return {
            'id': self.id,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'birthdate': self.birthdate,
            'email': self.email,
            'password' : self.password,
            'verified': self.verified,
            'mytrips' : [trip.serialize_with_activities() for trip in self.mytrips]
        }


    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class Trips(db.Model):  # type: ignore
    __tablename__ = 'mytrips'
    id = db.Column(db.Integer, primary_key= True)
    travelling = db.Column(db.Integer, nullable= False)
    with_children = db.Column(db.Boolean(), nullable= False)
    gender_specific = db.Column(db.Integer, nullable= False)
    stay = db.Column(db.Integer, nullable= False)
    budget = db.Column(db.Integer, nullable= False)
    partner_age = db.Column(db.Integer, nullable= False)
    activities = db.relationship('Activities', cascade = 'all, delete', backref= 'trip')
    users_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete= 'CASCADE'), nullable= False)

    def serialize(self):
        return {
            'id': self.id,
            'travelling': self.travelling,
            'with_children': self.with_children,
            'gender_specific': self.gender_specific,
            'stay': self.stay,
            'budget' : self.budget,
            'partner_age': self.partner_age,
            'users_id': self.users_id
        }

    def serialize_with_activities(self):
        return {
            'id': self.id,
            'travelling': self.travelling,
            'with_children': self.with_children,
            'gender_specific': self.gender_specific,
            'stay': self.stay,
            'budget' : self.budget,
            'partner_age': self.partner_age,
            'activities' : [activity.serialize() for activity in self.activities],
            'users_id': self.users_id
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class Activities(db.Model):  # type: ignore
    __tablename__ = 'activities'
    id = db.Column(db.Integer, primary_key= True)
    trekking = db.Column(db.Boolean(), default= False)
    gastronomy = db.Column(db.Boolean(), default= False)
    cultural = db.Column(db.Boolean(), default= False)
    nightlife = db.Column(db.Boolean(), default= False)
    shopping = db.Column(db.Boolean(), default= False)
    trips_id = db.Column(db.Integer, db.ForeignKey('mytrips.id', ondelete= 'CASCADE'), nullable= False)

    def serialize(self):
        return {
            'id': self.id,
            'trekking': self.trekking,
            'gastronomy': self.gastronomy,
            'cultural': self.cultural,
            'nightlife': self.nightlife,
            'shopping' : self.shopping,
            'trips_id': self.trips_id,
        }
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
