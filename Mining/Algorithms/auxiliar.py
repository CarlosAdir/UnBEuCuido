#  -*- coding: utf-8 -*-

# Todos os algoritmos gravam em arquivos e por padrão também armazenam o horário como a primeira linha de cada arquivo
# Caso não seja necessário isso, pode-se retirar a função grava e utilizar a saida normalmente como dados

import requests
import datetime
import random
import time
import re
import os

def get_time(tempo):
	if tempo == None:
		tempo = datetime.datetime.now()
		tempo = (str(tempo.year), str(tempo.month), str(tempo.day), str(tempo.hour), str(tempo.minute), str(tempo.second))
	return tempo
def grava_time(arquivo, tempo, separador = '\n'):
	arquivo.write(tempo[0])
	for i in range(1, 6):
		arquivo.write(' ' + tempo[i])
	arquivo.write(separador)


def grava(info, nome, tempo = None, separador = '\n'):
	arquivo = open(nome, 'w')
	tempo = get_time(tempo)
	grava_time(arquivo, tempo, separador)
	if type(info) == list or type(info) == type(()):
		for elemento in info:
			if type(elemento) == list or type(info) == type(()):
				for m in elemento:
					arquivo.write(str(m) + ';')
				arquivo.write(separador)
			else:
				arquivo.write(str(elemento) + separador)
	else:

		arquivo.write(info)
	arquivo.close()
	return tempo

def existe_arquivo(nome):
	try:
		arquivo = open(nome, "r")
		arquivo.close()
		return True
	except:
		pass
	return False

def le_arquivo(nome):
	arquivo = open(nome, "r")
	linhas = arquivo.readlines()
	arquivo.close()
	for i in range(len(linhas)):
		linhas[i] = linhas[i].split('\n')[0]
		if '\r' in linhas[i]:
			linhas[i] = linhas[i].split('\r')[0]
	return linhas

def grava_erro(erro, separador = '\n'):
	arq = open("erros.txt", "a")
	arq.write(erro + separador)
	arq.close()

def cria_pasta(diretorios):
	#os.system('if [ ! -d "' + diretorio + '" ]; then echo "doing ' + diretorio + '"; mkdir ' + diretorio + '; fi')
	if(type(diretorios) == str):
		os.system('if [ ! -d "' + diretorios + '" ]; then mkdir ' + diretorios + '; fi')
	else:
		w = diretorios[0]
		os.system('if [ ! -d "' + w + '" ]; then mkdir ' + w + '; fi')
		for i in range(1, len(diretorios)):
			w += "/" + diretorios[i]
			os.system('if [ ! -d "' + w + '" ]; then mkdir ' + w + '; fi')

#busca = re.findall

def pega_html(link, limit = 10):
	#pagina_html = mweb(nivel, 'faltavaga_rel', {'cod': disciplina})
	#pagina_html = mweb(nivel, 'faltavaga_rel', {'cod': curso})
	try:
		html = requests.get(link, timeout=limit)
		#return html.content
		return html.text
	except:
		print("Nao foi possivel pegar a pagina: " + link)
	return ''

def define_processo(processo, origem, destino):
	if processo != 0: # Protecao para a escolha de ja existir dados, mas nao existir
		if processo != 1: # Protecao para a escolha dos dados estiverem tratados
			if not existe_arquivo(destino):
				processo = 1
		if processo == 1:
			if not existe_arquivo(origem):
				processo = 0
	return processo

def common(pagina, origem, destino, processo, delay = 0): # Função auxiliar que é comum a todos
	# PARTE IGUAL
	processo = define_processo(processo, origem, destino)
	if processo == 0: 						# se precisa capturar dados da internet
		time.sleep(random.uniform(0, 0.5))
		html = str(pega_html(pagina))
		if html == '':
			return None, None, None
		tempo = grava(html, origem)
		html = html.split('\n')
	elif processo == 1:						# Se ja existe o dado bruno no computador
		html = le_arquivo(origem)
		tempo = html[0].split()
		html.remove(html[0])
	else:									# Se ja existem e os dados estao tratados
		info_util = le_arquivo(destino)
		tempo = info_util[0].split()
		info_util.remove(info_util[0])
		for i in range(len(info_util)):
			info_util[i] = info_util[i].split(';')[:-1]
		return tempo, None, info_util
	return tempo, html, None