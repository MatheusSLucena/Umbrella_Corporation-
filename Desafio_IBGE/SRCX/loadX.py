import json

class LoadX():
    def __initX__(self):
        pass
    def load_json(self, nome_doc, data):
        with open(f"{nome_doc}.json","w",encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False,indent=2)