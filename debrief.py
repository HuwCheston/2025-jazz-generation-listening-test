from dominate import tags

from psynet.consent import NoConsent
from psynet.modular_page import ModularPage, CheckboxControl
from psynet.page import InfoPage
from psynet.timeline import Module, join


def debriefing(
        time_estimate: float = 20
) -> Module:
    debriefing_html = tags.div()
    with debriefing_html:
        tags.h1("Debriefing")
        tags.p(
            """
            Thank you for taking part in this experiment. 
            """
        )
        tags.p(
            """
            In this study, we are examining how musical performances can be coordinated successfully over the internet. 
            We are interested in understanding what happens when performances take place online (whether they slow down 
            or change tempo, for instance), as well as how successful listeners evaluate these performances to be.
            """
        )
        tags.p(
            """
            Thank you for helping us shed light on this section of music psychology.
            """
        )

        with tags.p():
            tags.strong("Contact for further information.")
            tags.span(
                """
                If you have any questions or concerns about this experiment, please contact Huw Cheston at 
                """
            )
            tags.a('hwc31@cam.ac.uk.', href='mailto:hwc31@cam.ac.uk')

    return Module(
        "debriefing",
        join(
            InfoPage(debriefing_html, time_estimate=time_estimate),
        )
    )
