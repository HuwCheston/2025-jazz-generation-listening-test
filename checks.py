import os
import random

from dominate import tags

from psynet.modular_page import ModularPage, AudioPrompt, ImagePrompt, PushButtonControl, Prompt
from psynet.prescreen import HeadphoneTest
from psynet.page import InfoPage, SuccessfulEndPage, UnsuccessfulEndPage
from psynet.timeline import CodeBlock, PageMaker, join, Event, Module, conditional


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
