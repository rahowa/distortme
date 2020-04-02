import typer
from functools import wraps


def print_delimiter(op_name, up_symbol='=', down_symbol='='):
    def delimiter(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if up_symbol is not None:
                typer.echo(up_symbol * 80)
            typer.echo(op_name)
            f(*args, **kwargs)
            if down_symbol is not None:
                typer.echo(down_symbol * 80)
        return wrapper
    return delimiter