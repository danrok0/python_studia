import json

def save_to_json(data, file_path):
    """
    Zapisuje dane do pliku JSON.
    """
    try:
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)
        print(f"Zapisano dane do {file_path}")
    except Exception as e:
        print(f"Błąd podczas zapisywania danych: {e}")
