import os 

for pasta_atual, subpasta, arquivos in os.walk("Dados_extraidos"):
    for name_arquivo in arquivos:
        print(os.path.join(pasta_atual,name_arquivo))