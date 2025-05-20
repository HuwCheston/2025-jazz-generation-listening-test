import random

from dominate import tags
from typing import Dict, List, Optional, Union

from psynet.asset import CachedAsset, ExternalAsset
from psynet.page import VolumeCalibration, PageMaker
from psynet.modular_page import ModularPage, ImagePrompt, AudioPrompt, OptionControl, PushButton, Control, RadioButtonControl
from psynet.timeline import Event, Module, MediaSpec, FailedValidation
from psynet.utils import NoArgumentProvided, linspace, get_translator


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
                ImagePrompt(assets["brightness_calibration_image"], self.text(), height="200px", width="600px"),
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


class CustomSlider(Control):
    macro = "custom_slider"
    external_template = "custom-control.html"

    def __init__(
        self,
        start_value: float,
        min_value: float,
        max_value: float,
        n_steps: int = 10000,
        include_labels: Optional[bool] = True,
        label_step: Optional[int] = 1,
        reverse_scale: Optional[bool] = False,
        directional: Optional[bool] = True,
        slider_id: Optional[str] = "sliderpage_slider",
        input_type: Optional[str] = "HTML5_range_slider",
        random_wrap: Optional[bool] = False,
        snap_values: Optional[Union[int, list]] = None,
        minimal_interactions: Optional[int] = 0,
        minimal_time: Optional[int] = 0,
        continuous_updates: Optional[bool] = False,
        template_filename: Optional[str] = None,
        template_args: Optional[Dict] = None,
        bot_response=NoArgumentProvided,
    ):
        super().__init__(bot_response)

        # if include_labels is not False and (max_value - min_value) % (label_step - 1) != 0:
        #     raise ValueError(
        #         "Slider label step must XXXXX"
        #     )

        if snap_values is not None and input_type == "circular_slider":
            raise ValueError(
                "Snapping values is currently not supported for circular sliders, set snap_values=None"
            )
        if input_type == "circular_slider" and reverse_scale:
            raise NotImplementedError(
                "Reverse scale is currently not supported for circular sliders, set reverse_scale=False"
            )

        self.start_value = start_value
        self.min_value = min_value
        self.max_value = max_value
        self.include_labels = include_labels
        self.label_step = label_step
        self.n_steps = n_steps
        self.step_size = (max_value - min_value) / (n_steps - 1)
        self.reverse_scale = reverse_scale
        self.directional = directional
        self.slider_id = slider_id
        self.input_type = input_type
        self.random_wrap = random_wrap
        self.template_filename = template_filename
        self.template_args = template_args
        self.minimal_time = minimal_time

        self.snap_values = self.format_snap_values(
            snap_values, min_value, max_value, n_steps
        )

        js_vars = {}
        js_vars["snap_values"] = self.snap_values
        js_vars["minimal_interactions"] = minimal_interactions
        js_vars["continuous_updates"] = continuous_updates
        self.js_vars = js_vars

    def format_snap_values(self, snap_values, min_value, max_value, n_steps):
        if snap_values is None:
            return snap_values
            # return linspace(min_value, max_value, n_steps)
        elif isinstance(snap_values, int):
            return linspace(min_value, max_value, snap_values)
        else:
            for x in snap_values:
                assert isinstance(x, (float, int))
                assert x >= min_value
                assert x <= max_value
            return sorted(snap_values)

    def validate(self, response, **kwargs):
        if self.max_value <= self.min_value:
            raise ValueError("`max_value` must be larger than `min_value`")

        if self.start_value > self.max_value or self.start_value < self.min_value:
            raise ValueError(
                "`start_value` (= %f) must be between `min_value` (=%f) and `max_value` (=%f)"
                % (self.start_value, self.min_value, self.max_value)
            )

        if self.js_vars["minimal_interactions"] < 0:
            raise ValueError("`minimal_interactions` cannot be negative!")

    @property
    def metadata(self):
        return {
            "start_value": self.start_value,
            "min_value": self.min_value,
            "max_value": self.max_value,
            "include_labels": self.include_labels,
            "label_step": self.label_step,
            "n_steps": self.n_steps,
            "step_size": self.step_size,
            "reverse_scale": self.reverse_scale,
            "directional": self.directional,
            "slider_id": self.slider_id,
            "input_type": self.input_type,
            "random_wrap": self.random_wrap,
            "template_filename": self.template_filename,
            "template_args": self.template_args,
            "js_vars": self.js_vars,
        }

    def update_events(self, events):
        events["sliderMinimalTime"] = Event(
            is_triggered_by="trialStart", delay=self.minimal_time
        )
        events["submitEnable"].add_triggers(
            "sliderMinimalInteractions", "sliderMinimalTime"
        )

    def get_bot_response(self, experiment, bot, page, prompt):
        import numpy as np

        equidistant = not isinstance(self.snap_values, list)
        if equidistant:
            if self.snap_values:
                n_candidates = self.snap_values
            else:
                n_candidates = self.n_steps
            candidates = list(
                np.linspace(self.min_value, self.max_value, num=n_candidates)
            )
        else:
            candidates = self.snap_values
        return random.sample(candidates, 1)[0]


class AudioPromptMultiple(AudioPrompt):
    macro = "audio_multi"
    external_template = "custom-prompt.html"

    def __init__(self,  *args, **kwargs):
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


class RadioButtonMultiple(RadioButtonControl):
    macro = "radiobuttons_multi"
    external_template = "custom-control.html"

    def validate(self, response, **kwargs):
        _p = get_translator(context=True)
        print(response.answer, response.__dict__)
        if self.force_selection and response.answer is None:
            return FailedValidation(_p("validation", "You need to select an answerasdfasdga!"))
        return None

    def format_answer(self, raw_answer, **kwargs):
        print(raw_answer)
        return super().format_answer(raw_answer, **kwargs)
