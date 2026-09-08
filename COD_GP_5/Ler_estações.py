import geopandas as gpd


#Lê a pasta do shapefile de ovitrampas
estacao_1 = gpd.read_file("Dados_extraidos/ESTAÇÕES DISSEMINADORAS shapefile/DS 1")
estacao_2 = gpd.read_file("Dados_extraidos/ESTAÇÕES DISSEMINADORAS shapefile/DS 2")
estacao_3= gpd.read_file("Dados_extraidos/ESTAÇÕES DISSEMINADORAS shapefile/DS 3")
estacao_4 = gpd.read_file("Dados_extraidos/ESTAÇÕES DISSEMINADORAS shapefile/DS 4")
estacao_5 = gpd.read_file("Dados_extraidos/ESTAÇÕES DISSEMINADORAS shapefile/DS 5")
estacao_6 = gpd.read_file("Dados_extraidos/ESTAÇÕES DISSEMINADORAS shapefile/DS 6")
estacao_7 = gpd.read_file("Dados_extraidos/ESTAÇÕES DISSEMINADORAS shapefile/DS 7")
estacao_8 = gpd.read_file("Dados_extraidos/ESTAÇÕES DISSEMINADORAS shapefile/DS 8")

#Mostra as 5 primeiras linhas da tabela de Dados
print(estacao_1)
print(estacao_2)
print(estacao_3)
print(estacao_4)
print(estacao_5)
print(estacao_6)
print(estacao_7)
print(estacao_8)
#Mostra quais colunas (informações) existem

print(estacao_1.columns)
print(estacao_2.columns)
print(estacao_3.columns)
print(estacao_4.columns)
print(estacao_5.columns)
print(estacao_6.columns)
print(estacao_7.columns)
print(estacao_8.columns)



