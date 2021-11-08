from src.container import IO


def test_method(x: int) -> float:
    return x / 2.0


def test_map():
    def mapping_method(x):
        return x * 2.0

    new_io = IO(test_method)
    new_io.map(mapping_method)
    print(new_io)


def test_ap():
    ...


def test_chain():
    ...


def test_join():
    ...
