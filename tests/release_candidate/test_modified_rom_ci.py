import unittest
from pathlib import Path


class ModifiedRomCiTests(unittest.TestCase):
    def test_full_build_skips_stock_checksum_for_custom_game(self):
        workflow = Path(".github/workflows/build.yml").read_text(encoding="utf-8")

        self.assertIn("run: make rom", workflow)
        self.assertNotIn("run: make check", workflow)


if __name__ == "__main__":
    unittest.main()
