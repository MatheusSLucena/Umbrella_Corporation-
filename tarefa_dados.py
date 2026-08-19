import requests



class IBGE:

    def __init__(self, tabela):
        self.tabela = tabela
        self.base_url = "https://servicodados.ibge.gov.br/api/v3/agregados/4093/periodos/201201|201202|201203|201204|201301|201302|201303|201304|201401|201402|201403|201404|201501|201502|201503|201504|201601|201602|201603|201604|201701|201702|201703|201704|201801|201802|201803|201804|201901|201902|201903|201904|202001|202002|202003|202004|202101|202102|202103|202104|202201|202202|202203|202204|202301|202302|202303|202304|202401|202402|202403|202404|202501|202502|202503|202504|202601|202602/variaveis/4096|4099|12466?localidades=N6[N3[26]]&classificacao=2[all]"

    def consultar(self, variavel, sexo):

        url = (
            f"{self.base_url}/t/{self.tabela}"
            f"/n1/all"
            f"/v/{variavel}"
            f"/c{sexo}"
        )

        resposta = requests.get(url)

        if resposta.status_code == 200:
            return resposta.json()

        print(f"Erro na consulta: {resposta.status_code}")
        return None


# -----------------------------
# Opções disponíveis
# -----------------------------

variaveis = {
    "1": ("4099", "Taxa de desocupação"),
    "2": ("4096", "Taxa de participação na força de trabalho"),
    "3": ("12466", "Taxa de informalidade")
}

sexos = {
    "1": ("6794", "Total"),
    "2": ("4", "Homens"),
    "3": ("5", "Mulheres")
}


# -----------------------------
# Menu de variáveis
# -----------------------------

print("=== VARIÁVEIS ===")

for codigo, dados in variaveis.items():
    print(f"{codigo} - {dados[1]}")

opcao_variavel = input("Escolha uma variável: ")

variavel, nome_variavel = variaveis[opcao_variavel]


# -----------------------------
# Menu de sexo
# -----------------------------

print("\n=== SEXO ===")

for codigo, dados in sexos.items():
    print(f"{codigo} - {dados[1]}")

opcao_sexo = input("Escolha o sexo: ")

sexo, nome_sexo = sexos[opcao_sexo]


# -----------------------------
# Consulta à API
# -----------------------------

ibge = IBGE(4093)

dados = ibge.consultar(variavel, sexo)


# -----------------------------
# Resultado
# -----------------------------

if dados:

    print("\n=== RESULTADO ===")
    print(f"Variável: {nome_variavel}")
    print(f"Sexo: {nome_sexo}")

    for registro in dados:
        print(registro)