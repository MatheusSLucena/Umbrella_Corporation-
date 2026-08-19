class ReadX():
    def __initX__(self):
        pass
    def readX(self):
        with open("IBGEx.txt","r",encoding="utf-8") as f:
            ler = f.readlines()
            linhas = [linha.strip() for linha in ler]
            print("_________________________________\nSegue lista de itens disponíveis:\n")
            for item in linhas:
                print(item)
            print("---------------------------------")