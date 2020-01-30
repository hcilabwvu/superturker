from django.db import models
import logging

logger = logging.getLogger("log")

class Worker(models.Model):
	hits_completed = models.IntegerField(default=0)
	groups_completed = models.IntegerField(default=0)
	earnings = models.FloatField(default=0)
	search_sec = models.IntegerField(default=0)
	is_expert = models.IntegerField(default=0)
	age = models.IntegerField(default=0)
	gender = models.IntegerField(default=0)
	country = models.CharField(max_length=200)
	created = models.DateTimeField(auto_now_add=True, blank=True)

	def get_first(worker_mturk_id):
		return Worker.objects.filter(workermturkid__worker_mturk_id=worker_mturk_id).first()
		
	def get_or_add(worker_mturk_id):
		worker, created = Worker.objects.get_or_create(
			workermturkid__worker_mturk_id = worker_mturk_id,
			defaults = {
				"hits_completed": 0,
				"groups_completed": 0,
				"earnings": 0.0,
				"search_sec": 0.0,
				"is_expert": -1,
				"age": -1,
				"gender": -1,
				"country": ""
			}
		)
		return worker, created

class WorkerMTurkID(models.Model):
	worker = models.ForeignKey(Worker, on_delete=models.CASCADE, null=True)
	worker_mturk_id = models.CharField(max_length=200)
	created = models.DateTimeField(auto_now_add=True, blank=True)

	def add(worker, worker_mturk_id):
		WorkerMTurkID(worker=worker, worker_mturk_id=worker_mturk_id).save()

class Extension(models.Model):
	worker = models.ForeignKey(Worker, on_delete=models.CASCADE, null=True)
	amt_tools = models.IntegerField(default=0)
	auto_refresh = models.IntegerField(default=0)
	crowdworkers = models.IntegerField(default=0)
	distill = models.IntegerField(default=0)
	mturk_suite = models.IntegerField(default=0)
	openturk = models.IntegerField(default=0)
	page_monitor = models.IntegerField(default=0)
	tampermonkey = models.IntegerField(default=0)
	task_archive = models.IntegerField(default=0)
	tools_for_amt = models.IntegerField(default=0)
	turkopticon = models.IntegerField(default=0)
	visualping = models.IntegerField(default=0)
	created = models.DateTimeField(auto_now_add=True, blank=True)

	def update(request_data):
		data_extension, created = Extension.objects.get_or_create(**request_data)
		return data_extension, created

class RequesterRatings(models.Model):
	requester_id = models.CharField(max_length=200, null=True)
	requester_name = models.CharField(max_length=200, null=True)
	to1_comm = models.FloatField(default=0, null=True)
	to1_pay = models.FloatField(default=0, null=True)
	to1_fair = models.FloatField(default=0, null=True)
	to1_fast = models.FloatField(default=0, null=True)
	to1_reviews = models.IntegerField(default=0, null=True)
	to1_tos = models.FloatField(default=0, null=True)
	to2_all_reward = models.CharField(max_length=200, null=True)
	to2_all_pending = models.CharField(max_length=200, null=True)
	to2_all_comm = models.CharField(max_length=200, null=True)
	to2_all_recommend = models.CharField(max_length=200, null=True)
	to2_all_rejected = models.CharField(max_length=200, null=True)
	to2_all_tos = models.CharField(max_length=200, null=True)
	to2_all_broken = models.CharField(max_length=200, null=True)
	to2_recent_reward = models.CharField(max_length=200, null=True)
	to2_recent_pending = models.CharField(max_length=200, null=True)
	to2_recent_comm = models.CharField(max_length=200, null=True)
	to2_recent_recommend = models.CharField(max_length=200, null=True)
	to2_recent_rejected = models.CharField(max_length=200, null=True)
	to2_recent_tos = models.CharField(max_length=200, null=True)
	to2_recent_broken = models.CharField(max_length=200, null=True)
	tv_reviews = models.IntegerField(null=True)
	tv_hourly = models.FloatField(max_length=200, null=True)
	tv_pay = models.FloatField(max_length=200, null=True)
	tv_comm = models.FloatField(max_length=200, null=True)
	tv_fast = models.FloatField(max_length=200, null=True)
	tv_rejections = models.IntegerField(null=True)
	tv_blocks = models.IntegerField(null=True)
	tv_tos = models.IntegerField(null=True)
	tv_thid = models.CharField(max_length=200, null=True)
	created = models.DateTimeField(auto_now_add=True, blank=True)

	def get_or_add(request_data):
		data_to_rating, created = RequesterRatings.objects.get_or_create(**request_data)
		return data_to_rating, created

class HIT(models.Model):
	hit_id = models.CharField(max_length=200)
	assignment_id = models.CharField(max_length=200)
	worker = models.ForeignKey(Worker, on_delete=models.CASCADE, null=True)
	group_id = models.CharField(max_length=200)
	requester_id = models.CharField(max_length=200, null=True)
	requester_name = models.CharField(max_length=200)
	current_page = models.CharField(max_length=20)
	title = models.TextField()
	description = models.TextField()
	duration_sec = models.IntegerField(default=0)
	reward = models.FloatField(default=0)
	reward_currency = models.CharField(max_length=20)
	hits_available = models.IntegerField(default=0)
	qualifications = models.TextField(null=True)
	user_agent = models.TextField()
	template = models.CharField(max_length=100)
	rejected = models.IntegerField(default=0)
	created = models.DateTimeField(auto_now_add=True, blank=True)
	creation_time = models.TextField(default="")
	expiration_time = models.TextField(default="")

	def get_by_id(id):
		return HIT.objects.filter(id=id).first()

	def add(request_data):
		data_hit = HIT(**request_data)
		data_hit.save()
		return data_hit

class HITElements(models.Model):
	hit = models.ForeignKey(HIT, on_delete=models.CASCADE, null=True)
	num_link_total = models.IntegerField(default=0)
	num_link_survey = models.IntegerField(default=0)
	num_link_invalid = models.IntegerField(default=0)
	#num_link_video = models.IntegerField(default=0)
	ext_link_list = models.TextField(default="")
	num_video= models.IntegerField(default=0)
	num_audio= models.IntegerField(default=0)
	num_canvas = models.IntegerField(default=0)
	num_image = models.IntegerField(default=0)
	num_image_no_alt = models.IntegerField(default=0)
	num_canvas = models.IntegerField(default=0)
	duration_video = models.IntegerField(default=0)
	duration_audio = models.IntegerField(default=0)
	html = models.TextField(default="")
	created = models.DateTimeField(auto_now_add=True, blank=True)

	def add(request_data):
		data_hit_elements = HITElements(**request_data)
		data_hit_elements.save()
		return data_hit_elements

class HITKeywords(models.Model):
	hit = models.ForeignKey(HIT, on_delete=models.CASCADE, null=True)
	search = models.IntegerField(default=0)
	transcribe = models.IntegerField(default=0)
	click_and_drag = models.IntegerField(default=0)
	draw = models.IntegerField(default=0)
	copy = models.IntegerField(default=0)
	label = models.IntegerField(default=0)
	watch = models.IntegerField(default=0)
	listen = models.IntegerField(default=0)
	play = models.IntegerField(default=0)
	audio = models.IntegerField(default=0)
	video = models.IntegerField(default=0)
	record = models.IntegerField(default=0)
	classify = models.IntegerField(default=0)
	tag = models.IntegerField(default=0)
	tagging = models.IntegerField(default=0)
	survey = models.IntegerField(default=0)
	find = models.IntegerField(default=0)
	qualify = models.IntegerField(default=0)
	qualifier = models.IntegerField(default=0)
	transcription = models.IntegerField(default=0)
	image = models.IntegerField(default=0)
	sentiment = models.IntegerField(default=0)
	created = models.DateTimeField(auto_now_add=True, blank=True)

	def add(request_data):
		data_hit_keywords = HITKeywords(**request_data)
		data_hit_keywords.save()
		return data_hit_keywords
	
	def update(request_data):
		data_hit_keywords = HITKeywords.objects.filter(hit=request_data["hit"]).first()
		data_hit_keywords.search += request_data["search"]
		data_hit_keywords.transcribe += request_data["transcribe"]
		data_hit_keywords.click_and_drag += request_data["click_and_drag"]
		data_hit_keywords.draw += request_data["draw"]
		data_hit_keywords.copy += request_data["copy"]
		data_hit_keywords.label += request_data["label"]
		data_hit_keywords.watch += request_data["watch"]
		data_hit_keywords.listen += request_data["listen"]
		data_hit_keywords.play += request_data["play"]
		data_hit_keywords.audio += request_data["audio"]
		data_hit_keywords.video += request_data["video"]
		data_hit_keywords.record += request_data["record"]
		data_hit_keywords.classify += request_data["classify"]
		data_hit_keywords.tag += request_data["tag"]
		data_hit_keywords.tagging += request_data["tagging"]
		data_hit_keywords.survey += request_data["survey"]
		data_hit_keywords.find += request_data["find"]
		data_hit_keywords.qualify += request_data["qualify"]
		data_hit_keywords.qualifier += request_data["qualifier"]
		data_hit_keywords.transcription += request_data["transcription"]
		data_hit_keywords.image += request_data["image"]
		data_hit_keywords.sentiment += request_data["sentiment"]
		data_hit_keywords.save()
		return data_hit_keywords
	
class Interaction(models.Model):
	hit = models.ForeignKey(HIT, on_delete=models.CASCADE, null=True)
	num_click = models.IntegerField(default=0)
	num_keypress = models.IntegerField(default=0)
	len_scroll = models.IntegerField(default=0)
	len_mousemove = models.IntegerField(default=0)
	time_working = models.FloatField(default=0)
	time_previewing = models.FloatField(default=0)
	time_searching = models.FloatField(default=0)
	next_action = models.CharField(max_length=20, null=True)
	created = models.DateTimeField(auto_now_add=True, blank=True)

	def add(request_data):
		data_interaction = Interaction(**request_data)
		data_interaction.save()
		return data_interaction

class PostHITSurveyAnswer(models.Model):
	hit = models.ForeignKey(HIT, on_delete=models.CASCADE, null=True)
	worker = models.ForeignKey(Worker, on_delete=models.CASCADE, null=True)
	group_id = models.CharField(max_length=200)
	answers = models.TextField()
	created = models.DateTimeField(auto_now_add=True, blank=True)

	def get_last(worker_id,group_id):
		last_answer = PostHITSurveyAnswer.objects.filter(worker_id=worker_id,group_id=group_id).order_by("-created")
		if last_answer:
			return last_answer[0]
		else:
			return None

	def add(request_data):
		last_answer = PostHITSurveyAnswer.get_last(request_data["worker_id"],request_data["group_id"])
		if not last_answer or last_answer.answers!=request_data["answers"]:
			answer = PostHITSurveyAnswer(**request_data)
			answer.save()
		else:
			answer = None
		return answer

class InputFieldsCount(models.Model):
	hit = models.ForeignKey(HIT, on_delete=models.CASCADE, null=True)
	type = models.TextField()
	name = models.TextField()
	value = models.TextField()

	def add(request_data):
		data_input = InputFieldsCount(**request_data)
		data_input.save()
		return data_input
	
	def __str__(self):
		return "scrap={}, input_type={}, count={}".format(self.scrap,self.input_type,self.count)
