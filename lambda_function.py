import json
import boto3

table_name = "devhouse"
client  = boto3.resource('dynamodb')
table   = client.Table(table_name)


def read(new_data):
    id = int(new_data['ID'])
    response = table.scan()
    people = response['Items']
    print(people)
    for person in people:
        if person['ID'] == id:
            print(person)
            return person
    return False

def write(new_data):
    new_id = int(new_data['ID'])
    if read({'ID':new_id}) == False:
        new_data['ID'] = int(new_data['ID'])
        print(new_data)
        table.put_item(Item= new_data)
    else:
        return False


def delete(new_data):
    id = int(new_data['ID'])
    old_data = read({'ID': id})
    print(old_data)
    if old_data:
        response = table.delete_item(Key={
            'ID': id
        })
        return True
    else:
        return False
        

def edit(new_data):
    id = new_data['ID']
    var = new_data['var']
    new_content = new_data['new_content']
    old_data = read({'ID': id})
    if old_data:
        new_data = old_data

        new_data[var] = new_content
        delete({'ID': id})
        table.put_item(Item= new_data)
        return True
    else:
        return False



def lambda_handler(event, context):
    # TODO implement
    # return event
    
    functions = {
        'write': write, 
        'read': read, 
        'edit': edit, 
        'delete': delete}
    params = {
        'rawPath': event['rawPath'],
        'func': event['rawPath'].split()[0].strip('/'),
        'data': event['queryStringParameters']
    }
    if params['func'] not in functions:
        return {
            'statusCode': 400,
            'event': event
        }
    else:
        new_data = params['data']
        return functions[params['func']](new_data)
        
    return event
    
    # return {
    #     'statusCode': 200,
    #     'body': json.dumps('Hello from Lambda!')
    
