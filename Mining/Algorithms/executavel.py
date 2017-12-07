#  -*- coding: utf-8 -*-

import defines
import auxiliar
import impress
#import cursos
import oferta
#import disciplina



def getch():
	import sys, tty, termios
	fd = sys.stdin.fileno()
	old_settings = termios.tcgetattr(fd)
	try:
		tty.setraw(sys.stdin.fileno())
		ch = sys.stdin.read(1)
	finally:
		termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
	return ch


def main_menu():
	print("\tMatricula WEB")
	print("\n")
	print("1) Curso")
	print("2) Oferta")
	print("3) Sair")
	print("\n")
	print("Digite sua opcao: ")

def Curso():
	pass


def Departamento(nivel, campi, departamento):
	disciplinas = oferta.disciplinas(departamento, nivel, campi)
	posicao = 0
	maximo = len(disciplinas)
	intervalo = [0, defines.linhas_tela if maximo > defines.linhas_tela else maximo]
	while 1:
		posicao, intervalo = impress.intervalo_update(posicao, maximo, intervalo)
		impress.departamento(nivel, campi, disciplinas, posicao, intervalo)

		
		while 1:
			resposta = getch()
			if resposta == 'w' or resposta == 's' or resposta == 'x' or resposta == 'f':
				break
		if resposta == 'w':
			posicao -= 1
		elif resposta == 's':
			posicao += 1
		elif resposta == 'f':
			Disciplina(nivel, campi, departamento, disciplinas[posicao])
		elif resposta == 'x':
			break


def Oferta(nivel):
	campus = [defines.Campus.DARCY, defines.Campus.PLANALTINA, defines.Campus.CEILANDIA, defines.Campus.GAMA]
	#campus = [defines.Campus.DARCY]
	departamentos = {}
	abrange = {}
	maximo = 0
	for campi in campus:
		departamentos[campi] = oferta.departamentos(nivel, campi)
		abrange[campi] = [maximo]
		maximo += len(departamentos[campi])
		abrange[campi].append(maximo-1)
	posicao = 0
	intervalo = [0, defines.linhas_tela if maximo > defines.linhas_tela else maximo]
	while 1:
		posicao, intervalo = impress.intervalo_update(posicao, maximo, intervalo)
		impress.campus(nivel, campus, departamentos, posicao, intervalo)
		
		while 1:
			resposta = getch()
			if resposta == 'w' or resposta == 's' or resposta == 'x' or resposta == 'f':
				break
		if resposta == 'w':
			posicao -= 1
		elif resposta == 's':
			posicao += 1
		elif resposta == 'f':
			for campi in campus:
				if abrange[campi][0] <= posicao <= abrange[campi][1]:
					break
			Departamento(campi, departamentos[campi][posicao-abrange[campi][0]])
		elif resposta == 'x':
			break


if __name__ == "__main__":
	while 1:
		main_menu()
		resposta = getch()
		if resposta == "1":
			Curso(defines.Nivel.GRADUACAO)
		elif(resposta == "2"):
			Oferta(defines.Nivel.GRADUACAO)
		elif(resposta == "3"):
			break