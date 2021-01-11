from django.db import models

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

