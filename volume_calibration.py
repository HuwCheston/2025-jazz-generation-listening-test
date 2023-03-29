import os
import random

from dominate import tags

from psynet.modular_page import ModularPage, AudioPrompt
from psynet.timeline import CodeBlock, PageMaker, join, Event, Module


def volume_calibration(min_time=2.5, time_estimate=5.0):
    text = tags.div()
    with text:
        tags.p(
            """
            Please listen to the following sound and adjust your
            computer's output volume until it is at a comfortable level.
            """
        )
        tags.p(
            """
            If you can't hear anything, there may be a problem with your
            playback configuration or your internet connection.
            You can refresh the page to try loading the audio again.
            """
        )

    # TODO: replace this sample audio with our actual output.mp3 file
    audio = "https://ia803105.us.archive.org/10/items/cd_portrait-in-jazz_bill-evans-trio_0/disc1/" \
            "07.%20Bill%20Evans%20Trio%20-%20What%20Is%20This%20Thing%20Called%20Love__sample.mp3"

    return ModularPage(
        "volume_calibration",
        AudioPrompt(audio, text, loop=True),
        events={"submitEnable": Event(is_triggered_by="trialStart", delay=min_time)},
        time_estimate=time_estimate,
    )
