import os
import unittest
from solution import generar_reporte_pdf

class TestGenerarReportePDF(unittest.TestCase):
    def setUp(self):
        self.test_pdf = "test_reporte_devsecops.pdf"
        self.datos_prueba = {
            "Análisis SAST": "Completado",
            "Vulnerabilidades Críticas": 0,
            "Dependencias Obsoletas": 2
        }
        
    def tearDown(self):
        if os.path.exists(self.test_pdf):
            try:
                os.remove(self.test_pdf)
            except OSError:
                pass

    def test_creacion_exitosa(self):
        # Caso de prueba principal: comprobar creación exitosa del reporte
        resultado = generar_reporte_pdf(self.datos_prueba, self.test_pdf)
        self.assertEqual(resultado, self.test_pdf)
        self.assertTrue(os.path.exists(self.test_pdf))
        self.assertGreater(os.path.getsize(self.test_pdf), 0)

    def test_tipo_datos_invalido(self):
        # Validar control y prevención de tipos de entrada incorrectos
        with self.assertRaises(TypeError):
            generar_reporte_pdf("datos invalidos", self.test_pdf)

    def test_ruta_absoluta_convertida(self):
        # Validar que si se pasa una ruta absoluta, se convierte a relativa por seguridad
        ruta_absoluta = os.path.join(os.getcwd(), "absoluto_reporte.pdf")
        resultado = generar_reporte_pdf(self.datos_prueba, ruta_absoluta)
        self.assertNotEqual(resultado, ruta_absoluta)
        nombre_esperado = os.path.basename(ruta_absoluta)
        self.assertEqual(resultado, nombre_esperado)
        self.assertTrue(os.path.exists(nombre_esperado))
        if os.path.exists(nombre_esperado):
            os.remove(nombre_esperado)
