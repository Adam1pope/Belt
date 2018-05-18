# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from django.db import models

import bcrypt 
import re 

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z09._-]+\.[a-zA-Z]+$')
PASSWORD_REGEX = re.compile(r'^[a-zA-Z0-9]+$')
NAME_REGEX = re.compile(r'^[a-zA-Z]+$')



class UserManager(models.Manager):	 
	def basic_validator(self, postData):
		errors = {}
		#Name fields validated below
		if len(postData['name']) < 3:
			errors['name'] = "First name field needs to be longer than 3 characters"
		# if not NAME_REGEX.match(postData["name"]):
		# 	errors["name"] = "User name can only contain letters"
		# if len(postData['alias']) < 3:
		# 	errors['alias'] = "Last name field needs to be longer than 3 characters"
		# if not NAME_REGEX.match(postData["alias"]):
		# 	errors["alias"] = "User alias can only contain letters"
			# Email and password validated below
		if len(postData['password']) < 8:
			errors['password'] = "Password must be greater than 8 characters"
		if not PASSWORD_REGEX.match(postData["password"]):
			errors["password"] = "password must contain only letter and numbers"
		if  postData['password'] != postData['conf_password']:
			errors['conf_password']= "password does not match"
		if not EMAIL_REGEX.match(postData['email']):
			errors['email']= "Invalid email"
		if User.objects.filter(email = postData["email"]).exists():
			errors["email"] = "Email already exists"

		return errors

	def login_validator(self, postData):
		errors = {}
		if len(postData["email"]) < 3:
			errors["email"] = "Email should be more than 3 characters"
		if len(postData["password"]) < 8:
			errors["password"] = "Password must be longer than 8 characters"
		check = User.objects.filter(email=postData["email"])
		print check
		if len(check) == 0:
			errors["email"] = "Must enter an email address"
			return errors
		if not bcrypt.checkpw(postData["password"].encode(), check[0].password.encode()):
			errors["password"] = "Password doesn't match"
		
		return errors		


	def pw_validator(self, postData):
		errors = {}
		if len(postData["password"]) < 8:
			errors["password"] = "Password must be longer than 8 characters"
		if postData["password"] != postData["confirm_password"]:
			errors["confirm_password"] = "Password confirmation does not match"
		
		return errors


class User(models.Model):
	name = models.CharField(max_length = 255)
	email = models.CharField(max_length = 255)
	password = models.CharField(max_length = 255)
	dob = models.CharField(max_length = 255)
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	objects = UserManager()	


class appointment(models.Model):
	tasks = models.CharField(max_length = 255)
	status = models.CharField(max_length = 255)
	time = models.CharField(max_length = 255)
	date = models.CharField(max_length = 255)
	user_apt = models.ForeignKey(User, related_name = "apts")
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)		