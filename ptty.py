"""
A simple Python terminal that features dot-completion.
"""

import traceback


def __loop(x, y):
    """
    Easy way to iterate over two ranges at once.

    Args:
        x(int): outer range.
        y(int): inner range.

    Yields:
        A tuple containing each element within the iteration.
    """
    for a in range(x):
        for b in range(y):
            yield a, b

def print_columns(obj, cols=4, pad=24):
    """
    Prints any iterable object that supports __len__ and __iter__.

    Args:
        obj(iterable): any iterable object that supports __len__.
        cols(int): the number of columns of output.
        pad(int): the amount of whitespace to use for left-justifying elements.
    """
    items = iter(obj)
    for _, c in __loop(len(obj), cols):
        if not items.__length_hint__(): break
        print(str(next(items)).ljust(pad), end='')
        if c == cols - 1: print()
    print()


def term(globs=globals(), locs=locals()):
    """
    A simple but powerful terminal for Python.

    Meant to be imported and used inline:

    >>> def foo():
    ...     a = 3
    ...     import pyterm; pyterm.term()
    ...     print(a)

    In situations where exceptions are used as a means of complex flow control
    (i.e. Pytest), being able to quickly import a funcional terminal is very
    convenient.

    To print out dot-completion information, type any valid name followed by a
    period character ('.') and hit <enter>. This will print out the member
    methods and fields for that object.

    Args:
        globs(dict): what is to be considered the global evaluation environment
        locs(dict): what is to be considered the local evaluation environment

    Returns:
        A dict containing any names that were defined during the execution of
        the loop such as variables, functions, and classes. Effectively equals
        the `locs` argument after modification within the loop.
    """

    print('PyTerm v0.1.0')
    print('Portable mini-interpreter for convenience and debugging')
    print('Type quit() or exit() to stop interpreting')

    if locs == globals():
        print('Note: Variables defined here will persist and be returned at exit')
    else:
        print('Note: Variables defined here will be returned at exit')
    
    def __stop():
        "Mini function for making sure quit() in terminal doesn't quit Python."
        nonlocal running; running = False

    tmp_exit = exit; globs['exit'] = __stop
    tmp_quit = quit; globs['quit'] = __stop

    running = prompt = '>>> '
    buf = ''

    while running:
        text = input(prompt)
        if not text and not buf: continue

        try:
            try:
                # Expressions should be immediately evaluated if possible
                prompt = '>>> '
                out = eval(buf + text, globs, locs)
                buf = ''

                # Print values that evaulate to False (but not null values)
                if out is not None: print(out)

            except SyntaxError:
                # Tab Completion
                if text.endswith('.'):
                    lookup = text[:-1]
                    print_columns(dir(eval(lookup, globs, locs)))

                # Multiline Code
                else:
                    # Evaluate if the last line entered is blank
                    if not text:
                        prompt = '>>> '
                        exec(buf + text, globs, locs)
                        buf = ''

                    # Continue adding lines
                    else:
                        prompt = '... '
                        buf += '\n' + text

        # When an actual exception occurs, clear the buffer
        except:
            print(traceback.format_exc())
            buf = ''

    # Restore exit functions to not mess up outer scope
    globs['exit'] = tmp_exit
    globs['quit'] = tmp_quit

    # Return the environment that was created during execution
    return locs


if __name__ == '__main__':
    term()
else:
	# Allow this module to be callable
	import sys
	sys.modules[__name__] = term
