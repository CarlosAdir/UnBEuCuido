from defines import *
import auxiliar
import re

def departamentos(nivel = Nivel.GRADUACAO, campi = Campus.DARCY, pasta = "Informacoes/temp/", processo = -1):
	# a pagina é como:
	# https://matriculaweb.unb.br/graduacao/oferta_dep.aspx?cod=1
	campi			= str(campi)
	auxiliar.cria_pasta(("Informacoes", "temp", Estado.html, 	nivel, "Oferta"))
	auxiliar.cria_pasta(("Informacoes", "temp", Estado.tratado, 	nivel, "Oferta"))
	pagina 			= 'https://matriculaweb.unb.br/' + nivel + '/oferta_dep.aspx?cod=' 	+ campi
	origem 			= pasta + Estado.html 			 + nivel + "/Oferta/" 				+ campi + ".txt"
	destino 		= pasta + Estado.tratado 		 + nivel + "/Oferta/" 				+ campi + '.txt'
	tempo, html, info_util = auxiliar.common(pagina, origem, destino, processo)
	if info_util != None:
		return info_util
	# Trata os dados de departamentos em um campi
	# print("Chegou")
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
		for i in range(len(info_util)):
			info_util[i] = info_util[i].split('</td><td>')
			info_util[i][2] = info_util[i][2].split("' style='text-transform: uppercase;'>")[1]
			info_util[i][2] = info_util[i][2].split("</a></td></tr>")[0]
		auxiliar.grava(info_util, pasta + Estado.tratado + nivel + "/Oferta/" + campi + '.txt', tempo)
	else:
		auxiliar.grava_erro('Oferta.departamentos:nivel=' + nivel + ";campi=" + campi)
		return [[]] 
	# em info_util ja esta armazenado como info_util[i] = [codigo, sigla, nome]
	return info_util
	
def disciplinas(departamento, nivel = Nivel.GRADUACAO, campi = Campus.DARCY, pasta = "Informacoes/temp/", processo = -1):
	# campi nao adianta de nada pois nao interfere no resultado final.
	# Apenas colocado para auxiliar no armazenamento
	# mas é facilmente tirado. A utilizacao é somente para iteracao
	# a pagina é como https://matriculaweb.unb.br/graduacao/oferta_dis.aspx?cod=422
	# departamento sempre será string pois existe o departamento denominado "003" em vez de 3.
	campi 			= str(campi)
	auxiliar.cria_pasta(("Informacoes", "temp", Estado.html, 	nivel, "Oferta"))
	auxiliar.cria_pasta(("Informacoes", "temp", Estado.tratado, 	nivel, "Oferta"))
	pagina 			= 'https://matriculaweb.unb.br/' + nivel + '/oferta_dis.aspx?cod=' 	+ departamento
	origem 			= pasta + Estado.html 			 + nivel + "/Oferta/" 				+ campi + "_" + departamento + ".txt"
	destino 		= pasta + Estado.tratado 		 + nivel + "/Oferta/" 				+ campi + "_" + departamento + ".txt"
	tempo, html, info_util = auxiliar.common(pagina, origem, destino, processo)
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
		for i in range(len(info_util)):
			info_util[i] = info_util[i].split('<tr><td>')[1]
			info_util[i] = info_util[i].split("<a title='")
			info_util[i][0] = info_util[i][0].split("</td><td><a href=")[0]
			info_util[i][1] = info_util[i][1].split("' href='")[0]
		auxiliar.grava(info_util, pasta + Estado.tratado + nivel + "/Oferta/" + campi + "_" + departamento + ".txt", tempo)
	else:
		auxiliar.grava_erro('Oferta.disciplinas:nivel=' + nivel + ";dep=" + departamento)
		return [[]]
	return info_util


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

	busca = re.findall


	disciplina 		= str(disciplina)
	auxiliar.cria_pasta(("Informacoes", "temp", Estado.html, 	nivel, "Oferta", "turmas"))
	auxiliar.cria_pasta(("Informacoes", "temp", Estado.tratado, 	nivel, "Oferta", "turmas"))
	pagina 			= 'https://matriculaweb.unb.br/' + nivel + '/oferta_dados.aspx?cod='+ disciplina 	+ '&dep=' 	+ departamento
	origem 			= pasta + Estado.html 			 + nivel + "/Oferta/turmas/" 		+ departamento 	+ "_" 		+ disciplina + ".txt"
	destino 		= pasta + Estado.tratado 		 + nivel + "/Oferta/turmas/" 		+ departamento 	+ "_" 		+ disciplina + ".txt"
	tempo, html, info_util = auxiliar.common(pagina, origem, destino, processo)
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
		print(info_util[0])
		#info_util.remove(info_util[-1])
		#for i in range(1,len(info_util)-1):
		#	pass
		#quantidade = info_util.count("Turno")
		#info_util = busca(TURMAS, info_util)
		#if(len(info_util) == quantidade):
			#print info_util
		#	pass
		#else:
		#	print "Deu erro com " + disciplina + " de " + departamento


		auxiliar.grava(info_util, pasta + Estado.tratado + nivel + "/Oferta/turmas/" + departamento + "_" + disciplina + ".txt", tempo)
	else:
		info_util = []
		print(disciplina + " - " + departamento)

	return info_util


def espera(disciplina, nivel = Nivel.GRADUACAO, pasta = "Informacoes/temp/", processo = -1): # Incompleto
# a pagina é como:
# https://matriculaweb.unb.br/graduacao/faltavaga_rel.aspx?cod=116319
	disciplina 		= str(disciplina)
	auxiliar.cria_pasta(("Informacoes", "temp", Estado.html, 	nivel, "Oferta", "espera"))
	auxiliar.cria_pasta(("Informacoes", "temp", Estado.tratado, 	nivel, "Oferta", "espera"))
	pagina 			= 'https://matriculaweb.unb.br/' + nivel + '/faltavaga_rel.aspx?cod=' + disciplina
	origem 			= pasta + Estado.html 			 + nivel + "/Oferta/espera/" 		  + disciplina + ".txt"
	destino 		= pasta + Estado.tratado 		 + nivel + "/Oferta/espera/" 		  + disciplina + ".txt"
	tempo, html, info_util = auxiliar.common(pagina, origem, destino, processo, random.uniform(0, 0.5))
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
		for i in range(len(info_util)):
			info_util[i] = info_util[i].split("</td><td>")
			for j in range(len(info_util[i])):
				if " <small>" in info_util[i][j]:
					info_util[i][j] = info_util[i][j].replace(" <small>","-")
					info_util[i][j] = info_util[i][j].replace(" </small>","")
				elif "</td></tr>" in info_util[i][j]:
					info_util[i][j] = info_util[i][j].replace("</td></tr>","")
		auxiliar.grava(info_util, pasta + Estado.tratado + nivel + "/Oferta/espera/" + disciplina + ".txt", tempo)
		contador += 1
	else:
		auxiliar.grava_erro('Oferta.espera:nivel=' + nivel + ";disc=" + disciplina)
		return [[]]
	return info_util