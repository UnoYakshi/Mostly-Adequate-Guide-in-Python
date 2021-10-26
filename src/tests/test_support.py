from src.support import curry, prop


def test_curry():

    def some_method(*args):
        # if not args:
        #     return 0.0
        return sum(args) / len(args)

    # TODO: Refactor it...

    new_nethod_1 = curry(some_method)

    new_nethod_1(14, 12)
    new_nethod_1(14, 16)
    assert new_nethod_1() == 14.0

    new_nethod_2 = curry(some_method)
    new_nethod_2(2, 4)
    new_nethod_2(6)
    new_nethod_2(8)
    new_nethod_2(40)
    assert new_nethod_2() == 12.0

    new_nethod_3 = curry(some_method)
    assert new_nethod_3(2, 4, 6, 8, 40) == 12.0


def test_prop():
    class TestClass:
        test_field = 'test_field_value'

    test_class_inst = TestClass()

    actual_value = prop('test_field')
    assert actual_value(test_class_inst) == 'test_field_value'
