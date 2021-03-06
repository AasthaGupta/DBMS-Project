from . import database
from datetime import datetime
from hashlib import md5
import random


def login(form):
	status = { 'success' : True }
	userdata=None
	try:
		email = form['email']
		password = md5(form['password']).hexdigest()
		row = database.get_user(email, password)
		email, username, password, fname, lname, country, dob = row

		o_id = database.get_oid(username)

		row2 = database.get_user_organisation(o_id)
		o_id, oname, otype, ocity, ocountry = row2

		columns = ('email', 'username', 'password', 'fname', 'lname', 'country', 'dob', 'o_id','oname','otype','ocity','ocountry')
		userdata={}
		for k in columns:
			userdata[k]=eval(k)
	except Exception as e:
		status['error'] = str(e)
		status['success'] = False
	return status,userdata


def getQuestions(username):
        subData = database.getQuestions(username)
	return subData

def getSubmissions(username):
        subData = database.getSubmissions(username)
        return subData


def deleteAccount(username,oid):
	status = { 'success' : True }
	try:
		database.deleteUser(username,oid)
	except Exception as e:
		status['error'] = str(e)
		status['success'] = False
	return status



def submission(form,username):
	status = { 'success' : True }
	try:
		qdetails = form['qdetails']
		q_name,q_code = qdetails.split('$')
		q_code=int(q_code)
		language = form['language']
		s_date = datetime.now().date().strftime('%Y-%m-%d')
		s_time = datetime.now().time().strftime('%H:%M:%S')
		codeStatus = form['status']
		database.addSubmission(q_code,q_name,language,s_time,s_date,codeStatus,username)

	except Exception as e:
		status['error'] = str(e)
		status['success'] = False
	return status

def question(form,username):
	status = { 'success' : True }
	try:
		q_name = form['q_name']
		difficulty = form['difficulty']
		link = form['link']

		if database.link_exists(link,username):
			raise ValueError('Question already added')

		database.addQuestion(q_name,difficulty,link,username)

	except Exception as e:
		status['error'] = str(e)
		status['success'] = False
	return status

def register(form):
	status = {'success' : True}
	try:
		fname=form['fname']
		lname=form['lname']
		email=form['email']
		username=form['username']
		password=form['password']
		password2=form['password2']
		country=form['country']
		dob=form['dob']
		oname=form['oname']
		otype=form['otype']
		ocity=form['ocity']
		ocountry=form['ocountry']
		print"taken form data",form

		if database.username_exists(username):
			raise ValueError('Username already taken')

		if database.email_exists(email):
			raise ValueError('Email already registered')

		if password != password2:
			raise ValueError('Password does not match')

		password = md5(password).hexdigest()
		database.add(fname,lname,email,username,password,country,dob,oname,otype,ocity,ocountry)

	except Exception as e:
		status['error'] = str(e)
		status['success'] = False

	return status


def updateAccount(form):
	status = {'success' : True}
	userdata = None
	try:
		fname=form['fname']
		lname=form['lname']
		email=form['email']
		username=form['username']
		country=form['country']
		dob=form['dob']
		oname=form['oname']
		otype=form['otype']
		ocity=form['ocity']
		ocountry=form['ocountry']
		o_id = database.get_oid(username)
		database.updateUser(fname,lname,email,username,country,dob,o_id,oname,otype,ocity,ocountry)

		# to update session
		row = database.get_user_by_email(email)
		email, username, password, fname, lname, country, dob = row

		row2 = database.get_user_organisation(o_id)
		o_id, oname, otype, ocity, ocountry = row2

		columns = ('email', 'username', 'password', 'fname', 'lname', 'country', 'dob', 'o_id','oname','otype','ocity','ocountry')
		userdata={}
		for k in columns:
			userdata[k]=eval(k)
	except Exception as e:
		status['error'] = str(e)
		status['success'] = False

	return status, userdata

def userInfo(email):
	userdata = database.get_user_by_email(email)
	return userdata


def forgotPassword(email):
	status = {'success' : True}
	return status
