#  -*- coding: utf-8 -*-


import re
import requests
import datetime
import time

from os import system
from mwebcrawler import *
#from teste import imprime_formatado_com_colunas






def imprime_formatado_com_colunas(parametro, arquivo, identacao = 0):
	soma = 0
	arquivo.write('\t'*identacao)
	tipo = type(parametro)
	if tipo == str:
		arquivo.write("'" + parametro + "'\n")
	elif tipo == list:
		for i in parametro:
			soma += imprime_formatado_com_colunas(i, arquivo, identacao+1)
	elif tipo == tuple:
		for i in parametro:
			soma += imprime_formatado_com_colunas(i, arquivo, identacao+1)
	elif tipo == dict:
		for i in parametro:
			arquivo.write('\t'*identacao)
			if type(i) == str:
				arquivo.write("'" + i + "'" + ':\n')
			else:
				arquivo.write(str(i) + ':\n')
			soma += imprime_formatado_com_colunas(parametro[i], arquivo, identacao+1)
	elif tipo == int:
		arquivo.write(str(parametro) + '\n')
	elif tipo == float:
		arquivo.write(str(parametro) + '\n')
	else:
		return 1+soma
	return soma


def Armazena_disciplinas(caminho, intervalo, arq_erro, arq_exi, arq_falta, delay = 3, mostrar = True):
	ultimo_existente = 0
	for i in xrange(intervalo[0], intervalo[1]+1):
		disciplinas = Disciplina.informacoes(i)
		if len(disciplinas):
			ultimo_existente = i
			arq_exi.write(str(i) + '\n')
			arquivo = open(caminho + str(i) + ".txt", "w")
			erro = imprime_formatado_com_colunas(disciplinas, arquivo)
			arquivo.close()
			if erro:
				arq_erro.write(str(i) + '\n')
		else:
			arq_falta.write(str(i)+'\n')
		if mostrar:
			system("clear")
			print 'Iniciado !!!\n\n'
			print "Ultimo existente: %d" % ultimo_existente
			print "Atual:            %d" % i
		time.sleep(delay)
	if mostrar:
		print "Finalizado!!!"

def Armazena_departamentos(caminho):
	'''
	Esta funcao armazena os departamentos existentes por pasta, com um arquivo dentro chamado informacoes
	e dentro dessa pasta há outras informações como cada disciplina e turma que é oferecida
	'''
	departamentos = Oferta.departamentos()
	for i in departamentos:
		system("mkdir " + caminho + i)
		arquivo = open(caminho+i + "/descricao.txt", "w")
		arquivo.write(i + '\n')
		erro = imprime_formatado_com_colunas(i, arquivo)
		if erro:
			arq_erro = open(caminho+i+"/erro.txt", "w")
			arq_erro.close()
		




if __name__ == '__main__':

	data = datetime.datetime.now()
	data = (data.year, data.month, data.day, data.hour, data.minute)
	data = "%s_%s_%s_%s_%s" % data

	system("mkdir MW/" + data)
	system("mkdir MW/" + data + "/Alunos");
	system("mkdir MW/" + data + "/Professores");
	system("mkdir MW/" + data + "/Disciplinas");
	system("mkdir MW/" + data + "/Departamentos");

	erro_alunos = open("MW/" + data + "/Alunos/erro.txt", "w")
	erro_professores = open("MW/" + data + "/Professores/erro.txt", "w")
	erro_disciplinas = open("MW/" + data + "/Disciplinas/erro.txt", "w")
	erro_departamentos = open("MW/" + data + "/Departamentos/erro.txt", "w")

	falta_alunos = open("MW/" + data + "/Alunos/falta.txt", "w")
	falta_professores = open("MW/" + data + "/Professores/falta.txt", "w")
	falta_disciplinas = open("MW/" + data + "/Disciplinas/falta.txt", "w")
	falta_departamentos = open("MW/" + data + "/Departamentos/falta.txt", "w")

	existe_alunos = open("MW/" + data + "/Alunos/existe.txt", "w")
	existe_professores = open("MW/" + data + "/Professores/existe.txt", "w")
	existe_disciplinas = open("MW/" + data + "/Disciplinas/existe.txt", "w")
	existe_departamentos = open("MW/" + data + "/Departamentos/existe.txt", "w")

	a = input("Digite o primeiro valor:  ")
	b = input("Digite o segundo valor:   ")
	t = input("Digite o tempo de delay:  ")
	Armazena_disciplinas("MW/" + data + "/Disciplinas/", (a,b), erro_disciplinas, existe_disciplinas, falta_disciplinas, t)

	erro_alunos.close()
	erro_professores.close()
	erro_departamentos.close()
	erro_disciplinas.close()

	falta_alunos.close()
	falta_professores.close()
	falta_departamentos.close()
	falta_disciplinas.close()

	existe_alunos.close()
	existe_professores.close()
	existe_departamentos.close()
	existe_disciplinas.close()


'''
i = 157562
disciplinas = (i)
#arquivo = open("MW/" + data + "/Disciplinas/" + str(i) + ".txt", "w")
arquivo = open("saida.txt", "w")
erro = imprime_formatado_com_colunas(disciplinas, arquivo)
arquivo.close()

# 157597 - programacao visual
# 102733 - design de jogos
# 157830 - estudos dirigidos em design 2
# 157562 - materiais e processos graficos
'''
