
def chunk_iter(iterable, n):
    """Yields an iterator in chunks

    For example you can do

    for a, b in chunk_iter([1, 2, 3, 4, 5, 6], 2):
        print '{0} {1}'.format(a, b)

    # Prints
    # 1 2
    # 3 4
    # 5 6

    Args:
        iterable - Some iterable
        n - Chunk size (must be greater than 0)
    """
    assert n > 0
    iterable = iter(iterable)
    while True:
        chunk = tuple([iterable.next() for _ in xrange(n)])
        yield chunk
