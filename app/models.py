from app import db
import datetime

class User(db.Model):
	__tablename__ = 'user'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64), index=True, unique=True)
	email = db.Column(db.String(120), index=True, unique=True)
	password = db.Column(db.String(32))
	posts = db.relationship('Item', backref='user')
	sent_messages = db.relationship('Messages', backref="user_from", foreign_keys='[Messages.from_id]')
	from_messages = db.relationship('Messages', backref="user_to", foreign_keys='[Messages.to_id]')

	@property
	def is_authenticated(self):
		return True

	@property
	def is_active(self):
		return True

	@property
	def is_anonymous(self):
		return False

	def get_id(self):
		try:
			return unicode(self.id)  # python 2
		except NameError:
			return str(self.id)  # python 3

	def __repr__(self):
		return '<User %s Id %s>' % (self.name, str(self.id))


class Item(db.Model):
	__tablename__ = 'item'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64), index=True)
	info = db.Column(db.String(200))
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	requests = db.relationship('Requests', backref='item')
	messages = db.relationship('Messages', backref='item')

	def __repr__(self):
		return '<Item %s>' % (self.name)


class Requests(db.Model):
	__tablename__ = 'requests'
	id = db.Column(db.Integer, primary_key=True)
	requester_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	item_id = db.Column(db.Integer, db.ForeignKey('item.id'))
	request_info = db.Column(db.String(200))
	status = db.Column(db.String(10), default="Pending")



class Messages(db.Model):
	__tablename__ = 'messages'
	id = db.Column(db.Integer, primary_key=True)
	message = db.Column(db.String(100))
	from_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	to_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	item_id = db.Column(db.Integer, db.ForeignKey('item.id'))
	created_on = db.Column(db.DateTime,  default=datetime.datetime.utcnow)