#  -*- coding: utf-8 -*-

# Todos os algoritmos gravam em arquivos e por padrão também armazenam o horário como a primeira linha de cada arquivo
# Caso não seja necessário isso, pode-se retirar a função grava e utilizar a saida normalmente como dados

import datetime
import requests

def pega_html(link_pagina, timeout = 10):
	#pagina_html = mweb(nivel, 'faltavaga_rel', {'cod': disciplina})
	#pagina_html = mweb(nivel, 'faltavaga_rel', {'cod': curso})
	try:
		html = requests.get(link_pagina, timeout=timeout)
		return html.content
	except:
		print "Nao foi possivel pegar a pagina: " + link_pagina
	return ''

def grava(info, nome, time = None, separador = '\n'):
	arquivo = open(nome, 'w')
	if time == None:
		time = datetime.datetime.now()
		time = (str(time.year), str(time.month), str(time.day), str(time.hour), str(time.minute), str(time.second))
	arquivo.write(time[0] + ' ' + time[1] + ' ' + time[2] + ' ' + time[3] + ' ' + time[4] + ' ' + time[5] + separador)
	if type(info) == list:
		for elemento in info:
			if type(elemento) == list:
				for m in elemento:
					arquivo.write(str(m) + ';')
				arquivo.write(separador)
			else:
				arquivo.write(str(elemento) + separador)
	else:
		arquivo.write(info)
	arquivo.close()
	return time

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
	for i in xrange(len(linhas)):
		linhas[i] = linhas[i].split('\n')[0]
		if '\r' in linhas[i]:
			linhas[i] = linhas[i].split('\r')[0]
	return linhas


class Nivel:
	GRADUACAO = 'graduacao'
	POS = 'posgraduacao'

class Campus:
	DARCY = 1
	PLANALTINA = 2
	CEILANDIA = 3
	GAMA = 4

class Departamento:
    '''Enumeração dos códigos de cada departamento.'''
    CIC = 116
    ENE = 163
    ENM = 164
    EST = 115
    GAMA = 650
    IFD = 550  # Instituto de Física
    MAT = 113

class Habilitacoes:
    '''Enumeração das habilitações de cada curso.'''
    BCC = 1856  # Ciência da Computação
    LIC = 1899  # Computação
    ENC = 1741  # Engenharia de Computação
    MECA = 6912  # Engenharia de Controle e Automação
    ENM = 6424 # Engenharia Mecânica


class Cursos:

	@staticmethod
	def fluxo(habilitacao, nivel = Nivel.GRADUACAO):
	# https://matriculaweb.unb.br/graduacao/fluxo.aspx?cod=3131
		pagina = 'https://matriculaweb.unb.br/' + nivel + '/fluxo.aspx?cod=' + habilitacao
		return pega_html(pagina)

	def curriculo(habilitacao, nivel = Nivel.GRADUACAO):
	# https://matriculaweb.unb.br/graduacao/curriculo.aspx?cod=3131
		pagina = 'https://matriculaweb.unb.br/' + nivel + '/curriculo.aspx?cod=' + habilitacao
		return pega_html(pagina)

	@staticmethod
	def curso(curso, nivel = Nivel.GRADUACAO):
	# https://matriculaweb.unb.br/graduacao/curso_dados.aspx?cod=19
		pagina = 'https://matriculaweb.unb.br/' + nivel + '/curso_dados.aspx?cod=' + curso
		return pega_html(pagina)

	@staticmethod
	def relacoes(nivel = Nivel.GRADUACAO, campus = Campus.DARCY):
	# https://matriculaweb.unb.br/graduacao/curso_rel.aspx?cod=1
		pagina = 'https://matriculaweb.unb.br/' + nivel + '/curso_rel.aspx?cod=' + campus
		return pega_html(pagina)


class Disciplina:
	@staticmethod
	def informacoes(disciplina, nivel = Nivel.GRADUACAO, pasta = "Informacoes/temp/", processo = -1):
		# https://matriculaweb.unb.br/graduacao/disciplina.aspx?cod=116319
		disciplina = str(disciplina)
		if processo == -1:
			if existe_arquivo(pasta + 'tratado/' + nivel + "/Oferta/espera/" + disciplina + ".txt"): 	# Os dados existem e estao processados
				processo = 2
			elif existe_arquivo(pasta + 'html/' + nivel + "/Oferta/espera/" + disciplina + ".txt"): 	# Os dados existem mas nao processados
				processo = 1
			else: 																						# Os dados existem
				processo = 0
		if processo == 0:
			pagina = 'https://matriculaweb.unb.br/' + nivel + '/disciplina.aspx?cod=' + disciplina
			html = pega_html(pagina)
			time = grava(html, pasta + 'html/' + nivel + "/Disciplinas/" + disciplina + ".txt")
			html = html.split('\n')
			processo += 2
		elif processo == 1:
			html = le_arquivo(pasta + 'html/' + nivel + "/Disciplinas/" + disciplina + ".txt")
			time = html[0].split()
			html.remove(html[0])
			processo += 1
		else:
			info_util = le_arquivo(pasta + "tratado/" + nivel + "/Disciplinas/" + disciplina + ".txt")
			time = info_util[0].split()
			info_util.remove(info_util[0])
			for i in xrange(len(info_util)):
				info_util[i] = info_util[i].split(';')[:-1]
			return info_util

		
		# Para tratar os dados
		contador = [0];
		while contador[0] < len(html) and (not "VER OFERTA" in html[contador[0]]):
			contador[0] += 1
		if contador[0] == len(html):
			print "Deu erro com a disciplina " + disciplina + "em achar 'VER OFERTA'"
			return []
		contador.append(contador[0]+1)
		while (contador[1] < len(html)) and (not "Denominação" in html[contador[1]]): # Verifica se nao é vazio
			contador[1] += 1
		while (contador[1] < len(html)) and (not "</div>" in html[contador[1]]):
			contador[1] += 1
		if contador[1] == len(html):
			return []
		info_util = html[contador[0]+1 : contador[1]]
		#if len(info_util) != 1: teste para ver se achava mais de uma linha no meio do processo, devido a bibliografia
		#	print info_util
		#info_util = info_util[0]
		
		#info_util = info_util.split("col-xs-11'>")[1]
		#info_util = info_util.split("</td></tr><tr><th>Código</th><td>")
		#info_util[1] = info_util[1].split("</td></tr><tr><th>Denominação</th><td>")
		#info_util.append(info_util[1][1])
		#info_util[1] = info_util[1][0]
		#info_util[2] = info_util[2].split("</td></tr><tr><th>Nível</th><td>")
		#info_util.append(info_util[2][1])
		#info_util[2] = info_util[2][0]
		#info_util[3] = info_util[3].split("</td></tr><tr><th>Vigência</th><td>")
		#info_util.append(info_util[3][1])
		#info_util[3] = info_util[3][0]
		print info_util
		print '\n\n'
		grava(info_util, pasta + 'tratado/' + nivel + "/Disciplinas/" + disciplina + '.txt', time)
		return info_util
		
class Oferta:

	@staticmethod
	def departamentos(nivel = Nivel.GRADUACAO, campi = Campus.DARCY, pasta = "Informacoes/temp/", processo = -1):
		# processo so recebe 0 ou 1 ou 3 como argumento
		# a pagina é como:
		# https://matriculaweb.unb.br/graduacao/oferta_dep.aspx?cod=1
		if processo == -1:
			if existe_arquivo(pasta + 'tratado/' + nivel + "/Oferta/" + str(campi) + ".txt"): 	# Os dados existem e estao processados
				processo = 2
			elif existe_arquivo(pasta + 'html/' + nivel + "/Oferta/" + str(campi) + ".txt"): 	# Os dados existem mas nao processados
				processo = 1
			else: 																						# Os dados nao existem
				processo = 0
		if processo == 0:
			# pega da web e armazena, pois processo 0 indica que é desde o inicio
			# Ou seja, a captura de dados pela internet e depois grava em um arquivo o html lido
			pagina = 'https://matriculaweb.unb.br/' + nivel + '/oferta_dep.aspx?cod=' + str(campi)
			html = pega_html(pagina)
			time = grava(html, pasta + 'html/' + nivel + "/Oferta/" + str(campi) + ".txt")
			html = html.split('\n')
			processo += 2
		elif processo == 1:
			# pega já do arquivo existente para tratar caso necessario, so entra nesse caso se existir o arquivo
			# Simplesmente pega os dados do arquivo, não é necessário entrar nesse campo se for processo 0
			html = le_arquivo(pasta + 'html/' + nivel + "/Oferta/" + str(campi) + ".txt")
			time = html[0].split()
			html.remove(html[0])
			processo += 1
		else:
			# vem para esse caso já que está tratado
			info_util = le_arquivo(pasta + 'tratado/' + nivel + "/Oferta/" + str(campi) + '.txt')
			time = info_util[0].split()
			info_util.remove(info_util[0])
			for i in xrange(len(info_util)):
				info_util[i] = info_util[i].split(';')[:-1]
			return info_util
		# Parte 1 em que somente pega a pagina html e transforma em string
		# Neste momento já foi armazenado o html em um arquivo. Aqui começa a tratar os dados para armazenar em
		# pasta + 'tratado/' + nivel + "/Oferta/" + str(campi) + ".txt"
		# tratar uma lista de departamentos
		# indica para tratar os dados armazenados
		contador = 0
		while contador < len(html):
			if 'departamentos existentes' in html[contador]:
				break
			if 'departamento existente' in html[contador]:
				break
			contador += 1
		if contador < len(html):
			info_util = html[contador]
			info_util = info_util.split('<tbody>')[1]
			info_util = info_util.split('</tbody>')[0]
			info_util = info_util.split("<tr><td>")[1:] # gambiarra para dar certo pois a primeira linha sempre era vazia
			for i in xrange(len(info_util)):
				info_util[i] = info_util[i].split('</td><td>')
				info_util[i][2] = info_util[i][2].split("' style='text-transform: uppercase;'>")[1]
				info_util[i][2] = info_util[i][2].split("</a></td></tr>")[0]
			grava(info_util, pasta + 'tratado/' + nivel + "/Oferta/" + str(campi) + '.txt', time)
		else:
			print 'Erro com: ' + nivel + " + campi:" + campi
			return [[]] 
		# em info_util ja esta armazenado como info_util[i] = [codigo, sigla, nome]
		return info_util

	
	@staticmethod
	def disciplinas(departamento, nivel = Nivel.GRADUACAO, campi = Campus.DARCY, pasta = "Informacoes/temp/", processo = -1):
		# campi nao adianta de nada pois nao interfere no resultado final. Apenas colocado para auxiliar no armazenamento
		# mas é facilmente tirado. A utilizacao é somente para iteracao
		# a pagina é como https://matriculaweb.unb.br/graduacao/oferta_dis.aspx?cod=422
		if processo == -1:
			if existe_arquivo(pasta + 'tratado/' + nivel + "/Oferta/" + str(campi) + "_" + departamento + ".txt"): 	# Os dados existem e estao processados
				processo = 2
			elif existe_arquivo(pasta + 'html/' + nivel + "/Oferta/" + str(campi) + "_" + departamento + ".txt"): 	# Os dados existem mas nao processados
				processo = 1
			else: 																						# Os dados nao existem
				processo = 0
		if processo == 0:
			# caso precise baixar tudo da internet
			pagina = 'https://matriculaweb.unb.br/' + nivel + '/oferta_dis.aspx?cod=' + str(departamento)
			html = pega_html(pagina)
			time = grava(html, pasta + 'html/' + nivel + "/Oferta/" + str(campi) + "_" + departamento + ".txt")
			html = html.split('\n')
		elif processo == 1:
			# caso ja tenha armazenado
			html = le_arquivo(pasta + 'html/' + nivel + "/Oferta/" + str(campi) + "_" + departamento + ".txt")
			time = html[0].split()
			html.remove(html[0])
		else:
			# le o documento tratado
			info_util = le_arquivo(pasta + 'tratado/' + nivel + "/Oferta/" + str(campi) + "_" + departamento + ".txt")
			time = info_util[0].split()
			info_util.remove(info_util[0])
			for i in xrange(len(info_util)):
				info_util[i] = info_util[i].split(';')[:-1]
			return info_util
		# Agora que ja tem os dados armazenados na memoria RAM, no caso todo o arquivo html em que cada
		# linha é um elemento da lista na ordem dada por arquivo. lista[0] = primeira linha e assim por diante
		contador = 0
		while contador < len(html) :
			if 'disciplinas existentes' in html[contador]:
				break
			if 'disciplina existente' in html[contador]:
				break
			contador += 1
		if contador < len(html):
			info_util = html[contador]
			info_util = info_util.split("</th></tr>")[1]
			info_util = info_util.split("</table>")[0]
			info_util = info_util.split("</td></tr>")
			info_util.remove(info_util[len(info_util)-1]) # gambiarra pois o ultimo termo sempre é vazio
			for i in xrange(len(info_util)):
				info_util[i] = info_util[i].split('<tr><td>')[1]
				info_util[i] = info_util[i].split("<a title='")
				info_util[i][0] = info_util[i][0].split("</td><td><a href=")[0]
				info_util[i][1] = info_util[i][1].split("' href='")[0]
			grava(info_util, pasta + 'tratado/' + nivel + "/Oferta/" + str(campi) + "_" + departamento + ".txt", time)
		else:
			print 'Erro com: ' + nivel + " + dep:" + departamento
			return [[]]
		return info_util



	@staticmethod
	def turmas(disciplina, departamento, nivel = Nivel.GRADUACAO, pasta = "Informacoes/temp/", processo = -1):
		# a pagina é como:
		# https://matriculaweb.unb.br/graduacao/oferta_dados.aspx?cod=113034
		# se tiver departamento:
		# https://matriculaweb.unb.br/graduacao/oferta_dados.aspx?cod=200212&dep=004
		# assume-se que departamento já é string
		if processo == -1:
			if existe_arquivo(pasta + 'tratado/' + nivel + "/Oferta/disciplinas/" + str(departamento) + "_" + disciplina + ".txt"): 	# Os dados existem e estao processados
				processo = 2
			elif existe_arquivo(pasta + 'html/' + nivel + "/Oferta/disciplinas/" + str(departamento) + "_" + disciplina + ".txt"): 	# Os dados existem mas nao processados
				processo = 1
			else: 																						# Os dados existem
				processo = 0
		if processo == 0:
			disciplina = str(disciplina)
			pagina = 'https://matriculaweb.unb.br/' + nivel + '/oferta_dados.aspx?cod=' + disciplina + '&dep=' + departamento
			html = pega_html(pagina)
			time = grava(html, pasta + 'html/' + nivel + "/Oferta/disciplinas/" + str(departamento) + "_" + disciplina + ".txt")
			html = html.split('\n')
		elif processo == 1:
			html = le_arquivo(pasta + 'html/' + nivel + "/Oferta/disciplinas/" + str(departamento) + "_" + disciplina + ".txt")
			time = html[0].split()
			html.remove(html[0])
		else:
			info_util = le_arquivo(pasta + 'tratado/' + nivel + "/Oferta/disciplinas/" + str(departamento) + "_" + disciplina + ".txt")
			time = info_util[0].split()
			info_util.remove(info_util[0])
			for i in xrange(len(info_util)):
				info_util[i] = info_util[i].split(';')[:-1]
			return info_util

		contador = 0
		while( contador < len(html)):
			if "Departamento" in html[contador]:
				break
			contador += 1
		if contador < len(html):
			info_util = html[contador]
			grava(info_util, pasta + 'tratado/' + nivel + "/Oferta/disciplinas/" + str(departamento) + "_" + disciplina + ".txt", time)
		else:
			info_util = [[]]
			print str(disciplina) + " - " + str(departamento) 

		return info_util
	


	@staticmethod
	def espera(disciplina, nivel = Nivel.GRADUACAO, pasta = "Informacoes/temp/", processo = -1): # Incompleto
	# a pagina é como:
	# https://matriculaweb.unb.br/graduacao/faltavaga_rel.aspx?cod=116319
		disciplina = str(disciplina)
		if processo == -1:
			if existe_arquivo(pasta + 'tratado/' + nivel + "/Oferta/espera/" + disciplina + ".txt"): 	# Os dados existem e estao processados
				processo = 2
			elif existe_arquivo(pasta + 'html/' + nivel + "/Oferta/espera/" + disciplina + ".txt"): 	# Os dados existem mas nao processados
				processo = 1
			else: 																						# Os dados existem
				processo = 0
		if processo == 0:
			pagina = 'https://matriculaweb.unb.br/' + nivel + '/faltavaga_rel.aspx?cod=' + disciplina
			html = pega_html(pagina)
			time = grava(html, pasta + 'html/' + nivel + "/Oferta/espera/" + disciplina + ".txt")
			html = html.split('\n')
		elif processo == 1:
			html = le_arquivo(pasta + 'html/' + nivel + "/Oferta/espera/" + disciplina + ".txt")
			time = html[0].split()
			html.remove(html[0])
		else:
			info_util = le_arquivo(pasta + 'tratado/' + nivel + "/Oferta/espera/" + disciplina + ".txt")
			time = info_util[0].split()
			info_util.remove(info_util[0])
			for i in xrange(len(info_util)):
				info_util[i] = info_util[i].split(';')[:-1]
			return info_util
		info_util = html
		
		contador = 0
		while contador < len(html) :
			if 'alunos existentes' in html[contador]:
				break
			if 'aluno existente' in html[contador]:
				break
			contador += 1
		if contador < len(html):
			info_util = html[contador]
			info_util = info_util.split("_search'>")[1]
			#info_util = info_util.split("</span><div><table")
			info_util = info_util.split("</td></tr></tr></table></div><div id=")
			info_anterior = info_util[0]
			info_util = info_util[1].split("Desistente</th></tr>")
			turmas = info_util[0]
			info_util = info_util[1].split("</tr></table></div>")[0]
			info_util = info_util.split("<tr><td>")[1:] # gambiarra pois o primeiro elemento é nulo
			for i in xrange(len(info_util)):
				info_util[i] = info_util[i].split("</td><td>")
				for j in xrange(len(info_util[i])):
					if " <small>" in info_util[i][j]:
						info_util[i][j] = info_util[i][j].replace(" <small>","-")
						info_util[i][j] = info_util[i][j].replace(" </small>","")
					elif "</td></tr>" in info_util[i][j]:
						info_util[i][j] = info_util[i][j].replace("</td></tr>","")
			grava(info_util, pasta + 'tratado/' + nivel + "/Oferta/espera/" + disciplina + ".txt", time)
		else:
			#print 'Erro com: ' + nivel + " + disc:" + disciplina + ""
			return [[]]
		return info_util


