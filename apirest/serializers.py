from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User

class apiSerializer(serializers.ModelSerializer):
	class Meta:
		model = serie
		fields= ('id','name','release_date','rating','category')
			

	def create(self,validated_data):
		"""
		Create and return a new `Serie` instance, given the validated data.
		"""
		return serie.objects.create(**validated_data)

	def update(self, instance, validated_data):
		"""
		Update and return an existing `Serie` instance, given the validated data.
		"""
		instance.name = validated_data.get('name', instance.name)
		instance.release_date = validated_data.get('release_date', instance.release_date)
		instance.rating = validated_data.get('rating', instance.rating)
		instance.category = validated_data.get('category', instance.category)
		instance.save()
		return instance

class userSeializer(serializers.ModelSerializer):
	"""docstring for ClassName"""
	class Meta:
		model = User
		fields = ('id','username','first_name','last_name')

class userCliSerializer(serializers.ModelSerializer):
	"""docstring for ClassName"""
	class Meta:
		model = user_cli
		fields = '__all__'

class clienteSerializer(serializers.ModelSerializer):
	"""docstring for ClassName"""
	class Meta:
		model = cliente
		fields = '__all__'

class relaCliSerializer(serializers.ModelSerializer):
	id_user = userSeializer()
	id_cliente = clienteSerializer()
	class Meta:
		model = user_cli
		fields = ('id','id_user','id_cliente')

class groupSerializer(serializers.ModelSerializer):
	"""docstring for ClassName"""
	class Meta:
		model = grupo_juego
		fields = '__all__'

class tokenSerializer(serializers.ModelSerializer):
	"""docstring for ClassName"""
	class Meta:
		model = token_reg
		fields = '__all__'