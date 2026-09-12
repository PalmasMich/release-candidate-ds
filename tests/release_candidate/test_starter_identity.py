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


if __name__ == "__main__":
    unittest.main()
