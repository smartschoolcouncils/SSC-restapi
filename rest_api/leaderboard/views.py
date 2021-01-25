from django.contrib.auth.models import User, Group
from django.db.models import Count
from rest_framework import viewsets
from rest_framework import permissions
from leaderboard.serializers import UserSerializer, GroupSerializer, SchoolSerializer, ClassMeetingSerializer
from leaderboard.models import School, ClassMeeting
import pandas as pd
import datetime
import hashlib


def load_csv():
	df = pd.read_csv(r'/home/ssc/SmartSchoolCouncils/rest_api/SSC-restapi/rest_api/leaderboard/csv_files/school_questions.csv')

	today = datetime.date.today()

	summer_start = datetime.date(today.year, 4, 12)
	summer_end = datetime.date(today.year, 7, 31)

	spring_start = datetime.date(today.year, 1, 1)
	spring_end = datetime.date(today.year, 4, 11)

	autumn_start = datetime.date(today.year, 9, 1)
	autumn_end = datetime.date(today.year, 12, 31)

	current_start = today
	current_end = today

	if today <= spring_end and today >= spring_start:
		current_start = spring_start
		current_end = spring_end
	elif today <= summer_end and today >= summer_start:
		current_start = summer_start
		current_end = summer_end
	elif today <= autumn_end and today >= autumn_start:
		current_start = autumn_start
		current_end = autumn_end

	#Reset Values when new year, month, or term comes around
	
	#Reset for term
	if today == current_start:
		print("reseting term")
		for index, row in df.iterrows():

			if len(row) != 3:
				continue

			school_name = row['School Name']
			date = row['Session Date'].split('/')
			question = row['Question']

			today = datetime.date.today()

			if school_name == "" or school_name == "Coronavirus Daily Debates" or school_name == None or school_name == "TEST":
				continue
			
			if isinstance(school_name, float):
				continue

			school_name = school_name.upper()

			if School.objects.filter(name=school_name).exists():
				temp_school = School.objects.get(name=school_name)
				temp_school.term_cm = 0
				temp_school.save()

	#Reset for year
	if today == datetime.date(today.year, 1, 1):

		print("reseting year")
		for index, row in df.iterrows():

			if len(row) != 3:
				continue

			school_name = row['School Name']
			date = row['Session Date'].split('/')
			question = row['Question']

			today = datetime.date.today()

			if school_name == "" or school_name == "Coronavirus Daily Debates" or school_name == None or school_name == "TEST":
				continue
			
			if isinstance(school_name, float):
				continue

			school_name = school_name.upper()

			if School.objects.filter(name=school_name).exists():
				temp_school = School.objects.get(name=school_name)
				temp_school.year_cm = 0
				temp_school.save()

	#Reset for Month
	if today == datetime.date(today.year, today.month, 1):

		print("reseting month")
		for index, row in df.iterrows():

			if len(row) != 3:
				continue

			school_name = row['School Name']
			date = row['Session Date'].split('/')
			question = row['Question']

			today = datetime.date.today()

			if school_name == "" or school_name == "Coronavirus Daily Debates" or school_name == None or school_name == "TEST":
				continue
			
			if isinstance(school_name, float):
				continue

			school_name = school_name.upper()

			if School.objects.filter(name=school_name).exists():
				temp_school = School.objects.get(name=school_name)
				temp_school.month_cm = 0
				temp_school.save()

	WordDict.objects.all().delete()

	# Load the Values

	for index, row in df.iterrows():

		if len(row) != 3:
			continue

		school_name = row['School Name']
		date = row['Session Date'].split('/')
		question = row['Question']

		#Validate that row contains school

		if school_name == "" or school_name == "Coronavirus Daily Debates" or school_name == None or school_name == "test":
			continue
		
		if isinstance(school_name, float):
			continue

		school_name = school_name.upper()

		#Check if school already exists

		if not School.objects.filter(name=school_name).exists():
			temp_school = School.objects.create(name=school_name, total_cm=0, year_cm=0, term_cm=0, month_cm=0, first_post=today)
			temp_school.save()

		date_field = datetime.date(int(date[2]), int(date[1]), int(date[0]))

		temp_school = School.objects.get(name=school_name)


		#Check if CM already exists

		if not ClassMeeting.objects.filter(school=temp_school, date=date_field, question=question).exists():	#Create Question Map

			if date_field > today-timedelta(days=60):

				word_count = {}
				question = question.rstrip().split(' ')

				for word in question:
					if word in word_count:
						word_count[word] += 1
					else:
						word_count[word] = 1

				wordDict = ''

				#Check if worddict exists already/make one
				if WordDict.objects.filter(wd=word_count).exists():
					wordDict = WordDict.objects.get(wd=word_count)
				else:
					wordDict = WordDict.objects.create(wd=word_count, question=question)
				wordDict.save()

				temp_class = ClassMeeting.objects.create(school=temp_school, date=date_field, question=question)
				temp_class.save()


		
			#Update school stats for CM

			temp_school.total_cm += 1

			if date_field.year == today.year:
				temp_school.year_cm += 1

			if date_field <= current_end and date_field >= current_start:
				temp_school.term_cm += 1

			if date_field >= datetime.date(today.year, today.month, 1):
				temp_school.month_cm += 1
			
			temp_school.save()

def check_hash():
	md5 = ''
	if len(MD5_Hash.objects.all()) > 0:
		md5 = MD5_Hash.objects.get(id=1)
	else:

		with open('/home/ssc/SmartSchoolCouncils/rest_api/SSC-restapi/rest_api/leaderboard/csv_files/school_questions.csv') as f:
			while True:
				data = f.read(BUF_SIZE)
				if not data:
					break
				md5.update(data)
		
			md5 = MD5_Hash.objects.create(md5=md5)
			md5.save()

	return md5.same_hash

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class SchoolViewSet(viewsets.ModelViewSet):

	if not check_hash:
		load_csv()
	
	queryset = School.objects.all()
	serializer_class = SchoolSerializer
	permission_classes = [permissions.AllowAny]


class TopAllTimeViewSet(viewsets.ModelViewSet):
	
	if not check_hash:
		load_csv()
	
	queryset = School.objects.order_by('-total_cm')[:10]

	serializer_class = SchoolSerializer

	permission_classes = [permissions.AllowAny]


class TopYearViewSet(viewsets.ModelViewSet):

	if not check_hash:
		load_csv()

	queryset = School.objects.order_by('-year_cm')[:10]

	serializer_class = SchoolSerializer
	
	permission_classes = [permissions.AllowAny]

class TopTermViewSet(viewsets.ModelViewSet):
	if not check_hash:
		load_csv()
	
	queryset = School.objects.order_by('-term_cm')[:10]

	serializer_class = SchoolSerializer
	
	permission_classes = [permissions.AllowAny]

class TopMonthViewSet(viewsets.ModelViewSet):
	if not check_hash:
		load_csv()

	queryset = School.objects.order_by('-month_cm')[:10]

	serializer_class = SchoolSerializer
	
	permission_classes = [permissions.AllowAny]

class MostRecentQViewSet(viewsets.ModelViewSet):
	if not check_hash:
		load_csv()

	queryset = ClassMeeting.objects.order_by('-date')[:10]

	serializer_class = ClassMeetingSerializer

	permission_classes = [permissions.AllowAny]

'''
class TopTrendingCMQViewSet(viewsets.ModelViewSet):
	if !check_hash:
		load_csv()

	queryset = WordDict.objects.annotate(cm_count=Count('cms')).order_by('-cm_count')[:10]
	serializer_class = WordDictSerializer
	permission_classes = [permissions.AllowAny]
'''
	
	

