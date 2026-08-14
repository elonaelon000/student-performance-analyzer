import tempfile
import unittest
from pathlib import Path

import matplotlib
import pandas as pd

matplotlib.use("Agg")

from visualizations import generate_charts


class VisualizationTests(unittest.TestCase):
    def test_generate_charts_creates_png_files(self) -> None:
        students = pd.DataFrame(
            [
                {
                    "name": "Ada",
                    "math": 90.0,
                    "programming": 80.0,
                    "statistics": 70.0,
                    "study_hours": 10.0,
                },
                {
                    "name": "Ben",
                    "math": 60.0,
                    "programming": 50.0,
                    "statistics": 40.0,
                    "study_hours": 5.0,
                },
            ]
        )

        with tempfile.TemporaryDirectory() as temp_dir:
            paths = generate_charts(students, Path(temp_dir))
            self.assertEqual(len(paths), 2)
            for path in paths:
                self.assertTrue(path.exists())
                self.assertEqual(path.suffix, ".png")


if __name__ == "__main__":
    unittest.main()
