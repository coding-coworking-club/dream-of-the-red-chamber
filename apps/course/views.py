from django.shortcuts import render
from .models import Post
from datetime import datetime
from apps.history.models import History
from django.http import HttpRequest
#from django.db.models import Count
from django.http import HttpResponseRedirect


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
	
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
	type = "click"
	ip = get_client_ip(request)
	
	#template_name = 'course/course_detail.html'
	#context = {'course':course}
	#return render(request, template_name, context)
	if not request.user.is_authenticated:
		History.objects.create(course=course,keyword=keyword,time=time,type=type,ip=ip)
	else:
		History.objects.create(user=request.user,course=course,keyword=keyword,time=time,type=type,ip=ip)
	
	course.click_times += 1
	course.save()
	
	#hot_keyword = History.objects.values('keyword').annotate(c=Count('keyword')).order_by('-c')
	
	return HttpResponseRedirect(course.class_url)

def course_add(request, course_id):
	course = Post.objects.get(id=course_id)
	keyword = request.GET.get('keyword', '')
	time = datetime.now()
	type = "favourite"
	ip = get_client_ip(request)
	
	if not request.user.is_authenticated:
		History.objects.create(course=course,keyword=keyword,time=time,type=type,ip=ip)
	else:
		History.objects.create(user=request.user,course=course,keyword=keyword,time=time,type=type,ip=ip)
	
	return HttpResponseRedirect('https://nol.ntu.edu.tw/nol/coursesearch/myschedule.php?add='+str(course.serial_num))