from main import main

ip = input("IP >> ")
while 1:
    port = input("PORT >> ")
    try:
        port = port.replace(" ", "")
        port = int(port)
        if port == "":
            print("portu yanlış girdiniz")
            continue

    except ValueError:
        print("portu yanlış girdiniz")
        continue

    break

obj =  main(ip, port)
obj.runtime()

