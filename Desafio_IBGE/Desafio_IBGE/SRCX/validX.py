

class ValidX():
    def __init__(self):
        pass

    def validx(self):
        dados = []
        with open("IBGEx.txt", "r", encoding="utf-8") as f:
            for lines in f:
                parts = lines.strip().split("-")
            if len(parts) == 2:
                indices = int(parts[0])
                dados.append(indices)