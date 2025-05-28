import os
import random
import sys

sys.path.append("..")

import numpy as np
from dominate import tags

import psynet.experiment
from psynet.asset import CachedAsset, LocalStorage
from psynet.modular_page import SurveyJSControl
from psynet.page import SuccessfulEndPage, ModularPage

from psynet.timeline import Timeline, Event
from psynet.trial.static import StaticTrial, StaticNode, StaticTrialMaker
from psynet.utils import get_logger

try:
    from .consent import consent
    from .debrief import debriefing
    from .instructions import instructions
    from .questionnaire import questionnaire
    from .calibration import AudioCalibration, AudioPromptMultiple
    from .checks import experiment_requirements
# Seems necessary when debugging on pycharm
except ImportError:
    from consent import consent
    from debrief import debriefing
    from instructions import instructions
    from questionnaire import questionnaire
    from calibration import AudioCalibration, AudioPromptMultiple
    from checks import experiment_requirements


# We evaluate each model (Clamp and nCLaMP) using the following set of 3 conditions,
# which use comparisons to anchor our similarity judgments against useful upper/lower bounds.

# Condition 1:
# Real anchor performance
# Target 1: A generated performance from the same genre
# Target 2: A real performance from the same genre
# Tests us against an absolute upper bound of model performance

# Condition 2:
# Real anchor performance
# Target 1: A generated performance from the same genre
# Target 2: A real performance from a different genre
# Tests us against some kind of lower bound of model performance

# Condition 3:
# Real anchor performance
# Target 1: A generated performance from the same genre
# Target 2: A generated performance from a different genre
# Another lower bound of model performance

# We also compare the two model types directly to each other as follows:

# Condition 4:
# Real anchor performance
# Target 1: A generated performance from the same genre from Model 1 (ClaMP)
# Target 2: A generated performance from the same genre from Model 2 (nCLaMP)
# Tells us about how the models compare


def seed_everything(seed: int = 42) -> None:
    """Sets all random seeds for reproducible results."""
    random.seed(seed)
    np.random.seed(seed)


logger = get_logger()

seed_everything(seed=42)
DEBUG__ = False
TRIALS_PER_PARTICIPANT = 3 if DEBUG__ else 8

VOLUME_CALIBRATION_AUDIO = 'assets/calibration/output.mp3'
AUDIO_DIR = 'assets/render'

TEST_DESCRIPTIONS = [
    "CLaMP/target+CLaMP/wrong",
    "nCLaMP/target+nCLaMP/wrong",
    "CLaMP/target+real/wrong",
    "CLaMP/target+real/target",
    "nCLaMP/target+real/wrong",
    "nCLaMP/target+real/target",
    "CLaMP/target+nCLaMP/target",
]
GENRES = ["avantgardejazz", "global", "straightaheadjazz", "traditionalearlyjazz"]


def randomise_variables(var_tuple: tuple[str, str]):
    """Randomly assign the first and second item in a tuple to two variables"""
    #  This is how we shuffle the order of presentation
    if random.choice([True, False]):
        var_a, var_b = var_tuple
    else:
        var_b, var_a = var_tuple
    return var_a, var_b


def get_nodes(audio_dir: str = AUDIO_DIR) -> list[StaticNode]:
    """Gets all PsyNet nodes for the experiment"""
    nodes = []
    anchor_paths = sorted([i for i in os.listdir(audio_dir) if "anchor" in i])
    if len(anchor_paths) == 0:
        raise FileNotFoundError("Please make sure you have populated the render directory with the audio files")
    for anchor in anchor_paths:
        # Join with the audio directory to get the complete filepath
        anchor_path = os.path.join(audio_dir, anchor)
        # Get the name of the genre and the MBZ ID of the track from the filepath
        genre, anchor_id = anchor.split("_")[0], anchor.split("_")[-1].split(".")[0]
        # Skip over incorrect genres
        if genre not in GENRES:
            continue
        # Filepaths for generations can be obtained easily with string manipulation
        getter_gen = lambda fp: "_".join(anchor.split("_")[:2]) + fp
        clamp_target = getter_gen("_gen_match_clamp.mid.mp3")
        noclamp_target = getter_gen("_gen_match_noclamp.mid.mp3")
        clamp_wrong = getter_gen("_gen_nomatch_clamp.mid.mp3")
        noclamp_wrong = getter_gen("_gen_nomatch_noclamp.mid.mp3")
        # Filepaths for "real" tracks are a bit more complicated as they have IDs in them
        getter_real = lambda fp: sorted([
            i for i in os.listdir(audio_dir) if "_".join(anchor.split("_")[:2]) + fp in i
        ])[0]
        real_target = getter_real("_real_match_")
        real_wrong = getter_real("_real_nomatch_")
        # Sanity check that the MBZ IDs for the real tracks are different to the anchor track
        for real in [real_target, real_wrong]:
            real_id = real.split("_")[-1].split(".")[0]
            assert real_id != anchor_id
        # Create the tests as tuples of filepaths
        # TEST 1: CLaMP/target | CLaMP/wrong
        test_1 = (clamp_target, clamp_wrong)
        # TEST 2: nCLaMP/target | nCLaMP/wrong
        test_2 = (noclamp_target, noclamp_wrong)
        # TEST 3: CLaMP/target | real/wrong
        test_3 = (clamp_target, real_wrong)
        # TEST 4: CLaMP/target | real/target
        test_4 = (clamp_target, real_target)
        # TEST 5: nCLaMP/target | real/wrong
        test_5 = (noclamp_target, real_wrong)
        # TEST 6: nCLaMP/target | real/target
        test_6 = (noclamp_target, real_target)
        # TEST 7: CLaMP/target | nCLaMP/target
        test_7 = (clamp_target, noclamp_target)
        all_tests = [test_1, test_2, test_3, test_4, test_5, test_6, test_7]
        # Iterate over all the tests and the corresponding description
        for track_tuple, description in zip(all_tests, TEST_DESCRIPTIONS):
            # 50% chance that A is the first item in the tuple, 50% that it is the second
            track_a, track_b = randomise_variables(track_tuple)
            # Convert to paths
            track_a_path = os.path.join(audio_dir, track_a)
            track_b_path = os.path.join(audio_dir, track_b)
            # Sanity check all paths exist on disk
            for t_path in [track_a_path, track_b_path, anchor_path]:
                assert os.path.isfile(t_path)
            # Sanity check all items are unique
            assert track_a_path != track_b_path != anchor_path
            # Create the current node
            node = StaticNode(
                definition={
                    "genre": genre,
                    "description": description,
                    "anchor": anchor,
                    "test_a": track_a,
                    "test_b": track_b,
                },
                assets={
                    "anchor": CachedAsset(
                        input_path=anchor_path,
                    ),
                    "test_a": CachedAsset(
                        input_path=track_a_path,
                    ),
                    "test_b": CachedAsset(
                        input_path=track_b_path,
                    )
                }
            )
            nodes.append(node)
    assert len(nodes) == len(anchor_paths) * len(TEST_DESCRIPTIONS)
    return nodes


class RateTrial(StaticTrial):
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
                definition=self.node.definition,
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
                          "title": "Out of performances A and B, which sounds more like the anchor?",
                          "description": "Choose only one performance.",
                          "isRequired": True,
                          "showCommentArea": True,
                          "commentText": "What influenced your decision?",
                          "commentPlaceholder": "Optional",
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
                          "title": "I like this performance.",
                          "description": "Rate how much you like or dislike each performance.",
                          "isRequired": True,
                          "columns": [
                            {
                              "value": "1",
                              "text": "Strongly dislike"
                            },
                            {
                              "value": "2",
                              "text": "Dislike"
                            },
                            {
                              "value": "3",
                              "text": "Neither like nor dislike"
                            },
                            {
                              "value": "4",
                              "text": "Like"
                            },
                            {
                              "value": "5",
                              "text": "Strongly like"
                            }
                          ],
                          "rows": [
                            {
                              "value": "perf_a",
                              "text": "Performance A"
                            },
                            {
                              "value": "perf_b",
                              "text": "Performance B"
                            }
                          ]
                        },
                        {
                          "type": "matrix",
                          "name": "diversity",
                          "title": "The performance is creative.",
                          "description": "Rate how strongly you agree or disagree with the statement for each performance.",
                          "isRequired": True,
                          "columns": [
                            {
                              "value": "1",
                              "text": "Strongly disagree"
                            },
                            {
                              "value": "2",
                              "text": "Disagree"
                            },
                            {
                              "value": "3",
                              "text": "Neither agree nor disagree"
                            },
                            {
                              "value": "4",
                              "text": "Agree"
                            },
                            {
                              "value": "5",
                              "text": "Strongly agree"
                            }
                          ],
                          "rows": [
                            {
                              "value": "perf_a",
                              "text": "Performance A"
                            },
                            {
                              "value": "perf_b",
                              "text": "Performance B"
                            }
                          ]
                        },
                        {
                          "type": "matrix",
                          "name": "is_ml",
                          "title": "The performance is generated with AI.",
                          "description": "Rate how strongly you agree or disagree with the statement for each performance.",
                          "isRequired": True,
                          "columns": [
                            {
                              "value": "1",
                              "text": "Strongly disagree"
                            },
                            {
                              "value": "2",
                              "text": "Disagree"
                            },
                            {
                              "value": "3",
                              "text": "Neither agree nor disagree"
                            },
                            {
                              "value": "4",
                              "text": "Agree"
                            },
                            {
                              "value": "5",
                              "text": "Strongly agree"
                            }
                          ],
                          "rows": [
                            {
                              "value": "perf_a",
                              "text": "Performance A"
                            },
                            {
                              "value": "perf_b",
                              "text": "Performance B"
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


class RateTrialMaker(StaticTrialMaker):
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
    timeline = Timeline(
        consent(),
        experiment_requirements(),
        AudioCalibration(audio=VOLUME_CALIBRATION_AUDIO),
        instructions(),
        RateTrialMaker(
            id_="main_experiment",
            trial_class=RateTrial,
            nodes=get_nodes,
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
