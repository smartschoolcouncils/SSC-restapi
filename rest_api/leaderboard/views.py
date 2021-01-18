from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from leaderboard.serializers import UserSerializer, GroupSerializer, SchoolSerializer
from leaderboard.models import School, ClassMeeting
import pandas as pd
import datetime

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

	# Load the Values

	for index, row in df.iterrows():

		if len(row) != 3:
			continue

		school_name = row['School Name']
		date = row['Session Date'].split('/')
		question = row['Question']


		if school_name == "" or school_name == "Coronavirus Daily Debates" or school_name == None or school_name == "test":
			continue
		
		if isinstance(school_name, float):
			continue

		school_name = school_name.upper()

		if not School.objects.filter(name=school_name).exists():
			temp_school = School.objects.create(name=school_name, total_cm=0, year_cm=0, term_cm=0, month_cm=0, first_post=today)
			temp_school.save()

		date_field = datetime.date(int(date[2]), int(date[1]), int(date[0]))

		temp_school = School.objects.get(name=school_name)


		if not ClassMeeting.objects.filter(school=temp_school, date=date_field, question=question).exists():
			temp_class = ClassMeeting.objects.create(school=temp_school, date=date_field, question=question)
			temp_class.save()

			temp_school.total_cm += 1

			if date_field.year == today.year:
				temp_school.year_cm += 1

			if date_field <= current_end and date_field >= current_start:
				temp_school.term_cm += 1

			if date_field >= datetime.date(today.year, today.month, 1):
				temp_school.month_cm += 1
			
			temp_school.save()

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

	load_csv()
	queryset = School.objects.all()
	serializer_class = SchoolSerializer
	permission_classes = [permissions.AllowAny]


class TopAllTimeViewSet(viewsets.ModelViewSet):
	
	load_csv()
	queryset = School.objects.order_by('-total_cm')

	serializer_class = SchoolSerializer

	permission_classes = [permissions.AllowAny]


class TopYearViewSet(viewsets.ModelViewSet):
	load_csv()
	queryset = School.objects.order_by('-year_cm')

	serializer_class = SchoolSerializer
	
	permission_classes = [permissions.AllowAny]

class TopTermViewSet(viewsets.ModelViewSet):
	load_csv()
	queryset = School.objects.order_by('-term_cm')

	serializer_class = SchoolSerializer
	
	permission_classes = [permissions.AllowAny]

class TopMonthViewSet(viewsets.ModelViewSet):
	load_csv()
	queryset = School.objects.order_by('-month_cm')

	serializer_class = SchoolSerializer
	
	permission_classes = [permissions.AllowAny]

class MostRecentQViewSet(viewsets.ModelViewSet):
	load_csv()
	queryset = ClassMeeting.objects.order_by('-date')

	serializer_class = ClassMeetingSerializer

	permission_classes = [permissions.AllowAny]

