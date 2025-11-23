#! python
fruit = 'banana'

first_letter = fruit[0]
second_letter= fruit[1]

i = 10
#print(fruit[i]) # creeert een index error

i = -1
print(fruit[i]) #telt van achter naar voor

i = -2
print(fruit[i]) #tot je weer te ver gaat natuurlijk ;)

print(fruit[0:3]) #nooit loopen over ne string

print(fruit[0:10]) #hij print gewoon tot het einde (geen index error)

print(fruit[0:5:2]) #je kan er gewoon nen step tussen steken

print(fruit[0:]) # of print(fruit[:])

print(fruit[::-1]) #achterstevoren
print(str(9)<str(10)) #zou true moeten zijn maar omdat het strings zijn is dit dus wel degelijk false
print('009'<'010') # oplossen door de prefixen
print("02112025" > "10102025") # oppassen met data!
print("20251101">"20251010") #altijd data omkeren, dit gaat welg oed
import uuid
print(uuid.uuid4())
print(uuid.uuid4())
