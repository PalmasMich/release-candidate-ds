from pathlib import Path
import subprocess
import unittest


ROOT = Path(__file__).resolve().parents[2]
WORKFLOWS = ROOT / ".github" / "workflows"


class RepositoryPolicyTests(unittest.TestCase):
    def test_no_nds_rom_is_tracked(self):
        result = subprocess.run(
            ["git", "ls-files", "*.nds"],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        tracked = [line for line in result.stdout.splitlines() if line.strip()]
        self.assertEqual([], tracked, f"Tracked .nds ROM(s): {tracked}")

    def test_workflows_do_not_upload_artifacts(self):
        offenders = []
        for path in sorted(WORKFLOWS.glob("*.y*ml")):
            if "actions/upload-artifact" in path.read_text(encoding="utf-8"):
                offenders.append(str(path.relative_to(ROOT)))
        self.assertEqual([], offenders, f"Artifact-upload workflow(s): {offenders}")


if __name__ == "__main__":
    unittest.main()
