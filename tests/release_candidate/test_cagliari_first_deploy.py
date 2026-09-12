import json
import unittest
from pathlib import Path


def load_messages(path):
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    return {message["id"]: message.get("en_US") for message in payload["messages"]}


class CagliariFirstDeployTests(unittest.TestCase):
    def test_castello_gym_is_delivery_hub(self):
        messages = load_messages("res/text/oreburgh_city_gym.json")
        self.assertEqual(
            messages["OreburghGym_Text_RoarkIntro"],
            [
                "Benvenuto al Delivery Hub di Castello.\n",
                "Io sono il Tech Lead.\r",
                "Prima del primo deploy voglio vedere\n",
                "se la build regge davvero.\r",
                "In locale funziona sempre.\n",
                "Qui conta DEV.\r",
            ],
        )

    def test_first_badge_is_mvp_deploy(self):
        messages = load_messages("res/text/oreburgh_city_gym.json")
        self.assertEqual(
            messages["OreburghGym_Text_BeatRoark"],
            [
                "Build verde. Nessun rollback.\r",
                "Hai chiuso la prima milestone.\r",
                "Questo significa una cosa sola:\n",
                "primo deploy approvato.\r",
                "Ti spetta la Medaglia MVP.\r",
            ],
        )
        self.assertEqual(
            messages["OreburghGym_Text_RoarkReceiveCoalBadge"],
            [
                "{STRVAR_1 3, 0, 0} ha ottenuto\n",
                "la Medaglia MVP!",
            ],
        )
        self.assertEqual(
            messages["OreburghGym_Text_RoarkGymBeaten"],
            [
                "VERSION 0.1.0\n",
                "DEPLOYED TO DEV\r",
                "Ora inizia la parte difficile:\n",
                "farla arrivare in produzione.",
            ],
        )

    def test_castello_leader_is_presented_as_tech_lead(self):
        trainer = json.loads(Path("res/trainers/data/leader_roark.json").read_text(encoding="utf-8"))
        self.assertEqual(trainer["name"], "Tech Lead")


if __name__ == "__main__":
    unittest.main()
