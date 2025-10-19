import boto3

def lambda_handler(event, context):
    # Entrada (json)
    tenant_id = event['tenant_id']
    alumno_id = event['alumno_id']
    # Proceso
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('t_alumnos')
    response = table.get_item(
        Key={
            'tenant_id': tenant_id,
            'alumno_id': alumno_id
        }
    )
    # Salida (json)
    return {
        'statusCode': 200,
        'response': response
    }
