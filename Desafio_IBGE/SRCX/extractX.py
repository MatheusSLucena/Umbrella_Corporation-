import requests

class ExtractX():
    def __initX__(self):
        pass
    def extractX(self):
        # Solicitação do usuário
        x = int(input("Qual data base deseja acessar:\n(Escolha a partir do indice numérico)\n"))
        y = str(input("Qual sexo deseja acessar:\n 4 - Homens\n 5 - Mulheres\nall - Ambos\n"))
        url = (f"https://servicodados.ibge.gov.br/api/v3/agregados/4093/periodos/201201-202602/variaveis/{x}?localidades=N3[26]&classificacao=2[{y}]")

        req = requests.get(url)
        data = req.json()
        return data,x,y