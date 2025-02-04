import cv2 # type: ignore
from qreader import QReader #type: ignore
import asyncio
import json
from datetime import datetime, timedelta

class QRCodeService:
    def __new__(cls):
        cls._self = None
        if cls._self is None:
            cls._self = super().__new__(cls)
        return cls._self
    def __init__(self):
        self.cam = cv2.VideoCapture(0)
        print("Camera initialized")
        self.qr = QReader(model_size='l', min_confidence=0.3)


    async def read_qr_code(self,expected_medication: dict):
        while True:
            ret, img = self.cam.read()
            if ret:
                rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                data = self.qr.detect_and_decode(rgb_img)
                if data and data[0] is not None:
                    #print(f"QR Code detected: {data}")
                    break
            await asyncio.sleep(2)  # non-blocking sleep

        qr_data = json.loads(data[0])
        print(f"QR Code data: {qr_data}")

        if qr_data['Nome'] != expected_medication['Nome']:
            return 'Medicamento incorreto', [qr_data['Nome'],qr_data['Dose'],qr_data['Data de validade'],qr_data['Lote'],qr_data['Fornecedor']]
        expiration_date_str = qr_data.get("Data de validade")

        if qr_data.get('Dosagem') != expected_medication.get('Dosagem'):
            return 'Dosagem incorreta', [qr_data['Nome'],qr_data['Dose'],qr_data['Data de validade'],qr_data['Lote'],qr_data['Fornecedor']]

        try:
            expiration_date = datetime.strptime(expiration_date_str, "%d/%m/%Y")
        except ValueError as e:
            print(f"Error parsing date: {e}")
            return 'Erro de formatação da data de validade', [qr_data['Nome'],qr_data['Dose'],qr_data['Data de validade'],qr_data['Lote'],qr_data['Fornecedor']]

        current_date = datetime.now()
        six_months_ahead = current_date + timedelta(days=6*30)

        # Compare the expiration date to the current date
        if expiration_date < current_date:
            # Medication is expired
            return 'Medicamento correto, mas expirado', [qr_data['Nome'],qr_data['Dose'],qr_data['Data de validade'],qr_data['Lote'],qr_data['Fornecedor']]
        elif expiration_date < six_months_ahead:
            # Medication is close to expiration
            return 'Medicamento correto, mas próximo da data de validade', [qr_data['Nome'],qr_data['Dose'],qr_data['Data de validade'],qr_data['Lote'],qr_data['Fornecedor']]
        else:
            # Medication is valid
            return 'Medicamento correto e válido', [qr_data['Nome'],qr_data['Dose'],qr_data['Data de validade'],qr_data['Lote'],qr_data['Fornecedor']]

        

            

