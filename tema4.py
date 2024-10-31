
# 1. Lista de cuvinte și alegerea cuvântului la întâmplare
import random
cuvinte = ["python", "programare", "calculator", "date", "algoritm"]
cuvant_de_ghicit = random.choice(cuvinte)
progres = ["_" for _ in cuvant_de_ghicit]

# 2. Inițializarea numărului de încercări
incercari_ramase = 6
litere_incercate = []
def afisare_progres():
    print(" "," ".join(progres))
print("Bine ai venit la jocul Spanzuratoarea!")
print("Cuvantul de ghicit este: " + " ".join(progres))
print(f"Incercari ramase: {incercari_ramase}")

while "_" in progres and incercari_ramase>0:

    print("Litere incercate:", ", ".join(litere_incercate))
    litera=input("Introdu o litera: ").lower()
    if len(litera) != 1 or not litera.isalpha():
      print("Te rog sa introduci o singura litera valida.")
      continue
    if litera in litere_incercate:
      print("Ai mai incercat aceasta litera. Incearca alta.")
      continue
    litere_incercate.append(litera)
    if litera in cuvant_de_ghicit:
       print("Corect!")
       for i in range(len(cuvant_de_ghicit)):
           if cuvant_de_ghicit[i]==litera:
               progres[i]=litera
    else:
        incercari_ramase -=1
        print("Gresit!")
    afisare_progres()
    print(f"Incercari ramase: {incercari_ramase}")

if "_" not in progres:
    print(f"Felicitari! Ai ghicit cuvantul: {cuvant_de_ghicit}!")
else:
    print(f"Ai pierdut! Cuvantul era: {cuvant_de_ghicit}.")

