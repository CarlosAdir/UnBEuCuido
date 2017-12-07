from defines import *
import auxiliar

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


