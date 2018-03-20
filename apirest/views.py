from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from apirest.models import *
from apirest.serializers import *
from apirest.forms.forms import userForm
from django.contrib.auth import login
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from random import randint
from django.shortcuts import *
from django.utils.timezone import now
from datetime import datetime

from rest_framework.renderers import JSONRenderer
from rest_framework import generics,permissions
from rest_framework.authtoken.models import Token
from rest_framework.parsers import JSONParser
from rest_framework.response import Response


 
# Create your views here.
class JSONResponse(HttpResponse):

	data_response ={
		"error":{
			"error":"serie no encontrada"
			},
		"correcto":{
			"correcto":"serie encontrada"
			},
	}

	def __init__(self,data,**kwargs):
		content= JSONRenderer().render(data)
		kwargs['content_type'] = "application/json"
		super(JSONResponse,self).__init__(content,**kwargs)
		

@csrf_exempt
def serie_list(request):
	if request.method == "GET":
		series = serie.objects.all()
		serializer = apiSerializer(series,many=True)
		return JSONResponse(serializer.data)
	elif request.method=="POST":
		data=JSONParser().parse(request)
		serializer =apiSerializer(data=data)
		if serializer.is_valid():
			serializer.save()
			return JSONResponse(serializer.data,status=201)
		return JSONResponse(serializer.errors,status =400)

@csrf_exempt
def serie_detail(request, pk):
	print (request)
	try:
		sr = serie.objects.get(id=pk)
	except serie.DoesNotExist:
		return JSONResponse(JSONResponse.data_response["error"],status=404)

	if request.method =="GET":
		serializer = apiSerializer(sr)
		return JSONResponse(serializer.data)

	elif request.method=="PUT":
		data = JSONParser().parse(request)
		serializer= apiSerializer(sr,data=data)
		if serializer.is_valid():
			serializer.save()
			return JSONResponse(serializer.data)
		return JSONResponse(serializer.errors,status=400)

	elif request.method == "DELETE":
		sr.delete()
		return HttpResponse(status=204)
'''
EJEMPLO DE ENVIO 
{"category":"drama",
"name":"quecosass",
"release_date":"2004-09-22",
"rating":"3"}
'''
def addUser(request):
	form = userForm()
	if request.method=="POST":
		form = userForm(request.POST)
		if form.is_valid():
			new_user = User.objects.create_user(**form.cleaned_data)
			token = Token.objects.create(user=new_user)
		else:
			form = userForm()
	return render(request,'adduser.html',{'form':form})

def generateToken():
	if request.method=="POST":
		lett = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
		letras = list(lett)
		token = ""		
		for x in range(0,7):
			numero = randint(0, 9)
			if (x == 0) | (x == 2):
				token+=letras[randint(0, len(letras)-1)]
			else:
				token +=str(numero)
		return JSONResponse(token,status=200)

class Register(generics.CreateAPIView):
	permission_classes = (permissions.AllowAny,)
	def post(self,request,*args,**kwargs):
		username = request.POST.get('username')
		email = request.POST.get('email')
		password = request.POST.get('password')
		first_name = request.POST.get('first_name')
		last_name = request.POST.get('last_name')

		new_user = User.objects.create_user(username,email,password)
		new_user.first_name=first_name
		new_user.last_name = last_name
		new_user.save()
		token = Token.objects.create(user = new_user)
		return Response({"mensaje":"Usuario creado con el token "+token.key})

class ChangePassword(generics.CreateAPIView):
	permission_classes = (permissions.IsAuthenticated,)
	def post(self,request,*args,**kwargs):
		user = get_object_or_404(User,username=request.user)
		user.set_password(request.POST.get("new_pass"))
		user.save()
		return Response({"mensaje":"Password actualizado correctamente"})

class my_profile(generics.CreateAPIView):
	permission_classes = (permissions.IsAuthenticated,)
	def post(self,request,*args,**kwargs):
		user = User.objects.filter(username = request.user)[0]
		cliente = request.POST.get('id_cliente')
		user_cl = user_cli.objects.filter(id_user_id=user.id,id_cliente_id=cliente)
		if len(user_cl)<1:
			return JSONResponse({'mensaje':'no existe relacion'})
		token = utils.generateToken()
		us = userCliSerializer(user_cl,many=True)
		return JSONResponse(us.data,status=200)

class create_group(generics.CreateAPIView):
	permission_classes = (permissions.IsAuthenticated,)
	def post(self,request,*args,**kwargs):
		name = request.POST.get("name_group")
		prize = request.POST.get("prize")
		owner = request.POST.get("id_cliente")
		user = User.objects.filter(username = request.user)[0]
		user_cl = user_cli.objects.filter(id_user_id=user.id,id_cliente_id=owner)
		if len(user_cl)<1:
			return JSONResponse({'mensaje':'no existe relacion'})

		group = grupo_juego.objects.create(owner_id=1)
		group.name = name
		group.prize = prize
		group.save()
		return Response({"mensaje":"grupo creado correctamente"})

class list_groups(generics.CreateAPIView):
	permission_classes = (permissions.IsAuthenticated,)
	def post(self,request,*args,**kwargs):
		user = User.objects.get(username = request.user)
		cliente = request.POST.get('id_cliente')
		cli_us = user_cli.objects.filter(id_user__id=user.id,id_cliente__id = cliente)
		if len(cli_us)>0:
			grupos = grupo_juego.objects.filter(owner_id__id=cliente)
			cc = groupSerializer(grupos,many=True)
			return JSONResponse(cc.data)
		else:
			return Response({"error":"no existe relacion entre cliente y Usuario"})

class create_token(generics.CreateAPIView):
	permission_classes = (permissions.IsAuthenticated,)
	def post(self,request,*args,**kwargs):
		user = User.objects.get(username = request.user)
		grupo = request.POST.get('id_group')
		grupos = grupo_juego.objects.filter(id=grupo)
		if len(grupos)>0:
			cli_us = user_cli.objects.filter(id_user__id=user.id,id_cliente__id = grupos[0].owner_id)
			if len(cli_us)>0:
				token = utils.generateToken()
				tok  = token_reg.objects.create(id_group_id=grupo)
				tok.token = token
				tok.save()
				tt = tokenSerializer(tok)
				return JSONResponse(tt.data)
		else:
			return Response({"error":"no existe relacion entre cliente y Usuario"})

class burn_token(generics.CreateAPIView):
	permission_classes = (permissions.IsAuthenticated,)
	def post(self,request,*args,**kwargs):
		user = User.objects.get(username = request.user)
		username = request.POST.get('username')
		mi_token = request.POST.get('token')
		try:
			tok  = token_reg.objects.get(token=mi_token,id_cupo__isnull=True)
			cupo = cupo_juego.objects.create(username=username,id_group=tok.id_group,id_user=user)
			tok.id_cupo = cupo
			tok.burn_date = datetime.now().strftime('%Y-%m-%d')
			tok.save()
			tt = tokenSerializer(tok)
			return JSONResponse(tt.data)
		except:
			return Response({"mensaje":"No existe token"})
			


class utils():
	def generateToken():
		lett = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
		letras = list(lett)
		token = ""		
		for x in range(0,7):
			numero = randint(0, 9)
			if (x == 0) | (x == 2):
				token+=letras[randint(0, len(letras)-1)]
			else:
				token +=str(numero)
		return token	