import geopandas as gpd


#Lê a pasta do shapefile de ovitrampas
bds = gpd.read_file("Dados_extraidos/BASE Distritos Sanitários shapefile/")

#Mostra as 5 primeiras linhas da tabela de Dados
print(bds)

#Mostra quais colunas (informações) existem

print(bds)


