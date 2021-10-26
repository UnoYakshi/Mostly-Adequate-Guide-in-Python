from src.container import Container
from src.support import prop, curry


LAMBDAS = {
        2: lambda x: x**3,
        'test': lambda x: x.upper(),
        'blow me': lambda x: x + ' away',
        '12345': curry(lambda obj:  getattr(obj, '__len__'))
    }


def test_map():

    for val, method in LAMBDAS.items():
        cont = Container.of(val)
        mapped_cont = cont.map(method)
        print(f'{val} ==> {mapped_cont.value}')

    # TODO: Do something about executable Container.value...
    # mapped_cont = mapped_cont.map(prop('__len__'))
    print(mapped_cont.value())

    def cur_method(lval, rval):
        return lval * rval * 2
    sa = curry(cur_method)(3)
    sa = prop('__len__')

    new_container = Container.of([12])
    data = new_container.map(sa)
    print(data.value)
