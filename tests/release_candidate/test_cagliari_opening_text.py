import json
import unittest
from pathlib import Path


def load_messages(path):
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    return {message["id"]: message["en_US"] for message in payload["messages"]}


class CagliariOpeningTextTests(unittest.TestCase):
    def test_intro_establishes_release_candidate_onboarding(self):
        messages = load_messages("res/text/rowan_intro.json")
        self.assertEqual(
            messages["RowanIntro_Text_HelloThere"],
            [
                "Ciao!\n",
                "Benvenuto in Release Candidate.\r",
                "Sei stato assegnato a un progetto\n",
                "già avviato.\r",
            ],
        )
        self.assertEqual(
            messages["RowanIntro_Text_MyNameRowan"],
            [
                "Io coordino il delivery.\r",
                "Qui mi chiamano il Manager.\r",
                "I requisiti sono quasi definitivi.\n",
                "Quasi.\r",
                "Prima di partire, facciamo un breve\n",
                "allineamento.\r",
            ],
        )

    def test_intro_sends_player_to_cagliari_and_uat(self):
        messages = load_messages("res/text/rowan_intro.json")
        self.assertEqual(
            messages["RowanIntro_Text_EndDialogue"],
            [
                "Perfetto, {STRVAR_1 3, 0, 0}.\n",
                "Il progetto è ufficialmente partito.\r",
                "Prima tappa: Cagliari.\r",
                "Raccogli requisiti, gestisci le\n",
                "change request e prepara il deploy.\r",
                "Buon lavoro. Ci vediamo in UAT.\r",
            ],
        )


if __name__ == "__main__":
    unittest.main()
