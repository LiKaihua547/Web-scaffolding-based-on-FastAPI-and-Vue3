def success( msg="success",data=None):
    return {"code": 200, "msg": msg, "data": data}
def error(code=500,msg="error"):
    return {"code": code, "msg": msg}
