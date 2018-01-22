string1 = "abc\n"
string2 = "def\n"
arq = open("teste.txt", "a")
arq.write(string1)
arq.close()
arq = open("teste.txt", "a")
arq.write(string2)
arq.close()