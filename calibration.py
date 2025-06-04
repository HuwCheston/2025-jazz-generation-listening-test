from dominate import tags

from psynet.page import VolumeCalibration, PageMaker
from psynet.modular_page import ModularPage, ImagePrompt, AudioPrompt, OptionControl, PushButton, Control, RadioButtonControl
from psynet.timeline import Event, Module, MediaSpec, FailedValidation


class AudioCalibration(VolumeCalibration):
    def __init__(
            self, audio: str, min_time: float = 2.5, time_estimate: float = 5
    ):
        super().__init__(
            url=audio,
            min_time=min_time,
            time_estimate=time_estimate
        )

    def text(self):
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


class AudioPromptMultiple(AudioPrompt):
    macro = "audio_multi"
    external_template = "custom-prompt.html"

    def __init__(self,  *args, **kwargs):
        self.definition = kwargs.pop("definition")
        self.all_audios = kwargs.pop("all_audio")
        super().__init__(*args, **kwargs)

    @property
    def media(self):
        return MediaSpec(
            audio={
                "anchor": self.all_audios["anchor"],
                "test_a": self.all_audios["test_a"],
                "test_b": self.all_audios["test_b"],
            }
        )

    @property
    def metadata(self):
        return {
            "text": str(self.text),
            "url": self.url,
            "play_window": self.play_window,
        } | self.definition


class AudioPromptCustom(AudioPrompt):
    def __init__(self,  *args, **kwargs):
        self.definition = kwargs.pop("definition")
        super().__init__(*args, **kwargs)

    @property
    def metadata(self):
        meta = {k: self.definition["metadata"][k] for k in ["condition_token", "similarity", "condition_type", "track_fpath"]}
        return {"text": str(self.text), "url": self.url, "play_window": self.play_window} | meta
