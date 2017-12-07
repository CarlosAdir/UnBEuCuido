#  -*- coding: utf-8 -*-
import defines
import os

def triangle():
	return "◆"

def intervalo_update(posicao, maximo, intervalo):
	if posicao < 0:
		posicao = 0
	elif posicao == maximo:
		posicao = maximo-1;
	if(posicao < intervalo[0]):
		intervalo[0] -= 1;
		intervalo[1] -= 1;
	elif(posicao > intervalo[1]):
		intervalo[0] += 1
		intervalo[1] += 1
	return posicao, intervalo

def departamento(nivel, campi, departamento, posicao, intervalo):
	os.system("clear")
	c = 0
	'''
	for campi in campus:
		for departamento in departamento[campi]:
			if intervalo[0] <= c:
				if posicao == c:
					print("  " + triangle(), end = ' ')
				else:
					print("   ", end = ' ')
				temp = [" " * ( 4 - len(departamento[0])) + departamento[0], \
						" " * ( 5 - len(departamento[1])) + departamento[1], \
						departamento[2]]
				print(temp[0] + " - " + temp[1] + " - " + temp[2])
			c += 1
			if c > intervalo[1]:
				return 1
	'''

def campus(nivel, campus, departamentos, posicao, intervalo):
	os.system("clear")
	c = 0
	for campi in campus:
		if campi == defines.Campus.DARCY:
			campi_name = "Darcy"
		if campi == defines.Campus.PLANALTINA:
			campi_name = "Planaltina"
		if campi == defines.Campus.CEILANDIA:
			campi_name = "Ceilandia"
		if campi == defines.Campus.GAMA:
			campi_name = "Gama"
		print(campi_name + ':')
		for departamento in departamentos[campi]:
			if intervalo[0] <= c:
				if posicao == c:
					print("  " + triangle(), end = ' ')
				else:
					print("   ", end = ' ')
				temp = [" " * ( 4 - len(departamento[0])) + departamento[0], \
						" " * ( 5 - len(departamento[1])) + departamento[1], \
						departamento[2]]
				print(temp[0] + " - " + temp[1] + " - " + temp[2])
			c += 1
			if c > intervalo[1]:
				return 1