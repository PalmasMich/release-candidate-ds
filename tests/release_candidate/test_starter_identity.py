import json
import unittest
from pathlib import Path


class StarterIdentityTests(unittest.TestCase):
    def load(self, species):
        path = Path(f"res/pokemon/{species}/data.json")
        return json.loads(path.read_text(encoding="utf-8"))

    def test_turtle_starter_identity(self):
        data = self.load("turtwig")
        self.assertEqual(data["types"], ["TYPE_GRASS", "TYPE_GROUND"])
        self.assertEqual(data["pokedex_data"]["en"]["name"], "TARTAVIA")
        self.assertEqual(data["pokedex_data"]["en"]["category"], "Viandante Pokémon")

    def test_fire_monkey_starter_identity(self):
        data = self.load("chimchar")
        self.assertEqual(data["types"], ["TYPE_FIRE", "TYPE_FIRE"])
        self.assertEqual(data["pokedex_data"]["en"]["name"], "SARURAI")
        self.assertEqual(data["pokedex_data"]["en"]["category"], "Apprendista Pokémon")

    def test_water_frog_starter_identity(self):
        data = self.load("piplup")
        self.assertEqual(data["types"], ["TYPE_WATER", "TYPE_WATER"])
        self.assertEqual(data["pokedex_data"]["en"]["name"], "RANAMI")
        self.assertEqual(data["pokedex_data"]["en"]["category"], "Ventaglio Pokémon")

    def test_starter_selection_copy_uses_release_candidate_starters(self):
        path = Path("res/text/unk_0360.json")
        payload = json.loads(path.read_text(encoding="utf-8"))
        messages = {message["id"]: message.get("en_US") for message in payload["messages"]}

        self.assertEqual(
            messages["pl_msg_00000360_00000"],
            [
                "Queste sono le tre risorse disponibili.\n",
                "Una sola entrerà nel tuo team.\r",
            ],
        )
        self.assertEqual(
            messages["pl_msg_00000360_00001"],
            [
                "{COLOR 3}TARTAVIA - Erba/Terra{COLOR 0}\n",
                "Vuoi partire con lui?",
            ],
        )
        self.assertEqual(
            messages["pl_msg_00000360_00002"],
            [
                "{COLOR 1}SARURAI - Fuoco{COLOR 0}\n",
                "Vuoi partire con lui?",
            ],
        )
        self.assertEqual(
            messages["pl_msg_00000360_00003"],
            [
                "{COLOR 2}RANAMI - Acqua{COLOR 0}\n",
                "Vuoi partire con lei?",
            ],
        )
        self.assertEqual(
            messages["pl_msg_00000360_00007"],
            [
                "Scegli il tuo starter.\n",
                "Il primo requisito è già cambiato.",
            ],
        )


if __name__ == "__main__":
    unittest.main()
