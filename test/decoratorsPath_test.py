from kaa import decorators
from .decorators_test import DecoratorsTest


class DecoratorPathTest(DecoratorsTest):

    def testPathWrong(self):
        pathFunc = decorators.PATH('/path')
        func = pathFunc(self.__setAssertArgs())
        result = func(self.getResource(path='/otherPath'))
        self.assertFalse(result)
    
    def testPathBase(self):
        pathFunc = decorators.PATH('')
        func = pathFunc(self.__setAssertArgs())
        self.assertTrue(func(self.getResource(path='/')))
        self.assertTrue(func(self.getResource(path='')))

        pathFunc = decorators.PATH('/')
        func = pathFunc(self.__setAssertArgs())
        self.assertTrue(func(self.getResource(path='/')))
        self.assertTrue(func(self.getResource(path='')))

    def testPathValid(self):
        pathFunc = decorators.PATH('/path')
        func = pathFunc(self.__setAssertArgs())
        self.assertTrue(func(self.getResource(path='/path')))

        pathFunc = decorators.PATH('/path/subPath')
        func = pathFunc(self.__setAssertArgs())
        self.assertTrue(func(self.getResource(path='/path/subPath')))

    def testPathArgsWrong(self):
        pathFunc = decorators.PATH('/path/{identifier}')
        func = pathFunc(self.__setAssertArgs(
            assertionArgs = self.assertFalse,
            id='anyValue'
        ))
        result = func(self.getResource(path='/path/24'))
        self.assertTrue(result)

    def testPathArgsWrongValue(self):
        pathFunc = decorators.PATH('/path/{id:[a-z]}')
        func = pathFunc(self.__setAssertArgs())
        result = func(self.getResource(path='/path/24'))
        self.assertFalse(result)

    def testPathArgsValid(self):
        pathFunc = decorators.PATH('/path/{id:[0-9]}')
        func = pathFunc(self.__setAssertArgs(
            assertionArgs = self.assertTrue,
            assertionValues = self.assertEqual,
            id='24'
        ))
        result = func(self.getResource(path='/path/24'))
        self.assertTrue(result)

    def testPathMultipleWrong(self):
        pathFunc = decorators.PATH('/path/{id:[0-9]}/subPath/{option}')
        func = pathFunc(self.__setAssertArgs())
        result = func(self.getResource(path='/path/24'))
        self.assertFalse(result)

    def testPathMultipleValid(self):
        pathFunc = decorators.PATH('/path/{id:[0-9]}/subPath/{option}')
        func = pathFunc(self.__setAssertArgs(
            assertionArgs = self.assertTrue,
            assertionValues = self.assertEqual,
            id='24',
            option='value'
        ))
        result = func(self.getResource(path='/path/24/subPath/value'))
        self.assertTrue(result)
        
    def __setAssertArgs(self, assertionArgs=None, assertionValues=None, **expected_args):
        def wrap(self_rest, **result_args):
            for arg_name in expected_args:
                if assertionArgs is not None:
                    print(arg_name)
                    assertionArgs(arg_name in result_args)
                if assertionValues is not None:
                    assertionValues(result_args[arg_name], expected_args[arg_name])
            return True
        return wrap
