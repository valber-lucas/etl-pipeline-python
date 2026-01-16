import unittest
from etl_processor import transform_data

class TestETLPipeline(unittest.TestCase):

    def test_transform_data_valid_row(self):
        raw_row = {
            "transaction_id": "1",
            "product": "Mouse",
            "quantity": "2",
            "price": "50.00",
            "status": "Aprovado"
        }
        
        result = transform_data(raw_row)
        
        self.assertIsNotNone(result)
        self.assertEqual(result[0], 1)
        self.assertEqual(result[1], "MOUSE")
        self.assertEqual(result[2], 100.0)
        self.assertEqual(result[3], "Aprovado")

    def test_transform_data_invalid_price(self):
        raw_row = {
            "transaction_id": "2",
            "product": "Teclado",
            "quantity": "1",
            "price": "invalid_price",
            "status": "Pendente"
        }
        
        result = transform_data(raw_row)
        self.assertIsNone(result)

    def test_transform_data_negative_quantity(self):
        raw_row = {
            "transaction_id": "3",
            "product": "Webcam",
            "quantity": "-1",
            "price": "100.00",
            "status": "Cancelado"
        }
        
        result = transform_data(raw_row)
        self.assertEqual(result[2], -100.0)

if __name__ == "__main__":
    unittest.main()