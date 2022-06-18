from rest_framework.response import Response


def return_success_response(data, token, message):
    return Response({
        "token": token,
        "data": data,
        "message": message,
        "status": 200,
        "isSuccess": True
    })


def return_failure_response(data, token, message):
    return Response({
        "token": token,
        "data": data,
        "message": message,
        "status": 500,
        "isSuccess": False
    })
