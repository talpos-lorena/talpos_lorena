import random
import csv
from collections import defaultdict

judete = [
    (1, 'Alba'), (2, 'Arad'), (3, 'Arges'), (4, 'Bacau'), (5, 'Bihor'), (6, 'Bistrita-Nasaud'),
    (7, 'Botosani'), (8, 'Brasov'), (9, 'Braila'), (10, 'Buzau'), (11, 'Caras-Severin'), (12, 'Cluj'),
    (13, 'Constanta'), (14, 'Covasna'), (15, 'Dambovita'), (16, 'Dolj'), (17, 'Galati'), (18, 'Gorj'),
    (19, 'Harghita'), (20, 'Hunedoara'), (21, 'Ialomita'), (22, 'Iasi'), (23, 'Ilfov'), (24, 'Maramures'),
    (25, 'Mehedinti'), (26, 'Mures'), (27, 'Neamt'), (28, 'Olt'), (29, 'Prahova'), (30, 'Satu Mare'),
    (31, 'Salaj'), (32, 'Sibiu'), (33, 'Suceava'), (34, 'Teleorman'), (35, 'Timis'), (36, 'Tulcea'),
    (37, 'Vaslui'), (38, 'Valcea'), (39, 'Vrancea'), (40, 'Bucuresti'), (41, 'Calarasi'), (42, 'Giurgiu')
]

judete_dict = {code: name for code, name in judete}

def genereaza_cnp():
    sex = random.choice([1, 2, 3, 4])
    an = random.randint(1920, 2022) % 100
    luna = random.randint(1, 12)
    zi = random.randint(1, 31)
    judet = random.randint(1, 42)
    nr_ordine = random.randint(0, 999)
    cnp_fara_control = f"{sex}{an:02d}{luna:02d}{zi:02d}{judet:02d}{nr_ordine:03d}"
    control = calcul_cifra_control(cnp_fara_control)
    return cnp_fara_control + str(control), sex, an, judet

def calcul_cifra_control(cnp_fara_control):
    coeficienti = [2, 7, 9, 1, 4, 6, 8, 5, 3, 2, 7, 9]
    suma = sum(int(cnp_fara_control[i]) * coeficienti[i] for i in range(12))
    rest = suma % 11
    return rest if rest != 10 else 1

def genereaza_nume():
    prenume = random.choice(["Andrei", "Maria", "Ion", "Elena", "George", "Ioana", "Mihai", "Ana", "Vasile", "Gabriela"])
    nume = random.choice(["Popescu", "Ionescu", "Georgescu", "Dumitrescu", "Constantin", "Marin", "Radu", "Munteanu", "Popa", "Stan"])
    return f"{prenume} {nume}"

def calculeaza_varsta(an_nastere):
    if an_nastere < 22:
        an_nastere += 2000
    else:
        an_nastere += 1900
    varsta = 2025 - an_nastere
    return varsta

def genereaza_csv(numar_cnpuri=1000000):
    with open("cnpuri.csv", mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["CNP", "Nume", "Sex", "An", "Judet", "JudetNume"])
        for _ in range(numar_cnpuri):
            cnp, sex, an, judet = genereaza_cnp()
            nume = genereaza_nume()
            judet_nume = judete_dict.get(judet, "Necunoscut")
            writer.writerow([cnp, nume, sex, an, judet, judet_nume])

genereaza_csv()

class HashTable:
    def __init__(self, size):
        self.size = size
        self.table = [[] for _ in range(size)]

    def hash_function(self, key):
        return int(key[:8]) % self.size

    def insert(self, key, value):
        hash_index = self.hash_function(key)
        self.table[hash_index].append((key, value))

    def search(self, key):
        hash_index = self.hash_function(key)
        for i, (cnp, nume) in enumerate(self.table[hash_index]):
            if cnp == key:
                return i + 1
        return -1

hash_table = HashTable(1000)

statistici_sex = {"barbati": 0, "femei": 0}
statistici_judete = defaultdict(int)
statistici_varsta = {"1-18": 0, "18-55": 0, "55-102": 0}

with open("cnpuri.csv", mode='r', encoding='utf-8') as file:
    reader = csv.reader(file)
    next(reader)
    for row in reader:
        cnp = row[0]
        nume = row[1]
        sex = int(row[2])
        an = int(row[3])
        judet = int(row[4])
        judet_nume = row[5]

        varsta = calculeaza_varsta(an)

        if sex in [1, 3, 5, 7]:
            statistici_sex["barbati"] += 1
        elif sex in [2, 4, 6, 8]:
            statistici_sex["femei"] += 1

        statistici_judete[judet_nume] += 1

        if varsta <= 18:
            statistici_varsta["1-18"] += 1
        elif varsta <= 55:
            statistici_varsta["18-55"] += 1
        else:
            statistici_varsta["55-102"] += 1

        hash_table.insert(cnp, nume)

print(f"Numar barbati: {statistici_sex['barbati']}")
print(f"Numar femei: {statistici_sex['femei']}")
print("\nNumar persoane pe judete:")
for judet, numar in statistici_judete.items():
    print(f"{judet}: {numar} persoane")
print("\nDistributia pe varste:")
for categorie, numar in statistici_varsta.items():
    print(f"{categorie}: {numar} persoane")

numar_istorii = 1000
non_empty_buckets = [bucket for bucket in hash_table.table if bucket]

for _ in range(numar_istorii):
    if non_empty_buckets:
        random_bucket = random.choice(non_empty_buckets)
        random_cnp, _ = random.choice(random_bucket)
        iterații = hash_table.search(random_cnp)
        print(f"Cautare CNP: {random_cnp}, numar de iteratii: {iterații}")
    else:
        print("Tabelul de hash este gol, nu exista CNP-uri de cautat.")
