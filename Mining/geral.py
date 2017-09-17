#  -*- coding: utf-8 -*-
import pega_html as ph
import time
import random
import os

def lista(informacoes):
	if len(informacoes):
		if(len(informacoes[0])):
			retorno = []
			for i in informacoes:
				retorno.append(i[0])
			return retorno
	return []
	


if __name__ == "__main__":
	
	# niveis = [ph.Nivel.GRADUACAO, ph.Nivel.POS]
	niveis = [ph.Nivel.GRADUACAO]
	#campus = [ph.Campus.DARCY, ph.Campus.PLANALTINA, ph.Campus.CEILANDIA, ph.Campus.GAMA]
	#campus = [ph.Campus.DARCY]
	
	'''
	# PARA PEGAR TODOS OS DEPARTAMENTOS E LISTA DE DISCIPLINA EM CADA DEPARTAMENTO
	cont = [1, 1, 1]
	for nivel in niveis:
		for campi in campus:
			# Captura a lista de departamentos de um campi
			lista_departamentos = lista(ph.Oferta.departamentos(nivel, campi)) 
			for departamento in lista_departamentos:
				
				# SOMENTE PARA IMPRIMIR
				stri  = '[' + str(cont[0]) + '/' + str(len(niveis)) 			 + ']-'
				stri += '[' + str(cont[1]) + '/' + str(len(campus)) 			 + ']-'
				stri += '[' + str(cont[2]) + '/' + str(len(lista_departamentos)) + ']:' + str(departamento)
				print stri

				# Captura a lista de disciplinas dentro de um dep
				lista_disci = lista(ph.Oferta.disciplinas(departamento, nivel, campi))

				# AJUDAR PARA IMPRIMIR
				cont[2] += 1
			cont[1] += 1
			cont[2] = 1
		cont[0] += 1
		cont[1] = 1
	'''

	'''
	# PARA PEGAR TODAS AS LISTAS DE ESPERA
	cont = [1, 1, 1]
	for nivel in niveis:
		lista_disciplinas_total = []
		for campi in campus:
			# Captura a lista de departamentos de um campi
			lista_departamentos = lista(ph.Oferta.departamentos(nivel, campi)) 
			for departamento in lista_departamentos:
				
				# SOMENTE PARA IMPRIMIR
				stri  = '[' + str(cont[0]) + '/' + str(len(niveis)) 			 + ']-'
				stri += '[' + str(cont[1]) + '/' + str(len(campus)) 			 + ']-'
				stri += '[' + str(cont[2]) + '/' + str(len(lista_departamentos)) + ']-' + str(departamento)
				print stri

				# Captura a lista de disciplinas dentro de um dep
				lista_disci = lista(ph.Oferta.disciplinas(departamento, nivel, campi)) 
				for disciplina in lista_disci:
					if not (disciplina in lista_disciplinas_total): # Porque departamentos diferentes oferecem a mesma disciplina
						lista_disciplinas_total.append(disciplina)
				
				# AJUDAR PARA IMPRIMIR 				
				cont[2] += 1
			cont[1] += 1
			cont[2] = 1
		cont[0] += 1
		cont[1] = 1

		cont2 = 0
		for disciplina in lista_disciplinas_total:
			cont2 += 1
			print str(cont2) + '/' + str(len(lista_disciplinas_total)) + " - " + str(disciplina)
			ph.Oferta.espera(disciplina, nivel)
	
	'''

	
	'''
	# PARA CRIAR PASTAS SE NAO EXISTIREM
	cria_pasta("Informacoes")
	cria_pasta("Informacoes/temp")
	for i in ["html", "tratado"]:
		cria_pasta("Informacoes/temp/" + i)
		for nivel in niveis:
			cria_pasta("Informacoes/temp/" + i + "/" + nivel)
			for p in ["Cursos", "Disciplinas", "Oferta", "Oferta/espera", "Oferta/turmas"]:
				cria_pasta("Informacoes/temp/" + i + "/" + nivel + "/" + p)
	'''

	'''
	# PARA PEGAR TODAS AS TURMAS
	cont = [1, 1, 1, 1]
	for nivel in niveis:
		for campi in campus:
			# Captura a lista de departamentos de um campi
			lista_departamentos = lista(ph.Oferta.departamentos(nivel, campi))
			for departamento in lista_departamentos:
				# Captura a lista de disciplinas dentro de um dep
				lista_disci = lista(ph.Oferta.disciplinas(departamento, nivel, campi))
				for disciplina in lista_disci:
					# Captura a lista de turmas dentro de uma disciplina e departamento
					ph.Oferta.turmas(disciplina, departamento, nivel, processo = 1)

					# SOMENTE PARA IMPRIMIR
					stri  = '[' + str(cont[0]) + '/' + str(len(niveis)) 			 + ']-'
					stri += '[' + str(cont[1]) + '/' + str(len(campus)) 			 + ']-'
					stri += '[' + str(cont[2]) + '/' + str(len(lista_departamentos)) + ']-'
					stri += '[' + str(cont[3]) + '/' + str(len(lista_disci)) 		 + ']:' + str(disciplina)
					print stri
					

					# AJUDAR PARA IMPRIMIR 	
					cont[3] += 1
				cont[3] = 1
				cont[2] += 1
			cont[2] = 1
			cont[1] += 1
		cont[1] = 1
		cont[1] += 1
	'''



	for nivel in niveis:
		lista_disci = ["122360", "113034", "113476", "113476"]
		lista_departamentos = ["039", "113", "116", "650"]
		for i in xrange(len(lista_disci)):
			# Captura a lista de turmas dentro de uma disciplina e departamento
			disciplina = lista_disci[i]
			departamento = lista_departamentos[i]
			ph.Oferta.turmas(disciplina, departamento, nivel, processo = 1)


	'''
	#disciplinas = range(100*1000, 210*1000)
	disciplinas = [169344]
	#Este codigo pega todas as ementas das disciplinas
	for disciplina in disciplinas:
		ph.Disciplina.informacoes(disciplina)
		print disciplina
	'''
	
	'''
	lista_disci = open("Informacoes/temp/html/graduacao/Disciplinas_aux/lista_de_disciplinas.txt", "w")
	for i in xrange(100*1000, 101*1000):
		w = ph.Disciplina.informacoes(i)
	lista_disci.close()
	'''
	'''
	w = '116319'
	w = ph.Oferta.espera(w)
	for i in w:
		print i
	'''