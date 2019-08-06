from django.db import models

# Create your models here.
class Post(models.Model):
	serial_num = models.PositiveIntegerField(default=5) #流水號
	stu_department = models.CharField(max_length=50,default="",blank=True, null=True) #授課對象
	class_code = models.CharField(max_length=30,default=None) #課號
	class_order = models.CharField(max_length=30,default=None) #班次
	class_name = models.CharField(max_length=100,default=None) #課程名稱
	credit = models.PositiveIntegerField(default=None) #學分
	identification_code = models.CharField(max_length=100,default=None)#課程識別碼
	half_year = models.CharField(max_length=10,default=None) #全年/半年
	required = models.CharField(max_length=10,default=None) #必修/選修
	teacher = models.CharField(max_length=15,default=None) #授課教師
	add_type = models.PositiveIntegerField(default=None) #加選方式
	class_time = models.CharField(max_length=30,default=None) #上課時間
	place = models.CharField(max_length=30,default=None) #上課地點
	stu_number = models.CharField(max_length=50,default=None)#總人數
	click_times = models.IntegerField(default=0) #點擊次數
	constraints = models.CharField(max_length=100,default=None)#選課限制條件
	remark = models.TextField(default=None)#備註
	class_url = models.URLField(default=None) #課程網址
	syllabus = models.TextField(default=None) #課程大綱
	
	def __str__(self):
		return self.teacher+" "+self.class_name
	
