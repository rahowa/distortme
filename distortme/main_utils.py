import typer
from typing import Callable, List, Any, Dict
from functools import wraps


def print_delimiter(op_name: str, up_symbol: str = '=', down_symbol: str = '=') -> Callable:
    def delimiter(f: Callable) -> Callable:
        @wraps(f)
        def wrapper(*args: List[Any], **kwargs: Dict[str, Any]) -> None:
            if up_symbol is not None:
                typer.echo(f"[ {op_name} ]".center(80, up_symbol))
            else:
                typer.echo(op_name.center(80))
            f(*args, **kwargs)
            if down_symbol is not None:
                typer.echo("[ DONE ]".center(80, down_symbol))
            else:
                typer.echo("[ DONE ]".center(80))
        return wrapper
    return delimiter


def print_delimiter_async(op_name: str, up_symbol: str = '=', down_symbol: str = '=') -> Callable:
    def delimiter(f: Callable) -> Callable:
        @wraps(f)
        async def wrapper(*args: List[Any], **kwargs: Dict[str, Any]) -> None:
            if up_symbol is not None:
                typer.echo(f"[ {op_name} ]".center(80, up_symbol))
            else:
                typer.echo(op_name.center(80))
            await f(*args, **kwargs)
            if down_symbol is not None:
                typer.echo("[ DONE ]".center(80, down_symbol))
            else:
                typer.echo("[ DONE ]".center(80))
        return wrapper
    return delimiter


def not_implemented(f: Callable) -> Callable:
    @wraps(f)
    def wrapper(*args, **kwargs) -> None:
        warning = typer.style("WARNING".center(80), fg=typer.colors.GREEN, bg=typer.colors.RED, bold=True, blink=True)
        typer.echo(warning)
        typer.secho("This functionality is not fully implemented yet. Updates soon.".center(80), fg=typer.colors.RED)
        f(*args, **kwargs)
    return wrapper
