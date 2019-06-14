# 用于节耦的函数 用户用户登录成功后调用该函数在session中写入输入 需要传入参数request 和 username 可定制
def set_session(request, username):
    request.session['user_data'] = {"username": username}
