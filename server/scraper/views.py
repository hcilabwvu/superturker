from django.shortcuts import render

from django.http import HttpResponse
from .models import *
from django.views.decorators.csrf import csrf_exempt
from django import db
import json
import logging
import hashlib

#import grequests
#import requests
#import concurrent.futures
#import urllib.request

import threading
from multiprocessing import Pool

logger = logging.getLogger("log")

@csrf_exempt
def save_parent(request):
	request_data = json.loads(request.body)
	
	worker = Worker.get_first(request_data["worker_id"])
	request_data["HIT"]["worker"] = worker
	data_hit = HIT.add(request_data["HIT"])
	request_data["HITKeywords"]["hit"] = data_hit
	data_hit_keywords = HITKeywords.add(request_data["HITKeywords"])

	HIT.objects.filter(assignment_id__in=request_data["rejectedAssignmentIDs"]).update(rejected=1)
	
	response = HttpResponse(json.dumps({"parent_id": data_hit.id}))
	return response


@csrf_exempt
def update_worker_profile(request):
	request_data = json.loads(request.body)
	
	worker = Worker.get_first(request_data["worker_id"])
	request_data["Extension"]["worker"] = worker
	data_extension, created = Extension.update(request_data["Extension"])
	data_to_rating, created = RequesterRatings.get_or_add(request_data["RequesterRatings"])
	
	response = HttpResponse(json.dumps({}))
	return response


def get_url_base(url):
	url_lower = url.lower()  # to lower case
	if url_lower.startswith("http://"):
		url = url[7:]
	elif url_lower.startswith("https://"):
		url = url[8:]
	if url_lower.startswith("www."):
		url = url[4:]
	if url_lower.endswith("/"):
		url = url[:-1]
	return url


def count_invalid_links(request_data):
	def load_url(url, timeout):
		with urllib.request.urlopen(url, timeout=timeout) as conn:
			return conn.read()

	prefixes = ["http://", "https://", "http://www.", "https://www."]
	invalid_link_cnt = 0
	links = []
	[links.append(get_url_base(link)) for link in request_data["ext_links"] if get_url_base(link) not in links]

	response_list = []
	print(links)
	#all_links = []
	#for link in links:
	#	for pf in prefixes:
	#		all_links.append(pf+link)
	#		headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
	#		res = grequests.get(pf+link, timeout=3, headers=headers)
	#		response_list.append(res)
	#grequests.map(response_list)
	#with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
	#	future_to_url = {executor.submit(load_url, url, 60): url for url in all_links}
	#	for future in concurrent.futures.as_completed(future_to_url):
	#		url = future_to_url[future]
	#		try:
	#			data = future.result()
	#		except Exception as exc:
	#			print('%r generated an exception: %s' % (url, exc))
	#		else:
	#			response_list.append(data)

	#for i in range(0,len(response_list),4):
	#	valid_list = []
	#	for r in response_list[i:i+4]:
	#		if r.response and (r.response.status_code==200 or r.response.status_code==301):
	#			valid_list.append(True)
	#		else:
	#			valid_list.append(False)
	#	print(valid_list)
	#	is_valid = any(valid_list)
	#	if not is_valid:
	#		invalid_link_cnt += 1

	return invalid_link_cnt


def save_hit_elements(request_data):
	request_data["HITElements"]["num_link_invalid"] = count_invalid_links(request_data)

	print("# of invalid links: {}".format(request_data["HITElements"]["num_link_invalid"]))

	HITElements.add(request_data["HITElements"])


@csrf_exempt
def save_iframe(request):
	if request.method=="POST":
		request_data = json.loads(request.body)
		db.connections.close_all()

		worker = Worker.get_first(request_data["worker_id"])
		hit = HIT.get_by_id(request_data["parent_id"])
		hit.template = request_data["template"]
		hit.save()

		if bool(request_data["PostHITSurveyAnswer"])==True:
			if "ignore" not in request_data["PostHITSurveyAnswer"]:
				request_data["PostHITSurveyAnswer"]["hit_id"] = hit.id
				request_data["PostHITSurveyAnswer"]["worker_id"] = worker.id
				phs_answer = PostHITSurveyAnswer.add(request_data["PostHITSurveyAnswer"])
			has_phs_answer = True
		else:
			has_phs_answer = False

		request_data["HITElements"]["hit"] = hit
		t = threading.Thread(target=save_hit_elements,args=(request_data,))
		t.start()

		request_data["HITKeywords"]["hit"] = hit
		HITKeywords.update(request_data["HITKeywords"])

		for each in request_data["InputFieldsCount"]:
			each["hit"] = hit
			InputFieldsCount.add(each)

		request_data["Interaction"]["hit"] = hit
		Interaction.add(request_data["Interaction"])
		
		response = HttpResponse(json.dumps({"hit_id": hit.id, "worker_id": worker.id, "group_id": hit.group_id, "has_phs_answer": has_phs_answer }))
		
		return response


@csrf_exempt
def worker(request, worker_mturk_id):
	if request.method=="GET":
		worker, created = Worker.get_or_add(worker_mturk_id)
		if created:
			WorkerMTurkID.add(worker, worker_mturk_id)

		return HttpResponse(json.dumps({"worker_record_id": worker.id, "created": created}))


@csrf_exempt
def save_post_survey_result(request):
	if request.method=="POST":
		request_data = json.loads(request.body)
		logger.info(request_data)
		answer = PostHITSurveyAnswer.add(request_data)
		response = HttpResponse(json.dumps(request_data))
		return response


@csrf_exempt
def load_last_post_survey_result(request, worker_id, group_id):
	if request.method=="GET":
		try:
			worker = Worker.get_first(worker_id)
			last_result = PostHITSurveyAnswer.get_last(worker.id,group_id)
			if last_result:
				return HttpResponse(json.dumps(last_result.answers))
			else:
				return HttpResponse(json.dumps(None))
		except Exception as e:
			logger.info(e)
			return HttpResponse(json.dumps(None))

@csrf_exempt
def delete_all(request):
	if request.method=="POST":
		try:
			HITElements.objects.all().delete()
			HITKeywords.objects.all().delete()
			InputFieldsCount.objects.all().delete()
			Interaction.objects.all().delete()
			PostHITSurveyAnswer.objects.all().delete()
			RequesterRatings.objects.all().delete()
			WorkerMTurkID.objects.all().delete()
			Worker.objects.all().delete()
			HIT.objects.all().delete()
			return HttpResponse(json.dumps({"is_error": False}))
		except Exception as e:
			logger.info(e)
			return HttpResponse(json.dumps({"is_error": True}))
