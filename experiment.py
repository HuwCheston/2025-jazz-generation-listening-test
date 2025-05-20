import os
import random
import sys

sys.path.append("..")

from dominate import tags

import psynet.experiment
from psynet.asset import CachedAsset, LocalStorage
from psynet.modular_page import AudioPrompt, RadioButtonControl, Prompt, SurveyJSControl
from psynet.page import SuccessfulEndPage, ModularPage

from psynet.timeline import Timeline, Event
from psynet.trial.static import StaticTrial, StaticNode, StaticTrialMaker
from psynet.utils import get_logger

from .consent import consent
from .debrief import debriefing
from .instructions import instructions
from .questionnaire import questionnaire
from .calibration import AudioCalibration, AudioPromptMultiple, RadioButtonMultiple
from .checks import experiment_requirements

logger = get_logger()

DEBUG__ = False
TRIALS_PER_PARTICIPANT = 3 if DEBUG__ else 10

VOLUME_CALIBRATION_AUDIO = 'assets/calibration/output.mp3'
AUDIO_DIR = 'assets/render'

GENRES = ["avantgardejazz", "global", "straightaheadjazz", "traditionalearlyjazz"]
NODES = []

TEST_DESCRIPTIONS = [
    ("CLaMP/target", "CLaMP/wrong"),
    ("nCLaMP/target", "nCLaMP/wrong"),
    ("CLaMP/target", "real/wrong"),
    ("CLaMP/target", "real/target"),
    ("nCLaMP/target", "real/wrong"),
    ("nCLaMP/target", "real/target"),
    ("CLaMP/target", "nCLaMP/target"),
]

real_paths = [i for i in os.listdir(AUDIO_DIR) if "real" in i]
for anchor in real_paths:
    anchor_path = os.path.join(AUDIO_DIR, anchor)
    genre, anchor_id = anchor.split("_")[0], anchor.split("_")[-1].split(".")[0]
    if genre not in GENRES:
        continue
    # Get generated paths
    generates_same_genre_clamp = [i for i in os.listdir(AUDIO_DIR) if i.startswith(genre) and "gen_clamp" in i]
    generates_same_genre_noclamp = [i for i in os.listdir(AUDIO_DIR) if i.startswith(genre) and "gen_noclamp" in i]
    generates_diff_genre_clamp = [i for i in os.listdir(AUDIO_DIR) if not i.startswith(genre) and "gen_clamp" in i]
    generates_diff_genre_noclamp = [i for i in os.listdir(AUDIO_DIR) if not i.startswith(genre) and "gen_noclamp" in i]
    # Get real paths
    reals_same_genre = [
        i for i in os.listdir(AUDIO_DIR)
        if i.startswith(genre)
        and "real_" in i
        and i != anchor     # should not be the same as the anchor!
        and i.split("_")[-1].split(".")[0] != anchor_id     # shouldn't have the same track ID
    ]
    reals_diff_genre = [
        i for i in os.listdir(AUDIO_DIR)
        if not i.startswith(genre)
        and "real_" in i
        and i.split("_")[-1].split(".")[0] != anchor_id     # shouldn't have the same track ID
    ]
    # TEST 1: CLaMP/target | CLaMP/wrong
    test_1 = (
        random.choice(generates_same_genre_clamp), random.choice(generates_diff_genre_clamp)
    )
    # TEST 2: nCLaMP/target | nCLaMP/wrong
    test_2 = (
        random.choice(generates_same_genre_noclamp), random.choice(generates_diff_genre_noclamp)
    )
    # TEST 3: CLaMP/target | real/wrong
    test_3 = (
        random.choice(generates_same_genre_clamp), random.choice(reals_diff_genre)
    )
    # TEST 4: CLaMP/target | real/target
    test_4 = (
        random.choice(generates_same_genre_clamp), random.choice(reals_same_genre)
    )
    # TEST 5: nCLaMP/target | real/wrong
    test_5 = (
        random.choice(generates_same_genre_noclamp), random.choice(reals_diff_genre)
    )
    # TEST 6: nCLaMP/target | real/target
    test_6 = (
        random.choice(generates_same_genre_noclamp), random.choice(reals_same_genre)
    )
    # TEST 7: CLaMP/target | nCLaMP/target
    test_7 = (
        random.choice(generates_same_genre_clamp), random.choice(generates_same_genre_noclamp)
    )
    # Iterate over all tests and descriptions of them
    for test, description in zip([test_1, test_2, test_3, test_4, test_5, test_6, test_7], TEST_DESCRIPTIONS):
        # Get all file-paths correctly
        test_a, test_b = test
        test_a_path = os.path.join(AUDIO_DIR, test_a)
        test_b_path = os.path.join(AUDIO_DIR, test_b)
        # Check all paths exist on disk
        assert os.path.isfile(test_a_path)
        assert os.path.isfile(test_b_path)
        assert os.path.isfile(anchor_path)
        # Create the current node
        node = StaticNode(
            definition={
                "genre": genre,
                "description": description,
                "anchor": anchor,
                "test_a": test_a,
                "test_b": test_b,
            },
            assets={
                "anchor": CachedAsset(
                    input_path=anchor_path,
                ),
                "test_a": CachedAsset(
                    input_path=test_a_path,
                ),
                "test_b": CachedAsset(
                    input_path=test_b_path,
                )
            }
        )
        NODES.append(node)


class SuccessTrial(StaticTrial):
    time_estimate = 50

    def get_text(self):
        text = [
            tags.h1("Listen to the performances"),
        ]
        if DEBUG__:
            text.append(tags.p(
                    f"Genre: {self.node.definition['genre']}\n"
                    f"Test description: {self.node.definition['description']}\n"
                    f"Anchor: {self.node.definition['anchor']}\n"
                    f"A: {self.node.definition['test_a']}\n"
                    f"B: {self.node.definition['test_b']}\n"
                )
            )
        return tags.div(*text)

    def show_trial(self, *_, **__):
        return ModularPage(
            label="rating",
            prompt=AudioPromptMultiple(
                audio=self.node.assets['anchor'],
                all_audio=self.node.assets,
                text=self.get_text(),
                loop=False,
                controls=True,
            ),
            control=SurveyJSControl(design={
                  "pages": [
                    {
                      "name": "page1",
                      "elements": [
                        {
                          "type": "matrix",
                          "name": "similar",
                          "title": "Which performance is most similar to the Anchor?",
                          "isRequired": True,
                          "columns": [
                            {
                              "value": "perf_a",
                              "text": "Performance A"
                            },
                            {
                              "value": "perf_b",
                              "text": "Performance B"
                            },
                            {
                              "value": "null",
                              "text": "No Preference"
                            }
                          ],
                          "rows": [
                            {
                              "value": "similar_perf",
                              "text": "Make a selection"
                            }
                          ]
                        },
                        {
                          "type": "matrix",
                          "name": "preference",
                          "title": "Which performance do you prefer?",
                          "isRequired": True,
                          "columns": [
                            {
                              "value": "perf_a",
                              "text": "Performance A"
                            },
                            {
                              "value": "perf_b",
                              "text": "Performance B"
                            },
                            {
                              "value": "null",
                              "text": "No Preference"
                            }
                          ],
                          "rows": [
                            {
                              "value": "prefer_perf",
                              "text": "Make a selection"
                            }
                          ]
                        }
                      ]
                    }
                  ]
                }
            ),
            events={
                "responseEnable": Event(is_triggered_by="promptStart"),
                "submitEnable": Event(is_triggered_by="promptEnd"),
            },
        )


class SuccessTrialMaker(StaticTrialMaker):
    give_end_feedback_passed = False


class Exp(psynet.experiment.Experiment):
    label = "Jazz music generation listening test"
    asset_storage = LocalStorage()
    max_exp_dir_size_in_mb = 1000000000
    config = {
        "currency": "£",
        "wage_per_hour": 0.0,
        "window_width": 1024,
        "window_height": 1024,
    }
    if DEBUG__:
        timeline = Timeline(
            consent(),
            SuccessTrialMaker(
                id_="main_experiment",
                trial_class=SuccessTrial,
                nodes=NODES,
                expected_trials_per_participant=TRIALS_PER_PARTICIPANT,
                max_trials_per_participant=TRIALS_PER_PARTICIPANT,
                recruit_mode='n_trials',
                target_trials_per_node=10,
                allow_repeated_nodes=False,
                balance_across_nodes=True,
                check_performance_at_end=False,
                check_performance_every_trial=False,
                fail_trials_on_premature_exit=True,
                fail_trials_on_participant_performance_check=True,
                n_repeat_trials=0,
            ),
            SuccessfulEndPage(),
        )
    else:
        timeline = Timeline(
            consent(),
            experiment_requirements(),
            AudioCalibration(audio=VOLUME_CALIBRATION_AUDIO),
            instructions(),
            SuccessTrialMaker(
                id_="main_experiment",
                trial_class=SuccessTrial,
                nodes=NODES,
                expected_trials_per_participant=TRIALS_PER_PARTICIPANT,
                max_trials_per_participant=TRIALS_PER_PARTICIPANT,
                recruit_mode='n_trials',
                target_trials_per_node=10,
                allow_repeated_nodes=False,
                balance_across_nodes=True,
                check_performance_at_end=False,
                check_performance_every_trial=False,
                fail_trials_on_premature_exit=True,
                fail_trials_on_participant_performance_check=True,
                n_repeat_trials=0,
            ),
            questionnaire(),
            debriefing(),
            SuccessfulEndPage(),
        )
