from __future__ import unicode_literals
from django.db import models
import bcrypt
from datetime import datetime

class UserManager(models.Manager):
	def registrationValidate(self, postData):
		response = {
			'status': True,
		}
		errors = []

		if len(postData['name']) < 3 or len(postData['username']) < 3:
			errors.append('Name and Username should be at least 3 characters!')
		if postData['password'] != postData['confirm']:
			errors.append('Passwords did not match!')
		if len(postData['password']) < 8:
			errors.append('Weak password, try 8 or more characters!')
		if len(errors) > 0:
			response['status'] = False
			response['errors'] = errors
		else: 
			PW = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())
			response['user'] = User.objects.create(name=postData['name'], username=postData['username'], password=PW)
		return response

	def loginValidate(self, postData):
		response = {
			'status': False,
		}
		errors = []
		users = User.objects.filter(username=postData['logusername'])
		if len(users) < 1:
			errors.append('Incorrect Email/Password, Try again')
			response['errors'] = errors
			return response
		PW = bcrypt.checkpw(postData['logpassword'].encode(), users[0].password.encode())
		if PW == True:
			response['status'] = True
			response['user'] = users[0]
		else: 
			errors.append('Incorrect Email/Password, Try again')
			response['errors'] = errors
		return response

class PlanManager(models.Manager):
	def newplanValidate(self, postData):
		response = {
			'status': True,
		}
		errors = []
		if len(postData['destination']) < 1 or len(postData['desc']) < 1 or len(postData['datefrom']) < 1 or len(postData['dateto']) < 1:
			errors.append('Please fill all required fields!')
			response['status'] = False
			response['errors'] = errors
			return response
		now = datetime.now().date()
		datefrom = datetime.strptime(postData['datefrom'], '%Y-%m-%d').date()
		dateto = datetime.strptime(postData['dateto'], '%Y-%m-%d').date()
		if datefrom < now:
			errors.append('This is not a Back to the Future remake!')
		if datefrom > dateto:
			errors.append('Calendars cant moon-walk, choose a future date!')
		if len(errors) > 0:
			response['status'] = False
			response['errors'] = errors
		return response



class User(models.Model):
	name = models.CharField(max_length=255)
	username = models.CharField(max_length=255)
	password = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now_add=True)

	objects = UserManager()

	def __str__(self):
		return self.name

class Travel(models.Model):
	destination = models.CharField(max_length=255)
	desc =  models.CharField(max_length=255)
	datefrom = models.DateTimeField()
	dateto = models.DateTimeField()
	created_by = models.ForeignKey(User, related_name='travel_plans')
	joined_by = models.ManyToManyField(User, related_name='joined_plans')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	objects = PlanManager()

	def __str__(self):
		return self.destination