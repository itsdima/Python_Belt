# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, HttpResponse
from .models import *
from django.contrib import messages

# Create your views here.

def index(request):
	return render(request, 'Beltexam_app/index.html')

def travels(request):
	if 'user_id' not in request.session:
		return redirect('/main')
	activeuser = User.objects.get(id=request.session['user_id'])
	welcome = activeuser.username
	destinations = Travel.objects.filter(created_by=activeuser)
	joinedTrips = Travel.objects.filter(joined_by=activeuser)
	others = Travel.objects.all().exclude(created_by=activeuser).exclude(joined_by=activeuser)
	context = {
	'plans': destinations,
	'active': welcome, 
	'others': others, 
	'joined': joinedTrips
	}
	return render(request, 'Beltexam_app/travels.html', context)

def destination(request, number):
	if 'user_id' not in request.session:
		return redirect('/main')
	location = Travel.objects.get(id=number)
	activeuser = User.objects.get(id=request.session['user_id'])
	toexclude = location.created_by.id
	other = User.objects.filter(joined_plans=location).exclude(id=toexclude)
	context = {
	'info': location,
	'joinedby': other
	}
	return render(request, 'Beltexam_app/destination.html', context)

def add(request):
	if 'user_id' not in request.session:
		return redirect('/main')
	return render(request, 'Beltexam_app/add.html')

def processuser(request):
	result = User.objects.registrationValidate(request.POST)
	print result
	if result['status']:
		request.session['user_id'] = result['user'].id
	else: 
		for error in result['errors']:
			messages.error(request, error)
		return redirect('/main')
	return redirect('/travels')

def login(request):
	result = User.objects.loginValidate(request.POST)
	if result['status'] == False:
		for error in result['errors']:
			messages.warning(request, error)
		return redirect('/main')
	request.session['user_id'] = result['user'].id
	return redirect('/travels')

def logout(request):
	request.session.clear()
	return redirect('/main')

def processadd(request):
	result = Travel.objects.newplanValidate(request.POST)
	if result['status'] == False:
		for error in result['errors']:
			messages.warning(request, error)
		return redirect('/travels/add')
	else:
		user = User.objects.get(id=request.session['user_id'])
		Travel.objects.create(destination=request.POST['destination'], desc=request.POST['desc'], datefrom=request.POST['datefrom'], dateto=request.POST['dateto'], created_by=user)
		return redirect('/travels')

def jointrip(request, number):
	active = User.objects.get(id=request.session['user_id'])
	trip = Travel.objects.get(id=number)
	trip.joined_by.add(active)
	return redirect('/travels')