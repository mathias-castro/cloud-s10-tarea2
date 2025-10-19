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
        
        # Construir actualización dinámica
        update_expr = "SET "
        expr_values = {}
        
        for key, value in body.items():
            if key not in ['tenant_id', 'alumno_id']:
                update_expr += f"{key} = :{key}, "
                expr_values[f":{key}"] = value
        
        update_expr = update_expr.rstrip(', ')
        
        response = table.update_item(
            Key={'tenant_id': tenant_id, 'alumno_id': alumno_id},
            UpdateExpression=update_expr,
            ExpressionAttributeValues=expr_values,
            ReturnValues='ALL_NEW'
        )
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Alumno modificado exitosamente',
                'alumno': response['Attributes']
            })
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
