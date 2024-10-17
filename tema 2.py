from sys import api_version

text="""Pescuitul este activitatea de a prinde cu ajutorul unor instrumente speciale diverse varietăți de pește sau alte vietăți acvatice. Pescuitul mai poate fi considerat ca o extracție a organismelor acvatice, din mediul în care au crescut, cu diverse scopuri, precum alimentare, recreere (pescuit sportiv), ornamentare (captura speciilor ornamentale) sau țeluri industriale"""
jumatate=len(text)//2
prima_jumatate=text[:jumatate]
a_doua_jumatate=text[jumatate:]
prima_jumatate=prima_jumatate.upper()
prima_jumatate=prima_jumatate.strip(" ")
# print(prima_jumatate)

a_doua_jumatate=a_doua_jumatate[::-1]
a_doua_jumatate=a_doua_jumatate.capitalize()
a_doua_jumatate=a_doua_jumatate.replace(".", "")
a_doua_jumatate=a_doua_jumatate.replace(",", "")
a_doua_jumatate=a_doua_jumatate.replace("!", "")
a_doua_jumatate=a_doua_jumatate.replace("?", "")
# print(a_doua_jumatate)

text=prima_jumatate+a_doua_jumatate
print(text)