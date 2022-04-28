from flask import render_template, redirect
from .utils import get_user, is_logged_in, is_admin

def get_groups(request, db):
    if not is_logged_in(request):
        return redirect("/login", code=302)
    
    user_cookie = get_user(request)
    user_id = user_cookie['UserID']

    grps = db.engine.execute(f"SELECT * FROM (SELECT * FROM `groupassignment` WHERE UserID = {user_id}) tmp NATURAL JOIN `group`;")

    user_groups = []
    for g in grps:
        entry = {}
        entry['name'] = g.GroupName
        entry['users'] = db.engine.execute(f"SELECT u.FirstName, u.LastName, u.Email FROM (SELECT * FROM `groupassignment` WHERE GroupID = {g.GroupID}) tmp NATURAL JOIN `user` u WHERE u.UserID != {user_id};")
        user_groups.append(entry)

    return render_template("groups.html", user_groups=user_groups, logged_in=is_logged_in(request), route='groups', is_admin=is_admin(request))

def join_group_get(request, db):
    if not is_logged_in(request):
        return redirect("/login", code=302)

def join_group_post(request, db):
    pass
