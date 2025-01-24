import json

def string_to_json(input_data):
    # Проверяем, является ли input_data уже JSON-объектом
    if isinstance(input_data, (dict, list)):
        return input_data
    try:
        # Преобразуем строку в JSON
        json_object = json.loads(input_data)
        return json_object
    except (json.JSONDecodeError, TypeError) as e:
        return f"Ошибка декодирования JSON: {e}"