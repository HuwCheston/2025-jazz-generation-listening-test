import os
import random

from dominate import tags

from psynet.modular_page import ModularPage, AudioPrompt, ImagePrompt, PushButtonControl, Prompt
from psynet.prescreen import HeadphoneTest
from psynet.page import InfoPage, SuccessfulEndPage, UnsuccessfulEndPage
from psynet.timeline import CodeBlock, PageMaker, join, Event, Module, conditional


class HearingImpairmentCheck(Module):
    """

    """

    def __init__(
        self,
        label: str = 'hearing_impairment_check',
        time_estimate_per_trial: float = 3.0,
    ):

        self.label = label
        self.elts = join(
            ModularPage(
                self.label,
                Prompt(
                    tags.div(
                        tags.h1('Hearing check'),
                        tags.p(
                            """
                            Do you have any kind of hearing impairment? 
                            (I.e., do you have problems with your hearing?)
                            """
                        )
                    )
                ),
                control=PushButtonControl(["Yes", "No"], arrange_vertically=False),
                time_estimate=time_estimate_per_trial,
            ),
            conditional(
                'hearing_impairment_check',
                lambda experiment, participant: participant.answer == 'Yes',
                UnsuccessfulEndPage(failure_tags=['hearing_impairment_check'])
            )
        )
        super().__init__(self.label, self.elts)


def experiment_requirements(
        time_estimate: float = 10
) -> InfoPage:
    """

    :param time_estimate:
    :return:
    """

    return InfoPage(
        tags.div(
            tags.h1('Experiment requirements'),
            tags.p(
                tags.strong('Location:'),
                tags.span(
                    """
                    This experiment requires you to be sitting in a quiet environment where you can clearly see your 
                    computer screen.
                    """
                )
            ),
            tags.p(
                tags.strong('Headphones:'),
                tags.span(
                    """
                    This experiment also requires you to wear headphones. 
                    Please ensure you have plugged yours in now.
                    """
                )
            ),
            tags.p(
                """
                The next page will play some test audio. Please turn down your volume before proceeding.
                """
            )
        ),
        time_estimate=time_estimate,
    )


def headphone_test_intro(
        time_estimate: float = 5
) -> InfoPage:
    """

    :param time_estimate:
    :return:
    """

    return InfoPage(
        tags.div(
            tags.h1('Headphone check'),
            tags.p(
                """
                We will now perform a short listening test to verify that your audio is working properly.
                This test will be difficult to pass unless you listen carefully over your headphones.
                Press 'Next' when you are ready to start.
                """
            )
        ),
        time_estimate=time_estimate
    )
