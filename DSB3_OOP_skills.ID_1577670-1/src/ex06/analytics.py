import os
import logging
import requests
import json
from random import randint

# Настройка логирования
logging.basicConfig(
    filename='analytics.log',
    level=logging.DEBUG,
    format='%(asctime)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

class Research:
    def __init__(self, file_path):
        self.file_path = file_path
        logging.info(f"Research class initialized with file path: {file_path}")
    
    def file_reader(self, has_header=True):
        logging.info("Starting file reading process")
        if not os.path.exists(self.file_path):
            error_msg = "File not found"
            logging.error(error_msg)
            raise Exception(error_msg)
        
        with open(self.file_path, 'r') as file:
            lines = file.readlines()
            
        if len(lines) < 1:
            error_msg = "File is empty"
            logging.error(error_msg)
            raise Exception(error_msg)
            
        result = []
        start_index = 1 if has_header else 0
        
        for i in range(start_index, len(lines)):
            line = lines[i].strip()
            if line:
                values = line.split(',')
                if len(values) != 2:
                    error_msg = f"Invalid data format on line {i+1}"
                    logging.error(error_msg)
                    raise Exception(error_msg)
                if values[0] not in ['0', '1'] or values[1] not in ['0', '1']:
                    error_msg = f"Invalid values on line {i+1}"
                    logging.error(error_msg)
                    raise Exception(error_msg)
                if values[0] == values[1]:
                    error_msg = f"Both values are same on line {i+1}"
                    logging.error(error_msg)
                    raise Exception(error_msg)
                result.append([int(values[0]), int(values[1])])
        
        logging.info(f"Successfully read {len(result)} data points from file")
        return result
    
    def send_telegram_message(self, success=True):
        logging.info("Attempting to send Telegram message")
        try:
            import config
            
            if success:
                message = "The report has been successfully created"
            else:
                message = "The report hasn't been created due to an error"
            
            payload = {
                'chat_id': config.telegram_chat_id,
                'text': message
            }
            
            # Для тестирования используем вывод в консоль
            # В реальной реализации раскомментировать строку ниже:
            # response = requests.post(config.telegram_webhook_url, data=payload)
            
            logging.info(f"Telegram message prepared: {message}")
            print(f"TELEGRAM MESSAGE: {message}")
            
        except Exception as e:
            logging.error(f"Failed to send Telegram message: {e}")
    
    class Calculations:
        def __init__(self, data):
            self.data = data
            logging.info("Calculations class initialized with data")
        
        def counts(self):
            logging.info("Calculating counts of heads and tails")
            heads = sum(pair[0] for pair in self.data)
            tails = sum(pair[1] for pair in self.data)
            logging.info(f"Counts calculated: heads={heads}, tails={tails}")
            return heads, tails
        
        def fractions(self, heads, tails):
            logging.info("Calculating fractions")
            total = heads + tails
            if total == 0:
                logging.warning("Total count is zero, returning zero fractions")
                return 0, 0
            head_fraction = heads / total
            tail_fraction = tails / total
            logging.info(f"Fractions calculated: heads={head_fraction:.4f}, tails={tail_fraction:.4f}")
            return head_fraction, tail_fraction

class Analytics(Research.Calculations):
    def __init__(self, data):
        super().__init__(data)
        logging.info("Analytics class initialized")
    
    def predict_random(self, num_predictions):
        logging.info(f"Generating {num_predictions} random predictions")
        predictions = []
        for _ in range(num_predictions):
            prediction = randint(0, 1)
            if prediction == 1:
                predictions.append([1, 0])
            else:
                predictions.append([0, 1])
        logging.info(f"Generated {len(predictions)} random predictions")
        return predictions
    
    def predict_last(self, research_instance):
        logging.info("Getting last prediction from data")
        data = research_instance.file_reader()
        last_pred = data[-1] if data else None
        logging.info(f"Last prediction: {last_pred}")
        return last_pred
    
    def save_file(self, data, filename, extension):
        logging.info(f"Saving file {filename}.{extension}")
        full_filename = f"{filename}.{extension}"
        try:
            with open(full_filename, 'w') as file:
                file.write(data)
            logging.info(f"File {full_filename} saved successfully")
        except Exception as e:
            logging.error(f"Failed to save file {full_filename}: {e}")
            raise