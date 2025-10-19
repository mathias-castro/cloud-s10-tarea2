import boto3
import json

def lambda_handler(event, context):
    try:
        if 'body' in event and event['body']:
            body = json.loads(event['body'])
        else:
            body = event
        
        tenant_id = body.get('tenant_id')
        alumno_id = body.get('alumno_id')
        
        if not tenant_id or not alumno_id:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'tenant_id y alumno_id son requeridos'})
            }
        
        # Proceso
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('t_alumnos')
        response = table.get_item(
            Key={'tenant_id': tenant_id, 'alumno_id': alumno_id}
        )
        
        if 'Item' not in response:
            return {
                'statusCode': 404,
                'body': json.dumps({'error': 'Alumno no encontrado'})
            }
        
        return {
            'statusCode': 200,
            'body': json.dumps({'alumno': response['Item']})
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
