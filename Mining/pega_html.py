#  -*- coding: utf-8 -*-

# Todos os algoritmos gravam em arquivos e por padrão também armazenam o horário como a primeira linha de cada arquivo
# Caso não seja necessário isso, pode-se retirar a função grava e utilizar a saida normalmente como dados

import datetime
import requests
import random
import time
import os
import re

busca = re.findall

def pega_html(link, limit = 10):
	#pagina_html = mweb(nivel, 'faltavaga_rel', {'cod': disciplina})
	#pagina_html = mweb(nivel, 'faltavaga_rel', {'cod': curso})
	try:
		html = requests.get(link, timeout=limit)
		return html.content
	except:
		print "Nao foi possivel pegar a pagina: " + link
	return ''

def grava(info, nome, tempo = None, separador = '\n'):
	arquivo = open(nome, 'w')
	if tempo == None:
		tempo = datetime.datetime.now()
		tempo = (str(tempo.year), str(tempo.month), str(tempo.day), str(tempo.hour), str(tempo.minute), str(tempo.second))
	arquivo.write(tempo[0])
	for i in xrange(1, 6):
		arquivo.write(' ' + tempo[i])
	arquivo.write(separador)
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
	for i in xrange(len(linhas)):
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
	w = diretorios[0]
	for i in xrange(1, len(diretorios)):
		os.system('if [ ! -d "' + w + '" ]; then mkdir ' + w + '; fi')
		w += "/" + diretorios[i]
	os.system('if [ ! -d "' + w + '" ]; then mkdir ' + w + '; fi')
		



class Nivel:
	GRADUACAO = 'graduacao'
	POS = 'posgraduacao'

class Estado:
	# A maneira que o dado está armazenado
	tratado =  "tratado" + "/"
	html =  "html" + "/"

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

def auxiliar(pagina, origem, destino, processo, delay = 0): # Função auxiliar que é comum a todos
	# PARTE IGUAL
	if processo != 0: # Protecao para a escolha de ja existir dados, mas nao existir
		if processo != 1: # Protecao para a escolha dos dados estiverem tratados
			if not existe_arquivo(destino):
				processo = 1
		if processo == 1:
			if not existe_arquivo(origem):
				processo = 0
	if processo == 0: 						# se precisa capturar dados da internet
		time.sleep(random.uniform(0, 0.5))
		html = pega_html(pagina)
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
		for i in xrange(len(info_util)):
			info_util[i] = info_util[i].split(';')[:-1]
		return tempo, None, info_util
	return tempo, html, None


'''


'''



class Cursos:

	@staticmethod
	def fluxo(habilitacao, nivel = Nivel.GRADUACAO, pasta = "Informacoes/temp/", processo = 2):
	# https://matriculaweb.unb.br/graduacao/fluxo.aspx?cod=3131
		habilitacao 	= str(habilitacao)
		cria_pasta(("Informacoes", "temp", Estado.html, 	nivel, "Cursos"))
		cria_pasta(("Informacoes", "temp", Estado.tratado, 	nivel, "Cursos"))
		pagina 			= 'https://matriculaweb.unb.br/' + nivel + '/fluxo.aspx?cod=' 		+ habilitacao
		origem 			= pasta + Estado.html 			 + nivel + "/Cursos/f_"				+ habilitacao + ".txt"
		destino 		= pasta + Estado.tratado 		 + nivel + "/Cursos/f_" 			+ habilitacao + ".txt"
		tempo, html, info_util = auxiliar(pagina, origem, destino, processo)
		if info_util != None:
			return info_util
		return html

	@staticmethod
	def curriculo(habilitacao, nivel = Nivel.GRADUACAO, pasta = "Informacoes/temp/", processo = -1):
	# https://matriculaweb.unb.br/graduacao/curriculo.aspx?cod=3131
		habilitacao 	= str(habilitacao)
		cria_pasta(("Informacoes", "temp", Estado.html, 	nivel, "Cursos"))
		cria_pasta(("Informacoes", "temp", Estado.tratado, 	nivel, "Cursos"))
		pagina 			= 'https://matriculaweb.unb.br/' + nivel + '/curriculo.aspx?cod=' 	+ habilitacao
		origem 			= pasta + Estado.html 			 + nivel + "/Cursos/c_" 			+ habilitacao + ".txt"
		destino 		= pasta + Estado.tratado 		 + nivel + "/Cursos/c_" 			+ habilitacao + ".txt"
		tempo, html, info_util = auxiliar(pagina, origem, destino, processo)
		if info_util != None:
			return info_util
		return html

	@staticmethod
	def curso(curso, nivel = Nivel.GRADUACAO, pasta = "Informacoes/temp/", processo = -1):
	# https://matriculaweb.unb.br/graduacao/curso_dados.aspx?cod=19
		curso 			= str(curso)
		cria_pasta(("Informacoes", "temp", Estado.html, 	nivel, "Cursos"))
		cria_pasta(("Informacoes", "temp", Estado.tratado, 	nivel, "Cursos"))
		pagina 			= 'https://matriculaweb.unb.br/' + nivel + '/curso_dados.aspx?cod=' + curso
		origem 			= pasta + Estado.html 			 + nivel + "/Cursos/" 				+ curso + ".txt"
		destino 		= pasta + Estado.tratado 		 + nivel + "/Cursos/" 				+ curso + ".txt"
		tempo, html, info_util = auxiliar(pagina, origem, destino, processo)
		if info_util != None:
			return info_util
		return html



	@staticmethod
	def relacao(nivel = Nivel.GRADUACAO, campi = Campus.DARCY, pasta = "Informacoes/temp/", processo = -1):
	# https://matriculaweb.unb.br/graduacao/curso_rel.aspx?cod=1
		campi 			= str(campi)
		cria_pasta(("Informacoes", "temp", Estado.html, 	nivel, "Cursos"))
		cria_pasta(("Informacoes", "temp", Estado.tratado, 	nivel, "Cursos"))
		pagina 			= 'https://matriculaweb.unb.br/' + nivel + '/curso_rel.aspx?cod=' 	+ campi
		origem 			= pasta + Estado.html 			 + nivel + "/Cursos/r_" 			+ campi + ".txt"
		destino 		= pasta + Estado.tratado 		 + nivel + "/Cursos/r_" 			+ campi + ".txt"
		tempo, html, info_util = auxiliar(pagina, origem, destino, processo)
		if info_util != None:
			return info_util
		# Ate esse momento, só esta definido html e tempo. Os outros dados não são uteis
		return html


class Disciplina:
	@staticmethod
	def informacoes(disciplina, nivel = Nivel.GRADUACAO, pasta = "Informacoes/temp/", processo = -1):
		# https://matriculaweb.unb.br/graduacao/disciplina.aspx?cod=116319
		disciplina 		= str(disciplina)
		cria_pasta(("Informacoes", "temp", Estado.html, 	nivel, "Disciplinas"))
		cria_pasta(("Informacoes", "temp", Estado.tratado, 	nivel, "Disciplinas"))
		pagina 			= 'https://matriculaweb.unb.br/' + nivel + '/disciplina.aspx?cod=' 	+ disciplina
		origem 			= pasta + Estado.html 			 + nivel + "/Disciplinas/" 		+ disciplina + ".txt"
		destino			= pasta + Estado.tratado 		 + nivel + "/Disciplinas/" 		+ disciplina + ".txt"
		tempo, html, info_util = auxiliar(pagina, origem, destino, processo)
		if info_util != None:
			return info_util

	


		'''
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
		grava(info_util, pasta + Estado.tratado + nivel + "/Disciplinas/" + disciplina + '.txt', tempo)
		return info_util
		'''
		
class Oferta:

	@staticmethod
	def departamentos(nivel = Nivel.GRADUACAO, campi = Campus.DARCY, pasta = "Informacoes/temp/", processo = -1):
		# a pagina é como:
		# https://matriculaweb.unb.br/graduacao/oferta_dep.aspx?cod=1
		campi			= str(campi)
		cria_pasta(("Informacoes", "temp", Estado.html, 	nivel, "Oferta"))
		cria_pasta(("Informacoes", "temp", Estado.tratado, 	nivel, "Oferta"))
		pagina 			= 'https://matriculaweb.unb.br/' + nivel + '/oferta_dep.aspx?cod=' 	+ campi
		origem 			= pasta + Estado.html 			 + nivel + "/Oferta/" 				+ campi + ".txt"
		destino 		= pasta + Estado.tratado 		 + nivel + "/Oferta/" 				+ campi + '.txt'
		tempo, html, info_util = auxiliar(pagina, origem, destino, processo)
		if info_util != None:
			return info_util
		# Trata os dados de departamentos em um campi

		# Parte 1 em que somente pega a pagina html e transforma em string
		# Neste momento já foi armazenado o html em um arquivo. Aqui começa a tratar os dados para armazenar em
		# pasta + Estado.tratado + nivel + "/Oferta/" + campi + ".txt"
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
			grava(info_util, pasta + Estado.tratado + nivel + "/Oferta/" + campi + '.txt', tempo)
		else:
			grava_erro('Oferta.departamentos:nivel=' + nivel + ";campi=" + campi)
			return [[]] 
		# em info_util ja esta armazenado como info_util[i] = [codigo, sigla, nome]
		return info_util
		
	
	@staticmethod
	def disciplinas(departamento, nivel = Nivel.GRADUACAO, campi = Campus.DARCY, pasta = "Informacoes/temp/", processo = -1):
		# campi nao adianta de nada pois nao interfere no resultado final. Apenas colocado para auxiliar no armazenamento
		# mas é facilmente tirado. A utilizacao é somente para iteracao
		# a pagina é como https://matriculaweb.unb.br/graduacao/oferta_dis.aspx?cod=422
		# departamento sempre será string pois existe o departamento denominado "003" em vez de 3.
		campi 			= str(campi)
		cria_pasta(("Informacoes", "temp", Estado.html, 	nivel, "Oferta"))
		cria_pasta(("Informacoes", "temp", Estado.tratado, 	nivel, "Oferta"))
		pagina 			= 'https://matriculaweb.unb.br/' + nivel + '/oferta_dis.aspx?cod=' 	+ departamento
		origem 			= pasta + Estado.html 			 + nivel + "/Oferta/" 				+ campi + "_" + departamento + ".txt"
		destino 		= pasta + Estado.tratado 		 + nivel + "/Oferta/" 				+ campi + "_" + departamento + ".txt"
		tempo, html, info_util = auxiliar(pagina, origem, destino, processo)
		if info_util != None:
			return info_util
		# Trata os dados das disciplinas de um determinado departamento
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
			grava(info_util, pasta + Estado.tratado + nivel + "/Oferta/" + campi + "_" + departamento + ".txt", tempo)
		else:
			grava_erro('Oferta.disciplinas:nivel=' + nivel + ";dep=" + departamento)
			return [[]]
		return info_util


	@staticmethod
	def turmas(disciplina, departamento, nivel = Nivel.GRADUACAO, pasta = "Informacoes/temp/", processo = -1):
		# a pagina é como:
		# https://matriculaweb.unb.br/graduacao/oferta_dados.aspx?cod=113034
		# se tiver departamento:
		# https://matriculaweb.unb.br/graduacao/oferta_dados.aspx?cod=200212&dep=004
		# assume-se que departamento já é string


		CABECALHO = "Departamento.*?cod=.*?>(.*?) <small> (.*?)</small></a></td>"\
						+ ".*?" \
						+ "da Disciplina</th><td>(.*?)</td></tr>" \
						+ ".*?" \
						+ "Nome</th><td><a title=.*?>(.*?) <i class=" \
						+ ".*?" \
						+ "\(Teor-Prat-Ext-Est\)</small></th><td>(\d+)-(\d+)-(\d+)-(\d+)" \
						+ ".*?" \
						+ "<h4>Campus (.*?)</h4>"
		TURMA 		= "<td class='turma'>(.*?)</td></tr>" \
						+ ".*?" \
						+ "<td>Vagas</td><td><span>(\d+)</span></td></tr>" \
						+ ".*?" \
						+ "<td>Ocupadas</td><td><span style=.*?>(\d+)</span></td></tr>" \
						+ ".*?" \
						+ "<td>Restantes</td><td><span style=.*?>(\d+)</span></td></tr>"



		disciplina 		= str(disciplina)
		cria_pasta(("Informacoes", "temp", Estado.html, 	nivel, "Oferta", "turmas"))
		cria_pasta(("Informacoes", "temp", Estado.tratado, 	nivel, "Oferta", "turmas"))
		pagina 			= 'https://matriculaweb.unb.br/' + nivel + '/oferta_dados.aspx?cod='+ disciplina 	+ '&dep=' 	+ departamento
		origem 			= pasta + Estado.html 			 + nivel + "/Oferta/turmas/" 		+ departamento 	+ "_" 		+ disciplina + ".txt"
		destino 		= pasta + Estado.tratado 		 + nivel + "/Oferta/turmas/" 		+ departamento 	+ "_" 		+ disciplina + ".txt"
		tempo, html, info_util = auxiliar(pagina, origem, destino, processo)
		if info_util != None:
			return info_util
		# Trata os dados das turmas
		contador = 0
		while( contador < len(html)):
			if "Departamento" in html[contador]:
				break
			contador += 1
		if contador < len(html):
			info_util = html[contador]
			info_util = info_util.split("<div class='table-responsive' style=")
			info_util[0] = busca(CABECALHO, info_util[0])
			info_util[0] = info_util[0][0]
			print info_util[0]
			#info_util.remove(info_util[-1])
			#for i in xrange(1,len(info_util)-1):
			#	pass
			#quantidade = info_util.count("Turno")
			#info_util = busca(TURMAS, info_util)
			#if(len(info_util) == quantidade):
				#print info_util
			#	pass
			#else:
			#	print "Deu erro com " + disciplina + " de " + departamento


			grava(info_util, pasta + Estado.tratado + nivel + "/Oferta/turmas/" + departamento + "_" + disciplina + ".txt", tempo)
		else:
			info_util = []
			print disciplina + " - " + departamento

		return info_util


	@staticmethod
	def espera(disciplina, nivel = Nivel.GRADUACAO, pasta = "Informacoes/temp/", processo = -1): # Incompleto
	# a pagina é como:
	# https://matriculaweb.unb.br/graduacao/faltavaga_rel.aspx?cod=116319
		disciplina 		= str(disciplina)
		cria_pasta(("Informacoes", "temp", Estado.html, 	nivel, "Oferta", "espera"))
		cria_pasta(("Informacoes", "temp", Estado.tratado, 	nivel, "Oferta", "espera"))
		pagina 			= 'https://matriculaweb.unb.br/' + nivel + '/faltavaga_rel.aspx?cod=' + disciplina
		origem 			= pasta + Estado.html 			 + nivel + "/Oferta/espera/" 		  + disciplina + ".txt"
		destino 		= pasta + Estado.tratado 		 + nivel + "/Oferta/espera/" 		  + disciplina + ".txt"
		tempo, html, info_util = auxiliar(pagina, origem, destino, processo, random.uniform(0, 0.5))
		if info_util != None:
			return info_util



		# Trata os dados de espera
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
			grava(info_util, pasta + Estado.tratado + nivel + "/Oferta/espera/" + disciplina + ".txt", tempo)
			contador += 1
		else:
			grava_erro('Oferta.espera:nivel=' + nivel + ";disc=" + disciplina)
			return [[]]
		return info_util
		# '''