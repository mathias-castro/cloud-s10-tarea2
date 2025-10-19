import boto3
import json
from datetime import datetime

def lambda_handler(event, context):
    try:
        # Manejar tanto evento directo como API Gateway
        if 'body' in event and event['body']:
            body = json.loads(event['body'])
        else:
            body = event
        
        # Validar campos requeridos
        if 'tenant_id' not in body or 'alumno_id' not in body:
            return {
                'statusCode': 400,
                'body': json.dumps({
                    'error': 'tenant_id y alumno_id son requeridos'
                })
            }
        
        tenant_id = body['tenant_id']
        alumno_id = body['alumno_id']
        
        # Proceso
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('t_alumnos')
        
        # Verificar si existe antes de eliminar
        get_response = table.get_item(
            Key={
                'tenant_id': tenant_id,
                'alumno_id': alumno_id
            }
        )
        
        if 'Item' not in get_response:
            return {
                'statusCode': 404,
                'body': json.dumps({
                    'error': 'Alumno no encontrado'
                })
            }
        
        # Eliminar el item
        table.delete_item(
            Key={
                'tenant_id': tenant_id,
                'alumno_id': alumno_id
            }
        )
        
        # Salida (json)
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Alumno eliminado exitosamente'
            })
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e)
            })
        }
