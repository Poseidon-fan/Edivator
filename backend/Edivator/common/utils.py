from rest_framework.response import Response


def has_permission_for_document(user, document):
    return ((document.owner == 1 and document.user.id == user.id) or
                (document.owner == 2 and document.team.users.filter(id=user.id).exists()) or
                (document.owner == 3 and document.company.users.filter(id=user.id).exists()))


# 检测参数是否全
def check_is_all(params):
    for param in params:
        if param is None:
            return False
    return True
