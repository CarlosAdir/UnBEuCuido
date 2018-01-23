#  -*- coding: utf-8 -*-
'''
	Todas as funcoes aqui presentes recebem o html na forma bruta e entao, dependendo da pagina,
	sera retornado determinada informacoes
	Sao no total 9 tipos de paginas diferentes:
	1) https://matriculaweb.unb.br/graduacao/oferta_dep.aspx?cod=1
		Esta é a pagina que contem a lista d e todos os departamentos que estão oferecendo disciplina
		Essa pagina é a oferta do Darcy Ribeiro
	2) https://matriculaweb.unb.br/graduacao/oferta_dis.aspx?cod=113
		Essa é a pagina de oferta de disciplinas de um determinado departamento. O departamento escolhido
		foi o departamento de matematica. Atencao que o codigo pode ser do modo "003", sem aspas
	3) https://matriculaweb.unb.br/graduacao/oferta_dados.aspx?cod=113093&dep=113
		Essa é a pagina que contém a lista de turmas para uma determinada disciplina(no caso 113093) e um
		determinado departamento(no caso 113). Existe também a possibilidade do link:
		https://matriculaweb.unb.br/graduacao/oferta_dados.aspx?cod=113093
		contudo, com essa opção, é possivel que oferte as turmas de outro departamento.
		Essa disciplina por exemplo é a 113093(Introdução à algebra linear) do departamento 113(Matematica)
		Caso deixe sem o "&dep=113", é possível que apareçam as disciplinas do gamma que é do departamento FGA.
		Desta pagina é possivel obter a informação se existe ou não espera.
	4) https://matriculaweb.unb.br/graduacao/disciplina.aspx?cod=113093
		Essa é a pagina que mostra a ementa de uma determinada disciplina.
		No caso, é a ementa da disciplina de 113093(Introducao à algebra linear).
		Vale a pena dizer que essa disciplina não depende do departamento.
	5) https://matriculaweb.unb.br/graduacao/faltavaga_rel.aspx?cod=116319 
		Essa é a pagina que mostra a lista de espera de uma determinada disciplina.
		Frequentemente aparece quando está no periodo de ajuste após a matricula dos alunos
	6) https://matriculaweb.unb.br/graduacao/curso_rel.aspx?cod=1
		Essa pagina é a que mostra a lista de cursos de algum campus. No caso é o campus Darcy Ribeiro
	7) https://matriculaweb.unb.br/graduacao/curso_dados.aspx?cod=370
		Essa é a pagina que mostra a lista de habilitacoes de um determinado curso.
		No caso foi escolhido o curso 370(de Ciência da Computação), que só possui uma habilitação.
		Contudo, há casos em que há mmais de uma habilitação, como é no caso de 213(Ciências Sociais),
		em que possui 4 habilitações possiveis: Antropologia, Ciências Sociais, Ciências Sociais, Sociologia
		https://matriculaweb.unb.br/graduacao/curso_dados.aspx?cod=213
	8) https://matriculaweb.unb.br/graduacao/fluxo.aspx?cod=3123
		Essa é a pagina que mostra o fluxo de uma determinada habilitação.
		No caso escolhido foi a habilitação 3123(Sociologia, do curso Ciencias Sociais).
	9) https://matriculaweb.unb.br/graduacao/curriculo.aspx?cod=3123
		Essa é a pagina que mostra o curriculo de uma determinada habilitacao.
		No caso escolhido foi a habilitacao 3123(Sociologia, do curso Ciencias Sociais).

	Temos aqui 9 tipos diferentes de paginas. As funcoes nesse arquivo python sao referentes a essas paginas,
	respectivamente. 
	Como a unica diferença entre os graduacao e os da pós é um prefixo, entao sao tratados apenas 9 paginas 
	em vez de 18 no total.
'''
import defines # Arquivo que contem os nomes e numeros de alguns departamentos, facilmente mutavel
import re

busca = re.findall

# Para as transformacoes, colocaremos html como apenas uma string

def trans_1(html):
	if not '<div class="card">' in html:
		return False, []
	retorno = []
	html = html.split('<span class="badge">')[1]
	html = html.split('<!-- /Top Bar -->')
	retorno.append(html[0])
	retorno[0] = retorno[0].split('</span>')[0]
	html = html[1]
	html = html.split('<div class="card">')[1]
	html = html.split('<!-- /page content -->')[0]
	html = html.split('<div class="body table-responsive">')
	retorno.append(html[0])
	html = html[1]
	html = html.split("<span id='result_label' class='badge'")[1]
	retorno[1] = retorno[1].split('<h2>')[1].split('</h2>')[0].split('  ')
	for i in range(len(retorno[1])):
		if(len(retorno[1][i]) > 4):
			retorno[1] = retorno[1][i]
			break
	# Aqui comeca a separar 
	info_util = html
	info_util = info_util.split('<tbody>')[1]
	info_util = info_util.split('</tbody>')[0]
	info_util = info_util.split("<tr><td>")[1:] # gambiarra para dar certo pois a primeira linha sempre era vazia
	for i in range(len(info_util)):
		info_util[i] = info_util[i].split('</td><td>')
		info_util[i][2] = info_util[i][2].split("' style='text-transform: uppercase;'>")[1]
		info_util[i][2] = info_util[i][2].split("</a></td></tr>")[0]
	retorno.append(info_util)
	
	'''
	for i in retorno:
		if type(i) == str:
			print(i)
		else:
			for j in i:
				print(j)
	'''
	# Ate esse momento, html possui somente os codigos, siglas e denominacoes, sem textos
	return True, retorno
def trans_2(html):
	if not '<div class="card">' in html:
		return False, []
	retorno = []
	html = html.split('<span class="badge">')[1]
	html = html.split('<!-- /Top Bar -->')
	retorno.append(html[0])
	retorno[0] = retorno[0].split('</span>')[0]
	html = html[1].split('<div class="card">')[2]
	html = html.split('<!-- /page content -->')[0]
	html = html.split('<div class="body table-responsive">')
	retorno.append(html[0])
	retorno[1] = retorno[1].split('<h2>')[1].split('</h2>')[0]
	html = html[1]

	info_util = html
	info_util = info_util.split("</th></tr>")[1]
	info_util = info_util.split("</table>")[0]
	info_util = info_util.split("</td></tr>")
	info_util.remove(info_util[len(info_util)-1]) # gambiarra pois o ultimo termo sempre é vazio
	for i in range(len(info_util)):
		info_util[i] = info_util[i].split('<tr><td>')[1]
		info_util[i] = info_util[i].split("<a title='")
		info_util[i][0] = info_util[i][0].split("</td><td><a href=")[0]
		info_util[i][1] = info_util[i][1].split("' href='")[0]
	html = info_util
	retorno.append(html)
	
	'''
	for i in retorno:
		if type(i) == str:
			print(i)
		else:
			for j in i:
				print(j)
	'''
	
	return True, retorno
def trans_3(html):
	if not '<div class="card">' in html:
		return False, []
	retorno = []

	
	html = html.split('<span class="badge">')[1]
	html = html.split('<!-- /Top Bar -->')
	retorno.append(html[0])
	retorno[0] = retorno[0].split('</span>')[0]
	print(retorno)
	#html = html[1].split('<div class="card">')[1]
	html = html[1].split('<!-- /menu lateral -->')[1]
	html = html.split('<!-- /page content -->')[0]
	
	CABECALHO 	= 	'<div class="header">.*?<h2>.*?(.*?)<small>(.*?)</small>'\
					+ ".*?"\
					+ "Departamento.*?cod=.*?>(.*?) <small> (.*?)</small></a></td>"\
					+ ".*?" \
					+ "da Disciplina</th><td>(.*?)</td></tr>" \
					+ ".*?" \
					+ "Nome</th><td><a title=.*?>(.*?) <i class=" \
					+ ".*?" \
					+ "\(Teor-Prat-Ext-Est\)</small></th><td>(\d+)-(\d+)-(\d+)-(\d+)" 

	cabecalho 	= list(busca(CABECALHO, html)[0])
	cabecalho[0] = cabecalho[0].split('  ')[-1]
	#print(cabecalho)

	retorno.append(cabecalho)

	if("atendidos por falta de vagas" in html):
		retorno.append({"espera": True})
	else:
		retorno.append({"espera": False})
	
	NOME_TURMA	= "<td class='turma'>(.*?)</td></tr>"
	TURMA 		= "Vagas</td><td><span>(\d+)</span>"\
					+ ".*?" \
					+ "Ocupadas</td><td><span style='color:.*?'>(\d+)</span>" \
					+ ".*?" \
					+ "Restantes</td><td><span style='color:.*?'>(\d+)</span>"



	html = html.split("Campus")[1:]
	for i in range(len(html)):
		html[i] = html[i].split("<tr><th class='col-lg-1 col-sm-1 col-xs-1'>")

	campus = {}
	for i in range(len(html)):
		print('han')
		turmas = {}
		for j in range(1, len(html[i])):
			nome_turma 	= busca(NOME_TURMA, html[i][j])[0]
			print(nome_turma)
			turma 		= busca(TURMA, html[i][j])
			#turma = '       '
			#print(turma)
			#print(nome_turma[0])
			#print(turma)
			#print(len(turma))
			turmas[nome_turma] = {}
			#print(turma[0])
			#turmas[nome_turma]["Total"] = "ka"
			#print(turmas[nome_turma]["Total"])
			print(turma)
			for i in range(len(turma)):
				print(turma[i])
			#	
			#	if i == 0:
			#		turmas[nome_turma]["Total"] = turma[i]
			#	elif i == 1:
			#		turmas[nome_turma]["Calouros"] = turma[i]
		#for i in turmas:
		#	print(i + ":" + str(turmas[i]))
		#print(turmas)



	
			

	
	#turma = busca(TURMA, html)
	#print(turma)

	#'.*?' \
	#'<td>Ocupadas</td>' \
	#'<td><b><font color=(?:red|green)>(\d+)</font></b></td>' \
	#'(.*?)' \
	#'<center>(.*?)(?:|<br>)</center>' \
	#'.*?' \
	#'(Reserva para curso(.*?))?' \
	#'<tr><td colspan=6 bgcolor=white height=20></td></tr>'
	HORARIO 	= '<b>((?:Segunda|Terça|Quarta|Quinta|Sexta|Sábado|Domingo))' \
					+ '</b>.*?' \
					+ '<font size=1 color=black><b>(.*?)</font>.*?' \
					+ '<font size=1 color=brown>(.*?)</b></font><br><i>' \
					+ '<img src=/imagens/subseta_dir.gif align=top> (.*?)</i>'

	RESERVA 	= '<td align=left>(.*?)</td>' \
				+ '<td align=center>(\d+)</td>' \
				+ '<td align=center>(\d+)</td>'


    
	#print(html)
	'''
	retorno.append(html[0])
	retorno[1] = retorno[1].split('<h2>')[1].split('</h2>')[0].split('  ')
	for i in range(len(retorno[1])):
		if(len(retorno[1][i]) > 4):
			retorno[1] = retorno[1][i]
			break
	

	html = html[1].split("<div class='panel panel-primary'>")
	retorno.append(html[0])
	html = html[1].split("<div class='table-responsive'>")
	retorno.append(html[1])
	html = html[0].split("<div class='table-responsive' style='border:")
	retorno.append([])

	CABECALHO 	= "Departamento.*?cod=.*?>(.*?) <small> (.*?)</small></a></td>"\
					+ ".*?" \
					+ "da Disciplina</th><td>(.*?)</td></tr>" \
					+ ".*?" \
					+ "Nome</th><td><a title=.*?>(.*?) <i class=" \
					+ ".*?" \
					+ "\(Teor-Prat-Ext-Est\)</small></th><td>(\d+)-(\d+)-(\d+)-(\d+)" \
					+ ".*?" \
					+ "<h4>Campus (.*?)</h4>"
	TURMA 		= "<td class='turma'>(.*?)</td></tr>"
	VAGAS 		= "<tr><td>(.*?)</td>"\
					+ "<td>Vagas</td><td><span>(\d+)</span></td></tr>" \
					+ ".*?" \
					+ "<td>Ocupadas</td><td><span style=.*?>(\d+)</span></td></tr>" \
					+ ".*?" \
					+ "<td>Restantes</td><td><span style=.*?>(\d+)</span></td></tr>"
	HORARIOS	= "style='width: \d+px;'>(.*?)</td>"\
					+ "<td>(.*?)</td>"\
					+ "<td>(.*?)</td>"\
					+ ".*?"\
					+ "<td colspan='\d+'>(.*?)</td></tr>"
	PROFESSORES = "<tr><td>(.*?)</td></tr>"

	for i in range(len(html)):
		print(html[i]+'\n\n')
		if "panel-body" in html[i]:
			html[i] = html[i].split("<h4>")[1].split("</h4>")[0]
		else:

			html[i] = html[i].split("")
			#aux = aux.split("</thead>")[1]
			#regiaoturma = 
			turma = busca(TURMA, aux)
			vagas = busca(VAGAS, aux)
			if "<tr><td>" in vagas[0][0]:
				novo = []
				for i in vagas:
					novo.append(list(i))
				novo[0][0] = novo[0][0].split("<tr><td>")[-1]
				vagas = novo
			#horar = busca(HORARIOS, aux)

			print(turma)
			print(vagas)
			print(horar)
			retorno[4].append(aux)
	

	#for i in retorno:
		#if type(i) == str:
		#	print(i)
		#else:
		#	for j in i:
		#		print('\t' + str(j))
		#print(i)

	'''
	return True, retorno
	
def trans_4(html):
	pass
def trans_5(html):
	pass
def trans_6(html):
	pass
def trans_7(html):
	pass
def trans_8(html):
	pass
def trans_9(html):
	pass

def le_arquivo(nome):
	arquivo = open(nome, "r")
	linhas = arquivo.readlines()
	arquivo.close()
	for i in range(len(linhas)):
		linhas[i] = linhas[i].split('\n')[0]
		if '\r' in linhas[i]:
			linhas[i] = linhas[i].split('\r')[0]
	return linhas

def get_html(nome):
	linhas = le_arquivo(nome)
	string = ""
	for i in range(1, len(linhas)):
		string += linhas[i]
	return string

def get_1(	nivel = defines.Nivel.GRADUACAO, \
			campus = defines.Campus.DARCY):
	# Oferta
	# Lista de departamentos em um campus
	global pasta
	
	nivel		= str(nivel)
	campus		= str(campus)
	
	subpasta 	= pasta + "html/" + nivel + "/Oferta/"
	pagina		= "https://matriculaweb.unb.br/" + nivel + "/oferta_dep.aspx?cod=" + campus
	
	retorno		= get_html(subpasta + campus + ".txt")
	retorno		= trans_1(retorno)
	
	return retorno


def get_2(	nivel = defines.Nivel.GRADUACAO, \
			departamento = defines.Departamento.CIC):
	# Departamento
	# Oferta de um departamento, contem uma lista de disciplinas
	global pasta
	
	nivel		= str(nivel)
	departamento= str(departamento)
	
	subpasta 	= pasta + "html/" + nivel + "/Oferta/"
	pagina		= "https://matriculaweb.unb.br/" + nivel + "/oferta_dis.aspx?cod=" + departamento

	# Ainda a editar
	subpasta   += "1_"

	retorno		= get_html(subpasta + departamento + ".txt")
	retorno		= trans_2(retorno)
	
	return retorno

def get_3(	nivel = defines.Nivel.GRADUACAO, \
			disciplina = defines.Disciplina.APC, \
			departamento = None):
	# Disciplina
	# Turmas e oferta de uma disciplina
	global pasta
	
	nivel		= str(nivel)
	disciplina	= str(disciplina)
	
	subpasta 	= pasta + "html/" + nivel + "/Oferta/"
	pagina		= "https://matriculaweb.unb.br/" + nivel + "/oferta_dados.aspx?cod=" + disciplina
	if departamento != None:
		departamento = str(departamento)
		pagina += "&dep=" + departamento

	retorno		= get_html(subseta_dirpasta + departamento + "_" + disciplina + ".txt")
	retorno		= trans_3(retorno)
	
	return retorno
	
def get_4(	nivel = defines.Nivel.GRADUACAO, \
			disciplina = defines.Disciplina.APC):
	# Ementa
	# Ementa de uma determinada disciplina
	nivel		= str(nivel)
	disciplina	= str(disciplina)
	pagina		= "https://matriculaweb.unb.br/" + nivel + "/disciplina.aspx?cod=" + disciplina

def get_5(	nivel = defines.Nivel.GRADUACAO, \
			disciplina = defines.Disciplina.APC):
	# Espera
	# Lista de espera de uma determinada disciplina
	nivel		= str(nivel)
	disciplina	= str(disciplina)
	pagina		= "https://matriculaweb.unb.br/" + nivel + "/faltavaga_rel.aspx?cod=" + disciplina

def get_6(	nivel = defines.Nivel.GRADUACAO, \
			campus = defines.Campus.DARCY):
	# Curso
	# Lista de cursos em um determinado campus
	nivel		= str(nivel)
	campus		= str(campus)
	pagina		= "https://matriculaweb.unb.br/" + nivel + "/curso_rel.aspx?cod=" + campus


def get_7(	nivel = defines.Nivel.GRADUACAO, \
			curso = defines.Curso.CIC):
	# Habilitacao
	# Lista de habilitacoes de um determinado curso
	nivel		= str(nivel)
	# curso		= str(curso) # Nao necessario
	pagina		= "https://matriculaweb.unb.br/" + nivel + "/curso_dados.aspx?cod=" + curso

def get_8(	nivel = defines.Nivel.GRADUACAO, \
			habilitacao = defines.Habilitacoes.BCC):
	# Fluxo
	nivel		= str(nivel)
	habilitacao	= str(habilitacao)
	pagina		= "https://matriculaweb.unb.br/" + nivel + "/fluxo.aspx?cod=" + habilitacao

def get_9(	nivel = defines.Nivel.GRADUACAO, \
			habilitacao = defines.Habilitacoes.BCC):
	# Curriculo
	nivel		= str(nivel)
	habilitacao	= str(habilitacao)
	pagina		= "https://matriculaweb.unb.br/" + nivel + "/curriculo.aspx?cod=" + habilitacao

pasta = "../../Informacoes/temp_2018_01_22/"

if __name__ == "__main__":
	#bol, r = get_1(campus = defines.Campus.DARCY)
	#bol, r = get_1(campus = defines.Campus.PLANALTINA)
	#bol, r = get_1(campus = defines.Campus.CEILANDIA)
	#bol, r = get_1(campus = defines.Campus.GAMA)
	bol, r = get_2(departamento = defines.Departamento.CIC)
	#bol, r = get_2(departamento = defines.Departamento.ENE)
	#bol, r = get_3(departamento = defines.Departamento.CIC, disciplina = defines.Disciplina.APC)
	#bol, r = get_3(departamento = defines.Departamento.CIC, disciplina = defines.Disciplina.ED)
	print(bol)
	print(r)