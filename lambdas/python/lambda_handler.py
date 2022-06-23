import json


def create_response(status_code, body):
    response = {
        "statusCode": status_code,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Credentials": True,
        },
        "body": json.dumps(body),
        "isBase64Encoded": False,
    }

    return response


def handler(event, context):
    http_method = event["httpMethod"]

    if http_method == "GET":
        status_code = 200
        body = {"msg": "This is GET method"}
    elif http_method == "POST":
        status_code = 200
        body = {"msg": "This is POST method"}
    else:
        status_code = 400
        body = {"msg": f"{http_method} is not allowed"}

    return create_response(status_code, body)
