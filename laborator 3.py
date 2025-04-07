import json
import random
import copy
import os

def creeaza_fisier_daca_nu_exista(filename):
    date_exemplu = {
        "bancnote": [
            { "valoare": 50, "stoc": 20 },
            { "valoare": 20, "stoc": 30 },
            { "valoare": 10, "stoc": 40 },
            { "valoare": 5, "stoc": 50 },
            { "valoare": 1, "stoc": 100 }
        ],
        "produse": [
            { "nume": "Lapte", "pret": 7 },
            { "nume": "Paine", "pret": 3 },
            { "nume": "Ciocolata", "pret": 5 },
            { "nume": "Apa", "pret": 2 },
            { "nume": "Cafea", "pret": 9 }
        ]
    }
    if not os.path.exists(filename):
        with open(filename, 'w') as f:
            json.dump(date_exemplu, f, indent=2)
        print(f" Fisierul '{filename}' a fost creat cu date exemplu.")

def citeste_datele(filename):
    with open(filename, 'r') as f:
        return json.load(f)

def calculeaza_rest(rest, bancnote):
    dp = [None] * (rest + 1)
    dp[0] = (0, [0] * len(bancnote))

    for i, (valoare, stoc) in enumerate(bancnote):
        for r in range(rest, -1, -1):
            if dp[r] is not None:
                max_buc = min((rest - r) // valoare, stoc)
                for k in range(1, max_buc + 1):
                    nou_rest = r + valoare * k
                    if nou_rest <= rest:
                        total_bancnote = dp[r][0] + k
                        combinatii = dp[r][1][:]
                        combinatii[i] += k
                        if dp[nou_rest] is None or dp[nou_rest][0] > total_bancnote:
                            dp[nou_rest] = (total_bancnote, combinatii)
    return dp[rest]

def afiseaza_rest(combinatie, bancnote):
    output = []
    for i, nr in enumerate(combinatie):
        if nr > 0:
            output.append(f"{nr} x {bancnote[i][0]} RON")
    return ", ".join(output)

def simuleaza_casa(json_file):
    creeaza_fisier_daca_nu_exista(json_file)
    date = citeste_datele(json_file)
    bancnote_init = [(b["valoare"], b["stoc"]) for b in date["bancnote"]]
    produse = date["produse"]
    stoc_bancnote = copy.deepcopy(bancnote_init)
    client = 1

    while True:
        produs = random.choice(produse)
        pret = produs["pret"]
        suma_platita = pret + random.randint(1, 20)
        rest = suma_platita - pret

        rezultat = calculeaza_rest(rest, stoc_bancnote)

        print(f"\n Clientul {client}")
        print(f" Produs cumparat: {produs['nume']}")
        print(f" Pret: {pret} RON")
        print(f" Suma platita: {suma_platita} RON")
        print(f" Rest de oferit: {rest} RON")

        if rezultat is None:
            print(" Nu se poate oferi restul cu stocul disponibil.")
            print(" Simularea s-a oprit.")
            break

        numar_bancnote, combinatie = rezultat
        print(f" Rest oferit cu {numar_bancnote} bancnote: {afiseaza_rest(combinatie, bancnote_init)}")

        for i in range(len(stoc_bancnote)):
            stoc_bancnote[i] = (stoc_bancnote[i][0], stoc_bancnote[i][1] - combinatie[i])

        client += 1

simuleaza_casa("date_magazin.json")
