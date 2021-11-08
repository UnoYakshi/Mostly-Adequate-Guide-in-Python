from src.support import curry, prop


def test_curry():

    def some_method(*args):
        if not args:
            return 0.0
        return sum(args) / len(args)

    # TODO: Refactor it...

    new_nethod_1 = curry(some_method)
    new_nethod_2 = new_nethod_1(14, 12)
    new_nethod_3 = new_nethod_2(14, 16)
    assert new_nethod_3() == 14.0

    new_method_4 = curry(some_method)
    assert new_method_4(4, 4)(4)() == 4.0


def test_prop():
    class TestClass:
        test_field = 'test_field_value'

    test_class_inst = TestClass()

    actual_value = prop('test_field')
    assert actual_value(test_class_inst) == 'test_field_value'
