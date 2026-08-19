from SRCX.extractX import ExtractX
from SRCX.loadX import LoadX
from SRCX.readX import ReadX
from SRCX.validX import ValidX
from SRCX.validX import dados
ld = LoadX()
red = ReadX()
ind = ValidX()

# Apresentação dos dados para o usuário para poder escolher o índice que deseja
red.readX()
ind.validx()

# Coloquei a validação de dados aqui pois tive problemas em utilizar o método para validar por meio de outro arquivo
## OBS: Tive que fazer ajustes na dada base copiada dentro do arquivo .txt para poder copiar a quantidade correta de índices
dados = []
with open("IBGEx.txt", "r", encoding="utf-8") as f:
    for lines in f:
        parts = lines.strip().split("-")
        if len(parts) == 2:
            indices = int(parts[0])
            dados.append(indices)


# Ativação da escolha personalizada de URL para a extração
ext = ExtractX()
data, x, y = ext.extractX()


# Criação e edição do nome do arquivo
if x in dados:
    if y == "4":
        print(ld.load_json(f"{x} - Homens - 14y PE",data))
    elif y == "5":
        print(ld.load_json(f"{x} - Mulheres - 14y PE",data))
    else:
        print(ld.load_json(f"{x} - Homens e Mulheres - 14y PE",data))
else:
    print("Apenas informe os índices da lista!")