import os
import random
import sys
import json

sys.path.append("..")

import numpy as np
from dominate import tags

import psynet.experiment
from psynet.asset import CachedAsset, LocalStorage
from psynet.modular_page import SurveyJSControl, Prompt
from psynet.page import SuccessfulEndPage, ModularPage

from psynet.timeline import Timeline, Event
from psynet.trial.static import StaticTrial, StaticNode, StaticTrialMaker
from psynet.utils import get_logger

try:
    from .consent import consent
    from .debrief import debriefing
    from .instructions import instructions
    from .questionnaire import questionnaire
    from .calibration import AudioCalibration, AudioPromptCustom
    from .checks import experiment_requirements
# Seems necessary when debugging on pycharm
except ImportError:
    from consent import consent
    from debrief import debriefing
    from instructions import instructions
    from questionnaire import questionnaire
    from calibration import AudioCalibration, AudioPromptCustom
    from checks import experiment_requirements


def seed_everything(seed: int = 42) -> None:
    """Sets all random seeds for reproducible results."""
    random.seed(seed)
    np.random.seed(seed)


logger = get_logger()

seed_everything(seed=42)
DEBUG__ = False
TRIALS_PER_PARTICIPANT = 3 if DEBUG__ else 15

VOLUME_CALIBRATION_AUDIO = 'assets/calibration/output.mp3'
AUDIO_DIR = 'assets/render'
METADATA_DIR = "assets/metadata"

GENRES = ["avantgardejazz", "straightaheadjazz", "traditionalearlyjazz"]


def get_nodes(audio_dir: str = AUDIO_DIR) -> list[StaticNode]:
    """Gets all PsyNet nodes for the experiment"""
    nodes = []
    render_paths = sorted([i for i in os.listdir(audio_dir) if i.endswith(".mp3")])
    for render in render_paths:
        genre, num, condition = render.split("_")
        condition = condition.split(".")[0]    # remove the extension
        # Grab the metadata using the filepath
        metadata_path = os.path.join(METADATA_DIR, "_".join([genre, num, condition]) + ".json")
        with open(metadata_path, "r") as f:
            metadata_read = json.load(f)
        # Construct the node
        node = StaticNode(
            definition={"genre": genre, "num": int(num), "condition": condition, "metadata": metadata_read},
            assets={"render": CachedAsset(input_path=os.path.join(AUDIO_DIR, render))}
        )
        nodes.append(node)
    return nodes


class RateTrial(StaticTrial):
    time_estimate = 30

    def get_feedback_text(self):
        metadata = self.node.definition["metadata"]
        if metadata["condition_type"] == "real":
            return (f"You just listened to '{metadata['track_name']}' performed by {metadata['pianist']}, an example of {metadata['condition_token']}.")
        else:
            return f"You just listened to a generated example of {metadata['condition_token']}."

    def show_feedback(self, experiment, participant):
        return ModularPage(
            label="listening_feedback",
            prompt=Prompt(
                text=self.get_feedback_text()
            )
        )

    def get_text(self):
        text = [
            tags.h1("Listen to the performance"),
        ]
        if DEBUG__:
            text.append(tags.p(
                    f"Genre: {self.node.definition['genre']}\n"
                    f"Test description: {self.node.definition['condition']}\n"
                    f"Metadata {self.node.definition['metadata']}"
                )
            )
        return tags.div(*text)

    def show_trial(self, *_, **__):
        return ModularPage(
            label="rating",
            prompt=AudioPromptCustom(
                definition=self.node.definition,
                audio=self.node.assets['render'],
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
                              "name": "genre",
                              "title": "Which genre best matches this performance?",
                              "description": "Choose only one genre.",
                              "isRequired": True,
                              "columns": [
                                  {
                                      "value": "avantgardejazz",
                                      "text": "Avant-Garde"
                                  },
                                  {
                                      "value": "straightaheadjazz",
                                      "text": "Straight-Ahead"
                                  },
                                  {
                                      "value": "traditionalearlyjazz",
                                      "text": "Traditional & Early"
                                  }
                              ],
                              "rows": [
                                  {
                                      "value": "",
                                      "text": ""
                                  }
                              ]
                          },
                          {
                              "type": "rating",
                              "name": "fit",
                              "title": "How much does this performance sound like that genre?",
                              "description": "Where a score of 5 means \"sounds exactly like\""
                          },
                        {
                          "type": "matrix",
                          "name": "preference",
                          "title": "I like this performance.",
                          "description": "Rate how strongly you agree or disagree with the statement for the performance.",
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
                              "value": "",
                              "text": ""
                            }
                          ]
                        },
                        {
                          "type": "matrix",
                          "name": "diversity",
                          "title": "The performance is creative.",
                          "description": "Rate how strongly you agree or disagree with the statement for the performance.",
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
                              "value": "",
                              "text": ""
                            }
                          ]
                        },
                        {
                          "type": "matrix",
                          "name": "is_ml",
                          "title": "The performance is generated with AI.",
                          "description": "Rate how strongly you agree or disagree with the statement for the performance.",
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
                              "value": "",
                              "text": ""
                            }
                          ]
                        }
                      ]
                    }
                  ]
                }
            ),
            # events={
            #     "responseEnable": Event(is_triggered_by="promptStart"),
            #     "submitEnable": Event(is_triggered_by="promptEnd"),
            # },
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
            target_trials_per_node=TRIALS_PER_PARTICIPANT,
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
