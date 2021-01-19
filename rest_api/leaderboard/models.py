from django.db import models
from django_mysql.models import JSONField
import hashlib

# Create your models here.

class School(models.Model):
	name = models.CharField(max_length=100, unique=True)
	total_cm = models.IntegerField(default=0)
	year_cm = models.IntegerField(default=0)
	term_cm = models.IntegerField(default=0)
	month_cm = models.IntegerField(default=0)
	first_post = models.DateField(auto_now=True)

class ClassMeeting(models.Model):
	question = models.CharField(max_length=1000, default="")
	date = models.DateField(null=True, blank=True)
	school = models.ForeignKey(School, on_delete=models.CASCADE, null=True, blank=True)

class WordDict(models.Model):
	question = models.CharField(max_length=1000, default="")
	wd = JSONField()
	cms = models.ManyToManyField(ClassMeeting)
	date = models.DateField(null=True, blank=True)

	def to_py(self, value):
		if value == "":
			return None

		try:
			if isinstance(value, str):
				return json.loads(value)
		except ValueError:
			pass
		return value

	def from_db_value(self, value):
		return self.to_py(value)

	def to_db_string(self, value):
		if value == "":
			return None
		if isinstance(value, dict):
			value = json.dumps(value, cls=DjangoJSONEncoder)
		return value

class MD5_Hash(models.Model):
	md5 = models.CharField()

	def same_hash():
		BUF_SIZE = 65536
		md5 = hashlib.md5()

		with open('/home/ssc/SmartSchoolCouncils/rest_api/SSC-restapi/rest_api/leaderboard/csv_files/school_questions.csv') as f:
			while True:
				data = f.read(BUF_SIZE)
				if not data:
					break
				md5.update(data)

		if str(md5) == str(self.md5):
			return True
		else:
			return False
