import math


def calcula_area(area, percentual_folga_area):
	if area < 0:
		raise ValueError("Área deve ser um valor não negativo")
	return area * (1+((percentual_folga_area)/100))


def calcula_litros(area_com_folga, cobertura_tinta):
	if cobertura_tinta <= 0:
		raise ValueError("Cobertura de tinta deve ser um valor positivo")
	if area_com_folga < 0:
		raise ValueError("Área com folga deve ser um valor não negativo")
	return area_com_folga/cobertura_tinta


def calcula_so_latas(litros_para_pintar_area, litros_lata_de_tinta, preco_lata):
	numero_de_so_latas = math.ceil(litros_para_pintar_area/litros_lata_de_tinta)
	gasto_com_so_latas = numero_de_so_latas * preco_lata
	print("Gasto com somente latas =", numero_de_so_latas, "latas de 3,6L, seu custo será de R$ ", gasto_com_so_latas)
	return numero_de_so_latas, gasto_com_so_latas


def calcula_so_galoes(litros_para_pintar_area, litros_galao_de_tinta, preco_galao):
	numero_de_so_galoes = math.ceil(litros_para_pintar_area/litros_galao_de_tinta)
	gasto_com_so_galoes = numero_de_so_galoes * preco_galao
	print("Gasto com somente galões =", numero_de_so_galoes, "galões de 18L, seu custo será de R$ ", gasto_com_so_galoes)
	return numero_de_so_galoes, gasto_com_so_galoes


def calcula_otimizado(litros_para_pintar_area, litros_galao_de_tinta, preco_galao, litros_lata_de_tinta, preco_lata):
	numero_de_galoes = math.floor(litros_para_pintar_area/litros_galao_de_tinta)
	gasto_com_galoes = numero_de_galoes * preco_galao
	litros_resto = litros_para_pintar_area % litros_galao_de_tinta
	if litros_resto > 3*litros_lata_de_tinta:
		numero_de_galoes = math.ceil(litros_para_pintar_area/litros_galao_de_tinta)
		gasto_com_galoes = numero_de_galoes * preco_galao
		print("Gasto otimizado = ", numero_de_galoes, "galões de 18L, seu custo será de R$ ", gasto_com_galoes)
		return numero_de_galoes, gasto_com_galoes
	else:
		numero_de_latas = math.ceil(litros_resto / litros_lata_de_tinta)
		gasto_com_latas = numero_de_latas * preco_lata
		gasto_total = gasto_com_latas + gasto_com_galoes
		print("Gasto otimizado = {} galão(ões) de 18L e {} lata(s) de 3,6L e seu custo será de R${}".format(numero_de_galoes, numero_de_latas, gasto_total))
		return numero_de_galoes, numero_de_latas, gasto_total
