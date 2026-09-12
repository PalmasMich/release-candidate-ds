import configparser
import unittest
from pathlib import Path


class RomIdentityTests(unittest.TestCase):
    def test_rev1_header_uses_release_candidate_title(self):
        parser = configparser.ConfigParser()
        parser.read(Path("platinum.us/rom_rev1.ini"), encoding="utf-8")
        self.assertEqual(parser["header"]["title"], "RELEASE CAND")

    def test_rev1_banner_identifies_release_candidate(self):
        parser = configparser.ConfigParser()
        parser.read(Path("platinum.us/rom_rev1.ini"), encoding="utf-8")
        self.assertEqual(parser["banner"]["title"], "Release Candidate")
        self.assertEqual(parser["banner"]["developer"], "PalmasMich")


if __name__ == "__main__":
    unittest.main()
