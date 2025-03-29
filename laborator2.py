import hashlib
import time

# Hash-ul parolei reale
target_hash = "0e000d61c1735636f56154f30046be93b3d71f1abbac3cd9e3f80093fdb357ad"


# Funcția de criptare a parolei
def get_hash(password):
    return hashlib.sha256(password.encode()).hexdigest()


# Generator pentru caractere
upper_case = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
lower_case = 'abcdefghijklmnopqrstuvwxyz'
digits = '0123456789'
special_chars = '!@#$'

# Variabile pentru a urmări numărul de apeluri recursive
recursion_count = 0


# Funcția de backtracking pentru generarea parolelor candidate
def backtrack(password, upper, lower, digit, special):
    global recursion_count
    recursion_count += 1

    # Afișăm statusul curent pentru debug
    if recursion_count % 100000 == 0:
        print(f"Apeluri recursive: {recursion_count}, Parola partiala: {password}")

    # Verificăm dacă am ajuns la o parolă de 6 caractere
    if len(password) == 6:
        # Verificăm dacă respectă toate condițiile
        if upper == 1 and lower == 3 and digit == 1 and special == 1:
            # Calculăm hash-ul parolei candidate
            candidate_hash = get_hash(password)
            # Comparăm cu hash-ul real
            if candidate_hash == target_hash:
                # Afișăm parola găsită și numărul de apeluri recursive
                print(f"Parola găsită: {password}")
                print(f"Număr apeluri recursive: {recursion_count}")
                return True  # Oprirea căutării după ce găsim parola
        return False

    # Generăm recursiv parolele pentru fiecare tip de caracter
    for char in upper_case:  # Adăugăm literă mare
        if upper < 1:
            if backtrack(password + char, upper + 1, lower, digit, special):
                return True

    for char in lower_case:  # Adăugăm literă mică
        if lower < 3:
            if backtrack(password + char, upper, lower + 1, digit, special):
                return True

    for char in digits:  # Adăugăm cifră
        if digit < 1:
            if backtrack(password + char, upper, lower, digit + 1, special):
                return True

    for char in special_chars:  # Adăugăm caracter special
        if special < 1:
            if backtrack(password + char, upper, lower, digit, special + 1):
                return True

    return False


# Măsurarea timpului de execuție
start_time = time.time()

# Apelăm funcția de backtracking
found = backtrack('', 0, 0, 0, 0)

end_time = time.time()

# Dacă nu am găsit parola, afișăm un mesaj
if not found:
    print("Parola nu a fost găsită.")
else:
    # Afișăm timpul de execuție al programului
    print(f"Timp de execuție: {end_time - start_time} secunde")
