from kaa import PATH
from .decorators_test import DecoratorsTest


class DecoratorPathTest(DecoratorsTest):
    def test_path_wrong(self):
        path_func = PATH("/path")
        func = path_func(self.__set_assert_args())
        result = func(self.get_resource(path="/otherPath"))
        self.assertFalse(result)

    def test_path_base(self):
        path_func = PATH("")
        func = path_func(self.__set_assert_args())
        self.assertTrue(func(self.get_resource(path="/")))
        self.assertTrue(func(self.get_resource(path="")))

        path_func = PATH("/")
        func = path_func(self.__set_assert_args())
        self.assertTrue(func(self.get_resource(path="/")))
        self.assertTrue(func(self.get_resource(path="")))

    def test_path_valid(self):
        path_func = PATH("/path")
        func = path_func(self.__set_assert_args())
        self.assertTrue(func(self.get_resource(path="/path")))

        path_func = PATH("/path/subPath")
        func = path_func(self.__set_assert_args())
        self.assertTrue(func(self.get_resource(path="/path/subPath")))

    def test_path_args_wrong(self):
        path_func = PATH("/path/{identifier}")
        func = path_func(
            self.__set_assert_args(assertion_args=self.assertFalse, id="anyValue")
        )
        result = func(self.get_resource(path="/path/24"))
        self.assertTrue(result)

    def test_path_args_wrong_value(self):
        path_func = PATH("/path/{id:[a-z]}")
        func = path_func(self.__set_assert_args())
        result = func(self.get_resource(path="/path/24"))
        self.assertFalse(result)

    def test_path_args_valid(self):
        path_func = PATH("/path/{id:[0-9]}")
        func = path_func(
            self.__set_assert_args(
                assertion_args=self.assertTrue,
                assertion_values=self.assertEqual,
                id="24",
            )
        )
        result = func(self.get_resource(path="/path/24"))
        self.assertTrue(result)

    def test_path_multiple_wrong(self):
        path_func = PATH("/path/{id:[0-9]}/subPath/{option}")
        func = path_func(self.__set_assert_args())
        result = func(self.get_resource(path="/path/24"))
        self.assertFalse(result)

    def test_path_multiple_valid(self):
        path_func = PATH("/path/{id:[0-9]}/subPath/{option}")
        func = path_func(
            self.__set_assert_args(
                assertion_args=self.assertTrue,
                assertion_values=self.assertEqual,
                id="24",
                option="value",
            )
        )
        result = func(self.get_resource(path="/path/24/subPath/value"))
        self.assertTrue(result)

    def __set_assert_args(
        self, assertion_args=None, assertion_values=None, **expected_args
    ):
        def wrap(self_rest, **result_args):
            for arg_name in expected_args:
                if assertion_args is not None:
                    print(arg_name)
                    assertion_args(arg_name in result_args)
                if assertion_values is not None:
                    assertion_values(result_args[arg_name], expected_args[arg_name])
            return True

        return wrap
