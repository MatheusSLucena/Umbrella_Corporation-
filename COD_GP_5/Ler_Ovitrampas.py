import geopandas as gpd


#Lê a pasta do shapefile de ovitrampas
ovitrampas_26_1 = gpd.read_file("Dados_extraidos/ATUALIZAÇÃO TOTAL DAS OVITRAMPAS 2026 shapefile/DS 1")
ovitrampas_26_2 = gpd.read_file("Dados_extraidos/ATUALIZAÇÃO TOTAL DAS OVITRAMPAS 2026 shapefile/DS 2")
ovitrampas_26_3= gpd.read_file("Dados_extraidos/ATUALIZAÇÃO TOTAL DAS OVITRAMPAS 2026 shapefile/DS 3")
ovitrampas_26_4 = gpd.read_file("Dados_extraidos/ATUALIZAÇÃO TOTAL DAS OVITRAMPAS 2026 shapefile/DS 4")
ovitrampas_26_5 = gpd.read_file("Dados_extraidos/ATUALIZAÇÃO TOTAL DAS OVITRAMPAS 2026 shapefile/DS 5")
ovitrampas_26_6 = gpd.read_file("Dados_extraidos/ATUALIZAÇÃO TOTAL DAS OVITRAMPAS 2026 shapefile/DS 6")
ovitrampas_26_7 = gpd.read_file("Dados_extraidos/ATUALIZAÇÃO TOTAL DAS OVITRAMPAS 2026 shapefile/DS 7")
ovitrampas_26_8 = gpd.read_file("Dados_extraidos/ATUALIZAÇÃO TOTAL DAS OVITRAMPAS 2026 shapefile/DS 8")

#Mostra as 5 primeiras linhas da tabela de Dados
print(ovitrampas_26_1)
print(ovitrampas_26_2)
print(ovitrampas_26_3)
print(ovitrampas_26_4)
print(ovitrampas_26_5)
print(ovitrampas_26_6)
print(ovitrampas_26_7)
print(ovitrampas_26_8)
#Mostra quais colunas (informações) existem

print(ovitrampas_26_1.columns)
print(ovitrampas_26_2.columns)
print(ovitrampas_26_3.columns)
print(ovitrampas_26_4.columns)
print(ovitrampas_26_5.columns)
print(ovitrampas_26_6.columns)
print(ovitrampas_26_7.columns)
print(ovitrampas_26_8.columns)









