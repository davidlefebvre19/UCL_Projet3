from sense_hat import SenseHat, ACTION_PRESSED, ACTION_HELD, ACTION_RELEASED
sense = SenseHat()
sense.low_light = True
from time import sleep
from signal import pause
from subprocess import call

white = (255,255,255)
red = (255,0,0)
green = (0,255,0)
orange = (255,128,0)
key = "louvain"

def decode(key, cipher_text): #Fonction dechiffrant le message selon le chiffrement vigenere
	dec = []
	for i, e in enumerate(cipher_text):
	    key_c = key[i % len(key)]
	    dec_c = chr((256 + ord(e) - ord(key_c)) % 256)
	    dec.append(dec_c)
	return str("".join(dec))

def Show_Decrypted():
	f = open("message.txt", "r")
	encrypted_message = f.read()
	f.close()
	message = decode(key, encrypted_message)
	sense.show_message(message, text_colour=orange)

Show_Decrypted()
call("sudo shutdown now", shell=True)




