import boto3
import json

def lambda_handler(event, context):
    try:
        if 'body' in event:
            if isinstance(event['body'], str):
                body = json.loads(event['body'])
            else:
                body = event['body']
        else:
            body = event
        
        required = ['tenant_id', 'alumno_id', 'nombres', 'apellidos']
        for field in required:
            if field not in body:
                return {
                    'statusCode': 400,
                    'body': json.dumps({'error': f'{field} es requerido'})
                }
        
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('t_alumnos')
        table.put_item(Item=body)
        
        return {
            'statusCode': 201,
            'body': json.dumps({
                'message': 'Alumno creado exitosamente',
                'alumno': body
            })
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
