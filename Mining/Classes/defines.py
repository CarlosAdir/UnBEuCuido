#  -*- coding: utf-8 -*-
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
    CIC = "116"  # Computacao
    ENE = "163"  # Eletrica
    ENM = "164"  # Mecanica
    EST = "115"  # Estatistica
    GAMA = "650" 
    IFD = "550"  # Instituto de Física
    MAT = "113"  # Dep matematica

class Disciplina:
    IAL = 113093 # Intro Algebra Linear
    APC = 113476 # Algoritmos e Programacao de Computadores
    ED  = 116319 # Estrutura de Dados
    TP1 = 117889 # Tecnicas de Programacao 1
    TP2 = 117897 # Tecnicas de Programacao 2
    OA  = 116327 # Organizacao de Arquivos
    IIA = 116653 # Introducao à Inteligencia Artificial
    C1  = 113042 # Calculo 1 
    C2  = 116319 # Calculo 2
    CN  = 113417 # Calculo Numerico
    PE  = 115045 # Probabilidade e Estatistica

class Curso:
    CS  = "213" # Ciencias Sociais
    CIC = "370" # Ciencia da Computacao
    CB  = "94"  # Ciencias Biologicas
    MAT = "141" # Matematica

class Habilitacoes:
    '''Enumeração das habilitações de cada curso.'''
    BCC = 1856  # Ciência da Computação
    LIC = 1899  # Computação
    ENC = 1741  # Engenharia de Computação
    MECA = 6912  # Engenharia de Controle e Automação
    ENM = 6424 # Engenharia Mecânica
    CB  = 2216 # Ciencias Biologicas
    ANTRO = 3131 # Antropologia
    SOC1 = 3115 # Ciencias Sociais
    SOC2 = 3166 # Ciencias Sociais
    SOCI = 3123 # Sociologia
    MAT1 = 1325 # Matematica Licenciatura
    MAT2 = 1341 # Matematica Bacharel
