from django.conf.urls import url

from . import views

app_name = "scraper"
urlpatterns = [
	url(r'^parent/$', views.save_parent, name='save_parent'),
	url(r'^worker_profile/$', views.update_worker_profile, name='update_worker_profile'),
	url(r'^iframe/$', views.save_iframe, name='save_iframe'),
	url(r'^worker/(?P<worker_mturk_id>\w{1,50})/$', views.worker, name='worker'),
	url(r'^post_survey/$', views.save_post_survey_result, name='save_post_survey_result'),
	url(r'^post_survey/last/(?P<worker_id>\w{1,50})/(?P<group_id>\w{1,50})$', views.load_last_post_survey_result, name='load_last_post_survey_result'),
	url(r'^delete_all/$', views.delete_all, name='delete_all'),
]
