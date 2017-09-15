#  -*- coding: utf-8 -*-
import pega_html as ph
import time
import random

def lista(informacoes):
	retorno = []
	for i in informacoes:
		retorno.append(i[0])
	return retorno

if __name__ == "__main__":
	
	niveis = [ph.Nivel.GRADUACAO, ph.Nivel.POS]
	campus = [ph.Campus.DARCY, ph.Campus.PLANALTINA, ph.Campus.CEILANDIA, ph.Campus.GAMA]
	
	cont = [1, 1, 1]
	for nivel in niveis:
		lista_disciplinas_total = []
		for campi in campus:
			lista_departamentos = lista(ph.Oferta.departamentos(nivel, campi))
			for departamento in lista_departamentos:
				lista_disci = lista(ph.Oferta.disciplinas(departamento, nivel, campi))
				#print lista_disci
				for disciplina in lista_disci:
					if not (disciplina in lista_disciplinas_total):
						lista_disciplinas_total.append(disciplina)
				print str(cont[0]) + '/' + str(len(niveis)) + "-" + str(cont[1]) + "/" + str(len(campus)) +\
						 "-" + str(cont[2]) + "/" + str(len(lista_departamentos))
				cont[2] += 1
			cont[1] += 1
			cont[2] = 1
		cont[0] += 1
		cont[1] = 1

		cont = 0
		for disciplina in lista_disciplinas_total:
			cont += 1
			print str(cont) + '/' + str(len(lista_disciplinas_total)) + " - " + disciplina
			ph.Oferta.espera(disciplina, nivel)
	
	
	'''
	cont = [1, 1, 1, 1]
	for nivel in niveis:
		for campi in campus:
			lista_departamentos = lista(Oferta.departamentos(nivel, campi, processo = 2))
			for departamento in lista_departamentos:
				lista_disci = lista(Oferta.disciplinas(departamento, nivel, campi, processo = 2))
				for disciplina in lista_disci:
					Oferta.turmas(disciplina, departamento, nivel, processo = 1)
					stri = '[' + str(cont[0]) + '/' + str(len(niveis)) + ']-'
					stri += '[' + str(cont[1]) + '/' + str(len(campus)) + ']-'
					stri += '[' + str(cont[2]) + '/' + str(len(lista_departamentos)) + ']-'
					stri += '[' + str(cont[3]) + '/' + str(len(lista_disci)) + ']:' + str(disciplina)
					#print stri
					#time.sleep(1)
					cont[3] += 1
				cont[3] = 1
				cont[2] += 1
			cont[2] = 1
			cont[1] += 1
		cont[1] = 1
		cont[1] += 1
	'''

	'''
	#disciplinas = range(100*1000, 210*1000)
	disciplinas = [169344]
	#Este codigo pega todas as ementas das disciplinas
	for disciplina in disciplinas:
		ph.Disciplina.informacoes(disciplina, processo = 0)
		print disciplina
		time.sleep(random.uniform(0, 0.5))
	'''
	
	'''
	lista_disci = open("Informacoes/temp/html/graduacao/Disciplinas_aux/lista_de_disciplinas.txt", "w")
	for i in xrange(100*1000, 101*1000):
		w = ph.Disciplina.informacoes(i, processo = 1)
	lista_disci.close()
	'''
	'''
	w = '116319'
	w = ph.Oferta.espera(w, processo = 1)
	for i in w:
		print i
	'''