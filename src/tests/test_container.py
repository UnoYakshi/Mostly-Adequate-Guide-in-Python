from src.container import Container
from src.support import prop


LAMBDAS = {
        2: lambda x: x**3,
        'test': lambda x: x.upper(),
        'blow me': lambda x: x + ' away',
        '12345': prop('__len__')
    }


def test_map():

    for val, method in LAMBDAS.items():
        cont = Container.of(val)
        mapped_cont = cont.map(method)
        print(f'{val} ==> {mapped_cont.value}')

    # TODO: Do something about executable Container.value...
    get_len = prop('__len__')

    new_container = Container.of(['123', '123456'])
    data = new_container.map(get_len)
    assert data.value() == 2
