import json
import unittest
from pathlib import Path


class CagliariTextTests(unittest.TestCase):
    def test_starting_town_map_sign_is_cagliari(self):
        text_path = Path("res/text/twinleaf_town.json")
        payload = json.loads(text_path.read_text(encoding="utf-8"))

        messages = {message["id"]: message["en_US"] for message in payload["messages"]}

        self.assertEqual(
            messages["TwinleafTown_Text_MapSign"],
            ["Cagliari\n", "Prima build. Zero bug. Forse."],
        )


if __name__ == "__main__":
    unittest.main()
