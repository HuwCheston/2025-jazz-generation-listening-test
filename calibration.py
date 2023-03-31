from dominate import tags

from psynet.asset import CachedAsset, ExternalAsset
from psynet.page import VolumeCalibration, PageMaker
from psynet.modular_page import ModularPage, ImagePrompt, AudioPrompt
from psynet.timeline import Event, Module


class AudioCalibration(VolumeCalibration):
    """

    """
    def __init__(
            self, audio: str, min_time: float = 2.5, time_estimate: float = 5
    ):
        super().__init__(
            url=audio,
            min_time=min_time,
            time_estimate=time_estimate
        )

    def text(
            self
    ):
        return tags.div(
            tags.h1('Volume calibration'),
            tags.p(
                """
                Please listen to the following sound and adjust your
                computer's output volume until it is at a comfortable level.
                """
            ),
            tags.p(
                """
                If you can't hear anything, there may be a problem with your
                playback configuration or your internet connection.
                You can refresh the page to try loading the audio again.
                """
            )
        )


class BrightnessCalibration(Module):
    """

    """

    def __init__(
        self,
        image: str,
        min_time=2.5,
        time_estimate=5.0,
        id_="brightness_calibration",
    ):
        super().__init__(
            id_,
            self.page(min_time, time_estimate, id_),
            assets={
                "brightness_calibration_image": self.asset(image),
            },
        )

    def asset(self, url):
        if url.startswith("http"):
            return ExternalAsset(url=url)
        else:
            return CachedAsset(input_path=url)

    def page(self, min_time, time_estimate, id_):
        return PageMaker(
            lambda assets: ModularPage(
                id_,
                ImagePrompt(assets["brightness_calibration_image"], self.text(), height='100%', width='100%'),
                events={
                    "submitEnable": Event(is_triggered_by="trialStart", delay=min_time)
                },
            ),
            time_estimate=time_estimate,
        )

    def text(self):
        return tags.div(
            tags.h1('Brightness calibration'),
            tags.p(
                """
                Please adjust the brightness of your laptop or monitor until the individual colours in the image above
                can be distinguished from each other clearly.
                """
            )
        )
