from defines import *
import auxiliar

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