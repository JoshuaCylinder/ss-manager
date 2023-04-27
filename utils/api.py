from utils.manager import add_user, del_user, list_users, get_sub


def api_handler(data):
    if data.startswith("add") and ":" in data:
        # add user
        add_user(int(data.split(":")[1]))
        return "ok"
    elif data == "list":
        return list_users()
    elif data.startswith("del"):
        del_user(int(data.split(":")[1]))
        return "ok"
    elif data.startswith("sub"):
        return get_sub(int(data.split(":")[1]))
    else:
        return ""
