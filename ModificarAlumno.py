import boto3

def lambda_handler(event, context):
    # Entrada (json)
    tenant_id = event['tenant_id']
    alumno_id = event['alumno_id']
    alumno_datos = event['alumno_datos']
    # Proceso
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('t_alumnos')
    response = table.update_item(
        Key={
            'tenant_id': tenant_id,
            'alumno_id': alumno_id
        },
        UpdateExpression="set alumno_datos=:alumno_datos",
        ExpressionAttributeValues={
            ':alumno_datos': alumno_datos
        },
        ReturnValues="UPDATED_NEW"
    )
    # Salida (json)
    return {
        'statusCode': 200,
        'response': response
    }
