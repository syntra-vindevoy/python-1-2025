from time import time

now = time()
days = now // 86400
seconds_overschot = now % 86400

het_uur = seconds_overschot // 3600
resterende_seconden = seconds_overschot % 3600

huidige_minuut = resterende_seconden // 60
laatste_overschot = int(resterende_seconden % 60)

print("Dagen sinds 1 jan 1970:", int(days))
print("Uur (UTC):", int(het_uur))
print("Minuut:", int(huidige_minuut))
print("Seconde:", laatste_overschot)
