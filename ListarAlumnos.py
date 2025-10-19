import boto3
import json
from boto3.dynamodb.conditions import Key

def lambda_handler(event, context):
    try:
        # Manejar API Gateway
        if 'body' in event and event['body']:
            body = json.loads(event['body'])
        else:
            body = event
        
        tenant_id = body.get('tenant_id')
        if not tenant_id:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'tenant_id es requerido'})
            }
        
        # Proceso
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('t_alumnos')
        response = table.query(
            KeyConditionExpression=Key('tenant_id').eq(tenant_id)
        )
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'tenant_id': tenant_id,
                'num_reg': response['Count'],
                'alumnos': response['Items']
            })
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
