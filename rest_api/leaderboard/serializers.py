from django.contrib.auth.models import User, Group
from rest_framework import serializers
from leaderboard.models import School, ClassMeeting


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class SchoolSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = School
		fields = ['name', 'total_cm', 'year_cm', 'term_cm', 'month_cm', 'first_post']

class ClassMeetingSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = ClassMeeting
		fields = ['question', 'date', 'school']

