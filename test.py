from main import main

def test():
    obj =  main("127.0.0.1", 2112)
    obj.runtime()

if __name__ == "__main__":
    test()
