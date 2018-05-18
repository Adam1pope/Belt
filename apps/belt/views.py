# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from models import *
import bcrypt
from django.contrib import messages
from django.utils.crypto import get_random_string
from datetime import datetime  
from datetime import timedelta   #datetime.now()
from time import gmtime, strftime

def index(request):
	return render(request, 'belt/index.html')

def register(request):
	errors = User.objects.basic_validator(request.POST)
	if len(errors) > 0:
		for tag, error in errors.items():
			messages.error(request, error)
			print errors
		return redirect("/")
	else:
		pw = request.POST["password"]
		hash1 = bcrypt.hashpw(pw.encode(), bcrypt.gensalt())
		u = User.objects.create(name=request.POST["name"] ,email=request.POST["email"], password=hash1,)
		#above created a user, and stored it in a variable called u
		request.session["user_id"] = u.id #stored the user id in session
	return redirect('/appointments')

def appointments(request):
	user = User.objects.get(id = request.session['user_id'])
	# apt_id = appointments.objects.get(id = request.session['user_apt_id'])
	user_apts = user.apts.all()
	request.session['time'] = strftime("%m-%d-%Y", gmtime())

	context = {
			"user_apts": user_apts,
			"user": user, 
		}
	return render(request, 'belt/appointments.html', context,)


def login(request):
	errors = User.objects.login_validator(request.POST)
	if len(errors) > 0:
		for tag, error in errors.items():
			messages.error(request, error)
			print errors
		return redirect("/")
	else:
		user = User.objects.get(email = request.POST['email'])
		request.session["user_id"] = user.id #stored the user id in session
	
	return redirect('/appointments')


def process(request):
	apt_id = User.objects.get(id = request.session['user_id'])
	apt = appointment.objects.create(date = request.POST['date'], time = request.POST['time'], tasks = request.POST['tasks'], status = request.POST['status'], user_apt = apt_id)
	
	return redirect('/appointments')


# def redirect(request, id):
# 	apt_id = appointment.objects.get(id = id)

# 	print '##################################################################'
	
# 	return redirect('/appointments/{}'.format(apt_id))


def edit(request):
	user = User.objects.get(id = request.session['user_id'])
	# apt_id = appointments.objects.get(id = request.session['user_apt_id'])
	user_apts = user.apts.all()

	context = {
		"user_apts": user_apts,
		"user": user, 
		}

	return render(request, 'belt/edit.html', context)

def delete(request):
	a = appointment.objects.first()
	a.delete()
	return redirect('/appointments')


def update(request):
	a = appointment.objects.first()
	a.delete()
	apt_id = User.objects.get(id = request.session['user_id'])
	apt = appointment.objects.create(date = request.POST['date'], time = request.POST['time'], tasks = request.POST['tasks'], status = request.POST['status'], user_apt = apt_id)

	return redirect('/appointments') 




