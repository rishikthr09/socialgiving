from flask import render_template, redirect, flash, redirect, g, session, url_for, request
from app import app, lm, models
from .forms import LoginForm, RegisterForm, PostItemForm, RequestItemForm, MessageForm
from flask.ext.login import login_user, logout_user, current_user, login_required
import logging
from logging.handlers import RotatingFileHandler
from models import User, Item, Requests, Messages
from app import db
from sqlalchemy.sql import and_, or_


@app.route('/')
def default():
	return "hi"



@app.route('/index')
def index():
	if not current_user.is_authenticated:
		return redirect(url_for('login'))
	return render_template("index.html",
							title="Welcome",
							user=current_user)

'''
@app.route('/login', methods=['GET', 'POST'])
def login():
	if g.user is not None:
		return redirect(url_for('index'))
	form = LoginForm()
	if form.validate_on_submit():
		flash('Login requested for Username="%s", remember_me=%s' %
			(form.username.data, str(form.remember_me.data)))
		return redirect('/index')
	return render_template('login.html', 
							title='Sign In',
							form=form)
'''


@app.route('/login', methods=['GET', 'POST'])
def login():
	if(g.user is not None and g.user.is_authenticated):
		return redirect(url_for('index'))

	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter(User.email == form.email.data).first()
		if(user):
			if(user.password == form.password.data):
				login_user(user)
				flash('Logged In')
				return redirect(url_for('index'))
			else:
				flash("Invalid Password")
				return redirect(url_for('login'))


	return render_template('login.html', 
							title='Sign In',
							form=form,
							user=current_user)



@app.route('/register' , methods=['GET','POST'])
def register():
	form = RegisterForm()
	if(form.validate_on_submit()):
		try:
			user = User(name = form.name.data , email=form.email.data, password=form.password.data)
			db.session.add(user)
			db.session.commit()
			flash('User successfully registered')
			return redirect(url_for('login'))
		except:
			flash('User Already Exists')
			return redirect(url_for('login'))

	return render_template('register.html',
							title="Register",
							form=form,
							user=current_user)


@app.route('/postitem', methods=['GET','POST'])
@login_required
def postitem():
	form = PostItemForm()
	if(form.validate_on_submit()):
		try:
			item = Item(name = form.name.data, info = form.info.data, user_id = current_user.id)
			db.session.add(item)
			db.session.commit()
			flash('Item Posted')
			return redirect(url_for('index'))
		except:
			flash('Unable to post. Please try again')
			return redirect(url_for('postitem'))
	return render_template('postitem.html',
							title="Post Item",
							form = form,
							user = current_user)


@app.route("/viewitem/<int:item_id>", methods=['GET','POST'])
@login_required
def viewitem(item_id):
	item = Item.query.filter(Item.id == item_id).first()
	if(item.user_id == current_user.id):
		user_messages = {}
		id_to_user = {}
		for msg in item.messages:
			id_to_user[msg.from_id] = User.query.filter(User.id == msg.from_id).first().name
			if msg.from_id != current_user.id:
				try:
					user_messages[msg.from_id].append(msg)
				except:
					user_messages[msg.from_id] = []
					user_messages[msg.from_id].append(msg)
			else:
				try:
					user_messages[msg.to_id].append(msg)
				except:
					user_messages[msg.to_id] = []
					user_messages[msg.to_id].append(msg)
		return render_template('viewownpost.html',
								item = item,
								id_to_user=id_to_user,
								user_messages=user_messages,
								user=current_user)
	
	else:
		form = MessageForm()
		poster = User.query.filter(User.id == item.user_id).first()
		messages = Messages.query.filter(and_(or_(Messages.from_id == current_user.id,Messages.to_id == current_user.id), Messages.item_id == item_id)).all()
		for i in messages:
			print i.message
		if(form.validate_on_submit()):
			new_message = Messages(message=form.message.data, from_id=current_user.id,to_id=item.user_id,item_id=item.id)
			db.session.add(new_message)
			db.session.commit()
			flash("Message Sent")
			return redirect(url_for("viewitem", item_id=item_id))
		return render_template('viewotherpost.html',
								item=item,
								form=form,
								messages=messages,
								poster=poster,
								user=current_user)


@app.route('/viewusermessages/', methods=['GET','POST'])
@login_required
def viewusermessages():
	form = MessageForm()
	item_id = int(request.args.get('p'))
	requester_id = int(request.args.get('u'))
	item = Item.query.filter(Item.id == item_id).first()
	requester = User.query.filter(User.id == requester_id).first()
	items_list = (i.id for i in current_user.posts)
	if(item_id not in items_list):
		flash('Invalid Request')
		return redirect(url_for('index'))
	requester_list = (i.from_id for i in item.messages)
	print requester_id
	if(requester_id not in requester_list):
		flash('Invalid Request')
		return redirect(url_for('index'))
	message_list = Messages.query.filter(and_(or_(Messages.to_id == requester_id, Messages.from_id == requester_id),Messages.item_id == item_id)).all()
	for i in message_list:
		print i.message
	if(form.validate_on_submit()):
			new_message = Messages(message=form.message.data, from_id=current_user.id,to_id=requester.id,item_id=item.id)
			db.session.add(new_message)
			db.session.commit()
			flash("Message Sent")
			return redirect(url_for("viewusermessages",p=item_id,u=requester_id))
	return render_template('viewusermessages.html',
						requester=requester,
						item=item,
						message_list=message_list,
						form=form,
						user=current_user)




@app.route("/viewallitems")
@login_required
def viewallitems():
	all_items = Item.query.filter(Item.user_id != current_user.id).all()
	return render_template('viewallitems.html',
							items = all_items,
							user=current_user)


@app.route("/getlocation")
def getlocation():
	return render_template('getlocation.html',
							user=current_user)

'''
@app.route("/postrequest/<int:item_id>", methods=['GET','POST'])
@login_required
def postrequest(item_id):
	item = Item.query.filter(Item.id == item_id).first()
	form = RequestItemForm()
	if(form.validate_on_submit()):
		try:
			request = Requests(requester_id = current_user.id, item_id = item_id, request_info = form.info.data, status = "Pending")
			db.session.add(request)
			db.session.commit()
			flash("Request Posted")
			return redirect(url_for('index'))
		except:
			flash("Failed to post. Please try again.")
			return redirect(url_for('index'))
	return render_template('postrequest.html',
							title="Post Request",
							form=form,
							item=item,
							user=current_user)


@app.route("/acceptrequest/<int:req_id>")
@login_required
def acceptrequest(req_id):
	request_current = Requests.query.filter(Requests.id == req_id).first()
	item = Item.query.filter(Item.id == request_current.item_id).first()
	if(item.user_id == current_user.id):
		request_current.status = "Done"
		db.session.commit()
		return redirect(url_for('viewitem/'+item.id))
	flash("Invalid Request")
	return redirect(url_for('viewitem'+item.id))
'''




'''
@app.route('/viewownpost')
@login_required
def viewownpost():
	return render_template()
'''





'''
@app.route('/viewotherpost')
@login_required
def viewotherpost():
'''









@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('login'))
	

@lm.user_loader
def load_user(id):
	return User.query.get(int(id))


@app.before_request
def before_request():
	g.user = current_user