'''
Programa que calcula e otimiza o custo para pintar uma dada area,
Retorna 3 opções de compra: Somente latas, Somente galões e Compra otimizada por valor
'''
from CalculaTinta import *
area_a_ser_pintada = float( input("Informe a area a ser pintada em metros quadrados (xxx.xx) = "))#area a ser pintada em metros quadrados
percentual_folga = 10
litros_galao_de_tinta = 18
litros_lata_de_tinta  = 3.6
preco_galao = 80.00
preco_lata = 25.00
cobertura_tinta = 6 #area que um litro de tinta cobre

area_com_folga = calcula_area(area_a_ser_pintada, percentual_folga)
litros_para_pintar_area = calcula_litros(area_com_folga, cobertura_tinta)
calcula_so_latas(litros_para_pintar_area, litros_lata_de_tinta, preco_lata)
calcula_so_galoes(litros_para_pintar_area, litros_galao_de_tinta, preco_galao)
calcula_otimizado(litros_para_pintar_area, litros_galao_de_tinta, preco_galao, litros_lata_de_tinta, preco_lata)

