import boto3
import json

def lambda_handler(event, context):
    try:
        # Manejar diferentes tipos de eventos
        if 'body' in event:
            if isinstance(event['body'], str):
                body = json.loads(event['body'])
            else:
                body = event['body']
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
        
        # Verificar si el alumno existe antes de modificar
        get_response = table.get_item(
            Key={'tenant_id': tenant_id, 'alumno_id': alumno_id}
        )
        
        if 'Item' not in get_response:
            return {
                'statusCode': 404,
                'body': json.dumps({'error': 'Alumno no encontrado'})
            }
        
        # Construir expresión de actualización dinámica
        update_expr = "SET "
        expr_values = {}
        
        # Campos que se pueden actualizar
        updatable_fields = ['nombres', 'apellidos', 'email', 'telefono', 'edad', 'carrera']
        
        for field in updatable_fields:
            if field in body:
                update_expr += f"{field} = :{field}, "
                expr_values[f":{field}"] = body[field]
        
        if not expr_values:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'No hay campos para actualizar'})
            }
        
        # Remover la última coma y espacio
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
