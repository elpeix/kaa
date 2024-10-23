class TestBase:
    # Compatibility with unittest
    def assertFalse(self, value):
        assert not value

    def assertTrue(self, value):
        assert value

    def assertEqual(self, value1, value2):
        assert value1 == value2

    def assertIsNone(self, value):
        assert value is None

    def assertIsNotNone(self, value):
        assert value is not None

