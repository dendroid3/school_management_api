# api/items.py

import json
import database
from urllib.parse import parse_qs

def handler(event, context):
    method = event.get('httpMethod')
    path = event.get('path')
    body = event.get('body', '')

    if method == 'GET' and path == '/items':
        return get_items()
    elif method == 'POST' and path == '/add_item':
        return add_item(body)
    else:
        return {'statusCode': 404, 'body': 'Not Found'}

def get_items():
    with database.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM items')
        items = cursor.fetchall()
    return {'statusCode': 200, 'body': json.dumps(items)}

def add_item(body):
    data = parse_qs(body)
    name = data.get('name', [''])[0]
    if name:
        with database.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO items (name) VALUES (?)', (name,))
            conn.commit()
        return {'statusCode': 200, 'body': 'Item added'}
    else:
        return {'statusCode': 400, 'body': 'Bad Request'}
