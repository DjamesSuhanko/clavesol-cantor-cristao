import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location("converter", Path(__file__).resolve().parents[1]/"scripts/converter_cantor_cristao.py")
converter = importlib.util.module_from_spec(spec)
spec.loader.exec_module(converter)

class IdentityTests(unittest.TestCase):
    def test_versions_have_independent_destinations(self):
        cases = {"cc060a-4vozes.xml": (60, "hino-060a"),
                 "cc060b-4vozes.xml": (60, "hino-060b"),
                 "cc326-4vozes.xml": (326, "hino-326"),
                 "cc326b-4vozes.xml": (326, "hino-326b"),
                 "cc371A-4vozes.xml": (371, "hino-371a"),
                 "cc371b-4vozes.xml": (371, "hino-371b")}
        for name, expected in cases.items():
            with self.subTest(name=name):
                self.assertEqual(converter.identity(Path(name)), expected)
        self.assertEqual(len({converter.identity(Path(name))[1] for name in cases}), len(cases))

    def test_missing_number(self):
        with self.assertRaises(ValueError):
            converter.identity(Path("sem-numero.xml"))

if __name__ == "__main__":
    unittest.main()
