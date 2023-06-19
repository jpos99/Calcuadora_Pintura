import unittest
from CalculaTinta import calcula_area, calcula_litros


class TestCalculaArea(unittest.TestCase):

	def test_calcula_area(self):
		self.assertAlmostEqual(calcula_area(100, 10), 110, places=2)
		self.assertAlmostEqual(calcula_area(200, 20), 240, places=2)
		self.assertAlmostEqual(calcula_area(300, 30), 390, places=2)
		self.assertAlmostEqual(calcula_area(100, -10), 90, places=2)

	def test_area_negativa(self):
		with self.assertRaises(ValueError):
			calcula_area(-100, 10)


class TestCalculaLitros(unittest.TestCase):
	def test_calcula_litros(self):
		self.assertEqual(calcula_litros(100, 10), 10)
		self.assertEqual(calcula_litros(200, 20), 10)
		self.assertEqual(calcula_litros(300, 15), 20)
		self.assertAlmostEqual(calcula_litros(500, 30), 16.67, places=2)

	def test_cobertura_tinta_zero(self):
		with self.assertRaises(ValueError):
			calcula_litros(100, 0)

	def test_cobertura_tinta_negativa(self):
		with self.assertRaises(ValueError):
			calcula_litros(100, -10)

	def test_area_com_folga_negativa(self):
		with self.assertRaises(ValueError):
			calcula_litros(-100, 10)


if __name__ == '__main__':
	unittest.main()
