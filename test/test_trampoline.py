from pytest import fail, raises

from trampoline import tramp, tail, pull, tail_call

NFAIL = 100000

def test_fib_no_trampoline():
    """This test establishes the baseline behavior of
    Python with a function implemented in a manner that
    would not experience problems if Python implemented
    proper tail calls.  The baseline behavior is the fail
    with a `RecursionError`.
    """
    def fib(n):
        def recur(m, a, b):
            if m >= n:
                return b
            else:
                return recur(m+1, b, a+b)
        return recur(0, 0, 1)
    with raises(RecursionError):
        fib(NFAIL)

def test_fib_with_decorators():
    """This test check the behavior against the baseline behavior
    for the same function implemented using trampoline decorators.
    The behavior with the trampoline is to not experience a
    `RecursionError` because the stack is not being built out.
    """
    @tramp
    def fib(n):
        @tail
        def recur(m, a, b):
            if m >= n:
                return b
            else:
                return recur(m+1, b, a+b)
        return recur(0, 0, 1)

    try:
        fib(NFAIL)
    except RecursionError:
        fail(reason="A recursion error was raised indicating the trampoline did not work")


def test_fib_with_tail_call_function():
    """This test check the behavior against the baseline behavior
    for the same function implemented the `pull` and `tail_call`
    functions, rather than decorators.
    """
    def fib(n):
        def recur(m, a, b):
            if m >= n:
                return b
            else:
                return tail_call(recur, m+1, b, a+b)
        return pull(recur(0, 0, 1))

    try:
        fib(NFAIL)
    except RecursionError:
        fail(reason="A recursion error was raised indicating the trampoline did not work")



def test_mutual_recursion_no_trampoline():
    """This test establishes the baseline behavior for mututally recursive
    functions with recursion in the tail position. The baseline behavior is
    to fail with a `RecursionError`.
    """

    def even(x):
        return even_recur(x)

    def even_recur(x):
        if x == 0:
            return True
        else:
            return odd_recur(x - 1)

    def odd(x):
        return odd_recur(x)

    def odd_recur(x):
        if x == 0:
            return False
        else:
            return even_recur(x - 1)

    with raises(RecursionError):
        even(NFAIL)

    with raises(RecursionError):
        odd(NFAIL)

def test_mutual_recursion_with_trampoline_decoractors():
    """This test check the behavior against the baseline behavior
    for the same mutually recursive functions implemented using
    trampoline decorators. The behavior with the trampoline is to
    not experience a `RecursionError` because the stack is not being
    built out.
    """
    @tramp
    def even(x):
        return even_recur(x)

    @tail
    def even_recur(x):
        if x == 0:
            return True
        else:
            return odd_recur(x - 1)

    @tramp
    def odd(x):
        return odd_recur(x)

    @tail
    def odd_recur(x):
        if x == 0:
            return False
        else:
            return even_recur(x - 1)

    try:
        even(NFAIL)
    except RecursionError:
        fail(reason="A recursion error was raised indicating the trampoline did not work")

    try:
        odd(NFAIL)
    except RecursionError:
        fail(reason="A recursion error was raised indicating the trampoline did not work")


def test_mutual_recursion_with_pull_and_tail_call_functions():
    """This test check the behavior against the baseline behavior
    for the same mutually recursive functions implemented with the
    `pull` and `tail_call` functions, rather than decorators.
    """
    def even(x):
        return pull(even_recur(x))

    def even_recur(x):
        if x == 0:
            return True
        else:
            return tail_call(odd_recur, x - 1)

    def odd(x):
        return pull(odd_recur(x))

    def odd_recur(x):
        if x == 0:
            return False
        else:
            return tail_call(even_recur, x - 1)

    try:
        even(NFAIL)
    except RecursionError:
        fail(reason="A recursion error was raised indicating the trampoline did not work")

    try:
        odd(NFAIL)
    except RecursionError:
        fail(reason="A recursion error was raised indicating the trampoline did not work")
