from django.db import models
from django.contrib.auth.models import User

from django.utils.timezone import now
from datetime import datetime

# Create your models here.

class serie(models.Model):
	HORROR = "horror"
	COMEDIA = "comedia"
	ACCION = "accion"
	DRAMA = "drama"

	CATEGORIES_CHOICES = (
		(HORROR, "Horror"),
		(COMEDIA, "Comedy"),
		(ACCION, "Action"),
		(DRAMA, "Drama")
	)

	name = models.CharField(max_length=100)
	release_date = models.DateField()
	rating = models.IntegerField(default=0)
	category = models.CharField(max_length=100,choices=CATEGORIES_CHOICES)

class cliente(models.Model):
	name = models.CharField(max_length=150)
	phone = models.CharField(max_length=50)
	address = models.CharField(max_length=200)
	release_date = models.DateField()
	def __str__(self):
		return self.name

class grupo_juego(models.Model):
	name = models.CharField(max_length=150)
	prize = models.TextField(blank=False)
	owner = models.ForeignKey(cliente,on_delete=models.CASCADE,related_name ="cli_grup")
	release_date = models.DateField(default=datetime.now)
	def __str__(self):
		return 'Usuario:{} /**/ Cliente: {} '.format(self.owner,self.name)

class user_cli(models.Model):
	id_user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="user_usercli")	
	id_cliente = models.ForeignKey(cliente,on_delete=models.CASCADE,related_name="cliente_usercli")
	def __str__(self):
		return 'Usuario:{} /**/ Cliente: {} '.format(self.id_user,self.id_cliente)

class cupo_juego(models.Model):
	username = models.CharField(max_length=200)
	puntos = models.IntegerField(default=0)
	id_user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="cupo_user")	
	id_group = models.ForeignKey(grupo_juego,on_delete=models.CASCADE,related_name="cupo_grupo")	


class token_reg(models.Model):
	token = models.CharField(max_length=200)
	id_group = models.ForeignKey(grupo_juego,on_delete=models.CASCADE,related_name="token_group")
	id_cupo = models.ForeignKey(cupo_juego,models.SET_NULL,blank=True,null=True)	
	burn_date = models.DateField(null=True,blank=True)







		




