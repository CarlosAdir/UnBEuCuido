from defines import *
import auxiliar
import re

class CAMPI():
	"""

	"""
	def __init__(self, nivel, campi, pasta = "Informacoes/temp/"):
		self.nivel = str(nivel)
		self.campi = str(campi)
		self.pasta = pasta
		self.lista = []

	def __str__(self):
		return "Nivel: " + self.nivel + '\nCampi' + self.nivel

	def get(self, processo = -1):
		# a pagina é como:
		# https://matriculaweb.unb.br/graduacao/oferta_dep.aspx?cod=1
		auxiliar.cria_pasta(("Informacoes", "temp", Estado.html, self.nivel, "Oferta"))
		auxiliar.cria_pasta(("Informacoes", "temp", Estado.tratado, self.nivel, "Oferta"))
		pagina 			= 'https://matriculaweb.unb.br/' + self.nivel + '/oferta_dep.aspx?cod=' + self.campi
		origem 			= self.pasta + Estado.html + self.nivel + "/Oferta/" + self.campi + ".txt"
		destino 		= self.pasta + Estado.tratado + self.nivel + "/Oferta/"	+ self.campi + '.txt'
		tempo, html, info_util = auxiliar.common(pagina, origem, destino, processo)
		self.tempo = tempo
		if info_util == None: # Existe somente o html
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
				return False
			# em info_util ja esta armazenado como info_util[i] = [codigo, sigla, nome]
		for i in info_util:
			new = DEPARTAMENTO(self.nivel, self.campi, i[0], i[1], i[2], self.pasta)
			self.lista.append(new)
		return True
	def get_all(self):
		if(len(self.lista) == 0):
			self.get()
		for departamento in self.lista:
			departamento.get()
		for departamento in self.lista:
			departamento.get_all()



class DEPARTAMENTO():
	"""
	Essa classe consiste em armazenar todas as informações de um departamento
	Tais como sigla, nome, lista de disciplinas ofertadas e etc
	"""
	def __init__(self, nivel, campi, codigo, sigla, denominacao, pasta):
		self.nivel = nivel
		self.campi = campi # Desnecessario
		self.codigo = codigo # Codigo do departamento
		self.sigla = sigla
		self.denominacao = denominacao
		self.pasta = pasta
		self.lista = []
	def __str__(self):
		return self.codigo + " - " + self.sigla + " - " + self.denominacao
	def get(self, processo = -1):
		auxiliar.cria_pasta(("Informacoes", "temp", Estado.html, self.nivel, "Oferta"))
		auxiliar.cria_pasta(("Informacoes", "temp", Estado.tratado, self.nivel, "Oferta"))
		pagina 			= 'https://matriculaweb.unb.br/' + self.nivel + '/oferta_dis.aspx?cod=' + self.codigo
		origem 			= self.pasta + Estado.html 		 + self.nivel + "/Oferta/" 				+ self.campi + "_" + self.codigo + ".txt"
		destino 		= self.pasta + Estado.tratado 	 + self.nivel + "/Oferta/" 				+ self.campi + "_" + self.codigo + ".txt"
		tempo, html, info_util = auxiliar.common(pagina, origem, destino, processo)
		self.tempo = tempo
		if info_util == None:
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
				auxiliar.grava(info_util, pasta + Estado.tratado + self.nivel + "/Oferta/" + self.campi + "_" + self.codigo + ".txt", self.tempo)
			else:
				auxiliar.grava_erro('Oferta.disciplinas:nivel=' + self.nivel + ";dep=" + self.codigo)
				return False
		for i in info_util:
			self.lista.append(DISCIPLINA(self.nivel, self.codigo, i[0], i[1]))
		return True
	def get_all(self):
		if(len(self.lista) == 0):
			self.get()
		for disciplina in self.lista:
			disciplina.get()
		for disciplina in self.lista:
			disciplina.get_all()


class DISCIPLINA():

	def __init__(self, nivel, departamento, codigo, denominacao):
		self.nivel = nivel
		self.departamento = departamento
		self.codigo = codigo
		self.denominacao = denominacao
		self.turmas = {}
	def get(self, processo = -1):
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


		auxiliar.cria_pasta(("Informacoes", "temp", Estado.html, self.nivel, "Oferta", "turmas"))
		auxiliar.cria_pasta(("Informacoes", "temp", Estado.tratado, self.nivel, "Oferta", "turmas"))
		pagina 			= 'https://matriculaweb.unb.br/' + self.nivel + '/oferta_dados.aspx?cod=' + self.codigo		  + '&dep=' 	+ self.departamento
		origem 			= pasta + Estado.html 			 + self.nivel + "/Oferta/turmas/" 		  + self.departamento + "_" 		+ self.codigo + ".txt"
		destino 		= pasta + Estado.tratado 		 + self.nivel + "/Oferta/turmas/" 		  + self.departamento + "_" 		+ self.codigo + ".txt"
		tempo, html, info_util = auxiliar.common(pagina, origem, destino, processo)
		self.tempo = tempo
		if info_util == None:


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
				auxiliar.grava_erro('Oferta.disciplinas:nivel=' + self.nivel + ";dep=" + self.codigo)
				return False
		dados = info_util[0]
		info_util.delete(0)
		
		return info_util

class TURMA():
	"""

	"""
	def __init__(self, sigla, vagas, turno, horario_local, professor, obs):
		self.sigla = sigla
		self.vagas = vagas
		self.turno = turno
		self.horario_local = horario_local
		self.professor = professor
		self.obs = obs

class EMENTA():
	"""

	"""
	def __init__(self, orgao, codigo, denominacao, nivel, vigencia, prerequisitos, ementa, bibliografia):
		self.orgao = orgao
		self.codigo = codigo
		self.denominacao = denominacao
		self.nivel = nivel
		self.vigencia = vigencia
		self.prerequisitos = prerequisitos
		self.ementa = ementa
		self.bibliografia = bibliografia