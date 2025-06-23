import unittest
from solution import strict

class TestStrictDecorator(unittest.TestCase):

    def test_correct_types_positional(self):
        @strict
        def add(x: int, y: int) -> int:
            return x + y

        self.assertEqual(add(1, 2), 3)

    def test_correct_types_keyword(self):
        @strict
        def greet(name: str, age: int) -> str:
            return f"{name} is {age} years old"

        self.assertEqual(greet(name="Matvey", age=23), "Matvey is 23 years old")

    def test_type_mismatch_positional(self):
        @strict
        def multiply(a: int, b: int) -> int:
            return a * b

        with self.assertRaises(TypeError) as context:
            multiply(3, "4")  # str вместо int

        self.assertEqual(
            str(context.exception),
            "Argument 'b' must be of type int, got str"
        )

    def test_type_mismatch_keyword(self):
        @strict
        def welcome(name: str, active: bool) -> str:
            return f"{name}, active: {active}"

        with self.assertRaises(TypeError) as context:
            welcome(name="Matvey", active="yes")  # str вместо bool

        self.assertEqual(
            str(context.exception),
            "Argument 'active' must be of type bool, got str"
        )

    def test_extra_arguments(self):
        @strict
        def subtract(x: int, y: int) -> int:
            return x - y

        with self.assertRaises(TypeError) as context:
            subtract(10, 5, 2)  # слишком много аргументов

        self.assertIn("takes 2 positional arguments but 3 were given", str(context.exception))

    def test_mixed_args_and_kwargs(self):
        @strict
        def join_strings(a: str, b: str, c: str) -> str:
            return a + b + c

        self.assertEqual(join_strings("a", b="b", c="c"), "abc")

    def test_return_annotation_ignored(self):
        @strict
        def divide(x: float, y: float) -> float:
            return x / y

        self.assertAlmostEqual(divide(4.0, 2.0), 2.0)

    def test_bool_type(self):
        @strict
        def flag(active: bool) -> str:
            return "ON" if active else "OFF"

        self.assertEqual(flag(True), "ON")

        with self.assertRaises(TypeError) as context:
            flag(1)  # int не является bool

        self.assertEqual(
            str(context.exception),
            "Argument 'active' must be of type bool, got int"
        )


if __name__ == '__main__':
    unittest.main()