from client import client

ip = input("IP >> ")

while True:
    port = input("PORT >> ")
    port = port.replace(" ", "")
    if port == "":
        print("yanlış bir port değeri girdiniz")
        continue
    
    try:
        port = int(port)

    except ValueError:
        print("yanlış bir port değeri girdiniz")
        continue

    break

name = input("ISIM >> ")

client = client(ip, port, name)
client.init_connection()
