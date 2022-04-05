import json

def is_logged_in(request):
    return request.cookies.get('user') is not None

def get_user(request):
    cookie = request.cookies.get('user')
    if cookie is not None: 
        return json.loads(cookie)
    return None

def jsonify_user(u):
    return json.dumps({
        "Email": u.Email,
        "UserID": u.UserID,
        "FirstName": u.FirstName,
        "LastName": u.LastName
    })

def get_response_with_user_cookie(response, user):
    if user is not None:
        response.set_cookie('user', jsonify_user(user))
    return response
