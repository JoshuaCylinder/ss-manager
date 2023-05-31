from ss_manager import settings
from ss_manager.utils.manager import add_user, del_user, list_users, get_sub, reset as reset_origin
from ss_manager.utils.exceptions import ConflictPortException, UserNotFoundError
from ss_manager.utils.transporter import TCPTransporter


def _add(name, port, password, traffic):
    add_user(name, int(port), password, int(traffic))


def _list_all():
    return list_users()


def _reset():
    return reset_origin()


def _delete(name):
    del_user(name)


def _sub(name):
    return get_sub(name)


def _handler(data):
    method_name, args = data.split(":")[0], data.split(":")[1:]
    try:
        return globals()["_" + method_name](*args) or "ok"
    except UserNotFoundError as e:
        return f"User named {e.args[0]} does not exist."
    except ConflictPortException as e:
        return f"Port {e.args[0]} has been used."


def handler():
    TCPTransporter(settings.api_address, settings.key).recv(_handler)


def __getattr__(name):
    def sender(*args):
        data = f"{name}" + (f":{':'.join(args)}" if args else "")
        return TCPTransporter(settings.api_address, settings.key).send(data)
    return sender
