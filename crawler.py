#!/usr/bin/python
# -*- coding: big5 -*-

# first line is indicating python
# second line is indicating encoding
# hierachy of the variables: there are a lot of course in one page
 
import html2text
import requests
import re
import time
import json

prefix = 'http://nol.ntu.edu.tw/nol/coursesearch/'
num_course_in_one_page = 130  # how many courses in one page
current_sem = '108-1'  # which semster to crawl

first_page_url = (prefix + 
                 ('search_result.php?alltime=yes&allproced=yes&cstype=1&csname=&current_sem=' + current_sem +
                  '&op=stu&'
                  'startrec=0'
                  '&week1=&week2=&week3=&week4=&week5=&week6=&'
                  'proced0=&proced1=&proced2=&proced3=&proced4=&procedE=&proced5=&proced6=&proced7=&proced8=&proced9=&'
                  'procedA=&procedB=&procedC=&procedD=&'
                  'allsel=yes&selCode1=&selCode2=&selCode3=&'
                  'page_cnt=') + str(num_course_in_one_page))

# print(first_page_url)
# startrec indicates the course id on the top of the page
# page_cnt indicates the number of courses in one page


response_first_page = requests.get(first_page_url)
response_first_page.encoding = 'big5'                 
# the course website is encoded through big5

pattern_total_num_course = re.compile(' <b>(.+)</b>')
total_num_course = int(re.search(pattern_total_num_course, response_first_page.text).group()[4:-4])
# get the total number of courses
print(total_num_course)

# pattern for each column
pattern_course_inform   = re.compile('課程名稱\|(.*)開課學期\|')
pattern_course_semster  = re.compile('開課學期\|(.*)授課對象\|')
pattern_course_student  = re.compile('授課對象\|(.*)授課教師\|')
pattern_course_teacher  = re.compile('授課教師\|(.*)課號\|')
pattern_course_code     = re.compile('課號\|(.*)課程識別碼\|')
pattern_course_ID       = re.compile('課程識別碼\|(.*)班次\|')
pattern_course_class    = re.compile('班次\|(.*)學分\|')
pattern_course_credits  = re.compile('學分\|(.*)全/半年\|')
pattern_course_year     = re.compile('全/半年\|(.*)必/選修\|')
pattern_course_category = re.compile('必/選修\|(.*)上課時間\|')
pattern_course_time     = re.compile('上課時間\|(.*)上課地點\|')
pattern_course_location = re.compile('上課地點\|(.*)備註\|')
pattern_course_bonus    = re.compile('備註\|(.*)Ceiba 課程網頁\|')
pattern_course_ceiba    = re.compile('Ceiba 課程網頁\|(.*)課程簡介影片\|')
pattern_course_no_ceiba = re.compile('備註\|(.*)課程簡介影片\|')
pattern_course_half     = re.compile('備註\|(.*)課程大綱\|')
# 前14項分別為"課程名稱","開課學期","授課對象","授課教師","課號","課程識別碼","班次","學分","全年/半年","必修/選修","上課時間","上課地點","備註","ceiba課程網站"
# 第15項為"課程大綱"（syllabus），課程大綱包含該網頁中所有文字內容
# 第16項為"課程大綱網址"（url）
# 會有兩種例外：只有一半(像國文)、沒有ceiba(像學士論文下)

frame = []
course_number = 0
pattern_courses = re.compile(r'print_table(.+?)lang=CH')  
# if there is no '?', re will search for longest string, which will lead to error in our case

start_time = (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
print(start_time)

while course_number < total_num_course:
    
    page_url = (prefix + 
               ('search_result.php?alltime=yes&allproced=yes&cstype=1&csname=&current_sem=' + current_sem +
                '&op=stu&'
                'startrec=' + str(course_number) +
                '&week1=&week2=&week3=&week4=&week5=&week6=&'
                'proced0=&proced1=&proced2=&proced3=&proced4=&procedE=&proced5=&proced6=&proced7=&proced8=&proced9=&'
                'procedA=&procedB=&procedC=&procedD=&'
                'allsel=yes&selCode1=&selCode2=&selCode3=&'
                'page_cnt=') + str(num_course_in_one_page))

    page_response = requests.get(page_url)
    page_response.encoding = 'big5'
    courses_in_page = pattern_courses.findall(page_response.text)
    
    for course in courses_in_page:
        course_url = prefix + 'print_table' + course + 'lang=CH'
        print(course_url)        

        course_response = requests.get(course_url)
        print(course_response.status_code)
        course_response.encoding = 'big5'
        
        raw_text = html2text.html2text(course_response.text)
        syllabus = re.sub('---', '', "".join(raw_text.split('\n')))
        # print(syllabus)
        
        course_dict = {}
        course_dict['課程名稱']       = re.search(pattern_course_inform  , syllabus).group().split('|')[1].strip()
        course_dict['開課學期']       = re.search(pattern_course_semster , syllabus).group().split('|')[1][:-4].strip()
        course_dict['授課老師']       = re.search(pattern_course_teacher , syllabus).group().split('|')[1][:-2].strip()
        course_dict['課號']           = re.search(pattern_course_code    , syllabus).group().split('|')[1][:-5].strip()
        course_dict['課程識別碼']     = re.search(pattern_course_ID      , syllabus).group().split('|')[1][:-2].strip()
        course_dict['班次']           = re.search(pattern_course_class   , syllabus).group().split('|')[1][:-2].strip()
        course_dict['學分']           = re.search(pattern_course_credits , syllabus).group().split('|')[1][:-4].strip()
        course_dict['全/半年']        = re.search(pattern_course_year    , syllabus).group().split('|')[1][:-4].strip()
        course_dict['必/選修']        = re.search(pattern_course_category, syllabus).group().split('|')[1][:-4].strip()
        course_dict['上課時間']       = re.search(pattern_course_time    , syllabus).group().split('|')[1][:-4].strip()
        course_dict['上課地點']       = re.search(pattern_course_location, syllabus).group().split('|')[1][:-2].strip()
        course_dict['課程大綱']       = syllabus.strip()     
        course_dict['課程大綱網址']   = course_url
        
        try:
            course_dict['備註']           = re.search(pattern_course_bonus   , syllabus).group().split('|')[1][:-10].strip()
            course_dict['Ceiba 課程網頁'] = re.search(pattern_course_ceiba   , syllabus).group().split('|')[1][:-6].strip()

        except AttributeError:
            try:
                course_dict['備註']           = re.search(pattern_course_half     , syllabus).group().split('|')[1][:-4].strip()
            except AttributeError:
                course_dict['備註']           = re.search(pattern_course_no_ceiba , syllabus).group().split('|')[1].strip()    
                # 這裡我充滿了疑惑，到底是要不要加[:-n]
        # print(course_dict)
        
        frame.append(course_dict)
 
    print('page starts from course' + str(course_number) + ' is done!')
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

    course_number += num_course_in_one_page
    time.sleep(2)

print(start_time)

# save as json
final_file = 'all_course-' + current_sem + '.json'
with open(final_file, 'w') as fout:
    json.dump(frame, fout)    









