from django.shortcuts import render
from .models import Post
from datetime import datetime
from apps.history.models import History
from django.http import HttpRequest
#from django.db.models import Count
from django.http import HttpResponseRedirect


def course(request):
	keyword = request.GET.get('keyword', '')
	if keyword == "":
		course_list = []
	else:
		course_list = Post.objects.filter(syllabus__contains=keyword)
	template_name = 'course/course.html'
	context = {'course_list':course_list, 'keyword':keyword}
	return render(request, template_name, context)

def course_detail(request, course_id):
	course = Post.objects.get(id=course_id)
	keyword = request.GET.get('keyword', '')
	time = datetime.now()
	
	#template_name = 'course/course_detail.html'
	#context = {'course':course}
	#return render(request, template_name, context)
	if not request.user.is_authenticated:
		History.objects.create(course=course,keyword=keyword,time=time)
	else:
		History.objects.create(user=request.user,course=course,keyword=keyword,time=time)
	
	course.click_times += 1
	course.save()
	
	#hot_keyword = History.objects.values('keyword').annotate(c=Count('keyword')).order_by('-c')
	
	return HttpResponseRedirect(course.class_url)
