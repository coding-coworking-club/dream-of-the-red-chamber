from django.shortcuts import render
from .models import Post

# Create your views here.
def course_homepage(request):
	keyword = request.GET.get('keyword', '')
	course_list = Post.objects.filter(syllabus__contains=keyword)
	template_name='course/course_homepage.html'
	return render(request, template_name)

def course(request):
	keyword = request.GET.get('keyword', '')
	course_list = Post.objects.filter(syllabus__contains=keyword)
	template_name = 'course/course.html'
	context = {'course_list': course_list}
	return render(request, template_name, context)

def course_detail(request, course_id):
	course = Post.objects.get(id=course_id)
	template_name = 'course/course_detail.html'
	context = {'course':course}
	course.click_times += 1
	course.save()
	return render(request, template_name, context)
