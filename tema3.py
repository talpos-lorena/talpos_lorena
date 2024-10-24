meniu = ['papanasi'] * 10 + ['ceafa'] * 3 + ["guias"] * 6
preturi = [["papanasi", 7], ["ceafa", 10], ["guias", 5]]
studenti = ["Liviu", "Ion", "George", "Ana", "Florica"]  # coada FIFO
comenzi = ["guias", "ceafa", "ceafa", "papanasi", "ceafa"]  # coada FIFO
tavi = ["tava"] * 7  # stiva LIFO
istoric_comenzi = []

cata_ceafa_era_la_inceput=meniu.count("ceafa")
cata_ceafa_s_a_comandat=comenzi.count("ceafa")
pret_ceafa=preturi[1][1]
castig_ceafa=cata_ceafa_s_a_comandat * pret_ceafa

cati_papanasi_erau_la_inceput=meniu.count("papanasi")
cati_papanasi_s_au_comandat=comenzi.count("papanasi")
pret_papanasi=preturi[0][1]
castig_papanasi=cati_papanasi_s_au_comandat * pret_papanasi

cat_guias_era_la_inceput=meniu.count("guias")
cat_guias_s_a_comandat=comenzi.count("guias")
pret_guias=preturi[2][1]
castig_guias=cat_guias_s_a_comandat * pret_guias


while studenti:
    student=studenti.pop(0)
    comanda=comenzi.pop(0)
    print(f"Studentul {student} a comandat {comanda}")
    istoric_comenzi.append([student, comanda])
    tavi.pop()

print(f"S-au comandat {cati_papanasi_s_au_comandat} papanasi, {cata_ceafa_s_a_comandat} ceafa, {cat_guias_s_a_comandat} guias")
print(f"Mai sunt {len(tavi)} tavi")

numar_ceafa_ramasa=cata_ceafa_era_la_inceput - cata_ceafa_s_a_comandat
numar_papanasi_ramasi=cati_papanasi_erau_la_inceput - cati_papanasi_s_au_comandat
numar_guias_ramas=cat_guias_era_la_inceput - cat_guias_s_a_comandat

if numar_ceafa_ramasa>0:
    print("Mai este ceafa: True")
else:
    print("Mai este ceafa: False")


if numar_papanasi_ramasi>0:
         print("Mai sunt papanasi:True")
else:
         print("Mai sunt papanasi:False")

if numar_guias_ramas>0:
     print("Mai este guias: True")
else:
     print("Mai este guias: False")

