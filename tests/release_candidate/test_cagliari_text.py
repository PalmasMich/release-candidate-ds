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

    def test_opening_progression_stays_inside_cagliari(self):
        text_path = Path("res/text/location_names.json")
        payload = json.loads(text_path.read_text(encoding="utf-8"))
        messages = {message["id"]: message["en_US"] for message in payload["messages"]}

        expected = {
            "LocationNames_Text_TwinleafTown": "Cagliari",
            "LocationNames_Text_Route201": "Via Roma",
            "LocationNames_Text_SandgemTown": "Marina",
            "LocationNames_Text_Route202": "Stampace",
            "LocationNames_Text_JubilifeCity": "Centro",
            "LocationNames_Text_Route203": "Buoncammino",
            "LocationNames_Text_OreburghGate": "Bastione",
            "LocationNames_Text_OreburghCity": "Castello",
        }

        for message_id, expected_name in expected.items():
            with self.subTest(message_id=message_id):
                self.assertEqual(messages[message_id], expected_name)


if __name__ == "__main__":
    unittest.main()
