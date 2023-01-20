"""
Allows early returning of `exec()`, use `Exec` over `exec` function
"""

class ExecInterrupt(Exception):
    pass


def Exec(source, globals = None, locals = None):
    try:
        exec(source, globals, locals)
    except ExecInterrupt:
        pass