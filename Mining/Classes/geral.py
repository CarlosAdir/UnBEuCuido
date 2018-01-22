from get_data import *
import defines

if __name__ == "__main__":
	niveis = [defines.Nivel.GRADUACAO]
	campus = [defines.Campus.DARCY, defines.Campus.PLANALTINA, defines.Campus.CEILANDIA, defines.Campus.GAMA]
	everything = []
	for nivel in niveis:
		for campi in campus:
			everything.append(CAMPI(nivel, campi))
	for campi in everything:
		campi.get_all()

	cons = everything[0]
	
	
	#for campi in everything:
	#	for departamento in campi.lista:
	#		print(departamento)

	