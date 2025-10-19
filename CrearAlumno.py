import boto3

def lambda_handler(event, context):
    # Entrada (json)
    tenant_id = event['tenant_id']
    alumno_id = event['alumno_id']
    alumno_datos = event['alumno_datos']
    # Proceso
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('t_alumnos')
    alumno = {
        'tenant_id': tenant_id,
        'alumno_id': alumno_id,
        'alumno_datos': alumno_datos
    }
    response = table.put_item(Item=alumno)
    # Salida (json)
    return {
        'statusCode': 200,
        'response': response
    }
