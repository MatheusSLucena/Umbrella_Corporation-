import xml.etree.ElementTree as ET
arvore_1 = ET.parse("Dados_extraidos/BASE Distritos sanitários shapefile/Distrito_Sanitário 24-09-14.shp.xml")
raiz_1 = arvore_1.getroot()

print("\n 1:",ET.tostring(raiz_1, encoding="unicode"))

arvore_2 = ET.parse("Dados_extraidos/BASE Distritos sanitários shapefile/DSI.shp.xml")
raiz_2 = arvore_2.getroot()

print(" \n 2:",ET.tostring(raiz_2, encoding="unicode"))

arvore_3 = ET.parse("Dados_extraidos/BASE Distritos sanitários shapefile/DSII.shp.xml")
raiz_3 = arvore_3.getroot()

print("\n 3:", ET.tostring(raiz_3, encoding="unicode"))

arvore_4 = ET.parse("Dados_extraidos/BASE Distritos sanitários shapefile/DSII.shp.xml")
raiz_4 = arvore_4.getroot()

print("\n 4:", ET.tostring(raiz_4, encoding="unicode"))

arvore_5 = ET.parse("Dados_extraidos/BASE Distritos sanitários shapefile/DSIV.shp.xml")
raiz_5 = arvore_5.getroot()

print("\n 5:", ET.tostring(raiz_5, encoding="unicode"))

arvore_6 = ET.parse("Dados_extraidos/BASE Distritos sanitários shapefile/DSV.shp.xml")
raiz_6 = arvore_6.getroot()

print("\n 6:", ET.tostring(raiz_6, encoding="unicode"))

arvore_7 = ET.parse("Dados_extraidos/BASE Distritos sanitários shapefile/DSVI.shp.xml")
raiz_7 = arvore_7.getroot()

print("\n 7:", ET.tostring(raiz_7, encoding="unicode"))

arvore_8 = ET.parse("Dados_extraidos/BASE Distritos sanitários shapefile/DSVII.shp.xml")
raiz_8 = arvore_8.getroot()

print("\n 8:", ET.tostring(raiz_8, encoding="unicode"))

arvore_9 =ET.parse("Dados_extraidos/BASE Distritos sanitários shapefile/DSVIII.shp.xml")
raiz_9 = arvore_9.getroot()

print("\n 9:", ET.tostring(raiz_9, encoding="unicode"))

