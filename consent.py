from dominate import tags

from psynet.consent import NoConsent
from psynet.modular_page import ModularPage, CheckboxControl
from psynet.page import InfoPage
from psynet.timeline import Module, join

information_sheet = tags.div()

with information_sheet:
    tags.h1("Information sheet")
    tags.p(
        """
        Before you decide to take part in this study it is important for you to understand why the research is being 
        done and what it will involve. Please take time to read the following information carefully and discuss it with
        others if you wish.
        """
    )
    with tags.p():
        tags.strong("Purpose of the study.")
        tags.span(
            """
            Anyone who has ever watched a group of people create music together knows that it often involves a great 
            deal of coordination and communication between the performers. As music psychologists, we want to 
            understand the strategies that underpin successful musical interaction. In this particular experiment, we 
            are studying how musicians can successfully perform together over the internet.
            """
        )

    with tags.p():
        tags.strong("Do I have to take part?")
        tags.span(
            """
            Taking part is entirely voluntary. Refusal or withdrawal will involve no penalty or loss, now or in the
            future.
            """
        )

    with tags.p():
        tags.strong("How long does the experiment last?")
        tags.span(
            """
            The full experiment should last approximately 15 minutes, though individual times will vary, and your
            experiment may end early depending on various factors.
            """
        )


# with pages[1]:
    with tags.p():
        tags.strong("Benefits of taking part.")
        tags.span(
            """
            Completing the entire experiment earns you a payment of approximately £2.50. This fee is calculated by
            multiplying a notional hourly rate of £10.00/hour by the estimated duration of the experiment. However,
            please note the following:
            """
        )
        with tags.ul():
            tags.li(
                """
                Taking the experiment more slowly does not earn you a greater total payment. The total payment is fixed
                according to the 
                """,
                tags.em("estimated"),
                " duration of the experiment",
            )

            tags.li(
                """
                Your experiment could end early for a number of reasons, including but not limited to technical failure
                and task performance. In this case you will be compensated pro rata for the portion of the experiment
                that you completed.
                """
            )

    with tags.p():
        tags.strong("What is the procedure?")
        tags.span(
            """
            The experiment takes place in your web browser. You will be asked to perform simple tasks using your
            keyboard or mouse while listening to sounds and watching videos.
            """
        )

    with tags.p():
        tags.strong("Risks of taking part.")
        tags.span(
            """
            There are no risks involved beyond those associated with normal computer use.
            """
        )

    with tags.p():
        tags.strong("Confidentiality.")
        tags.span(
            """
            No personal details (e.g. name, contact data) will be collected at any stage, so your data will be anonymous
            throughout. This anonymous data may eventually be shared in public data repositories, conferences, and
            scientific journals.
            """
        )

    with tags.p():
        tags.strong("Ethical review.")
        tags.span(
            """
            The project has been approved by the University of Cambridge Faculty of Music Ethics Committee.
            """
        )

    with tags.p():
        tags.strong("Contact for further information.")
        tags.span(
            """
            If you have further queries about this experiment, please contact Huw Cheston at hwc31@cam.ac.uk.
            """
        )


consent_form = tags.div()

with consent_form:
    tags.h1("Consent form")

    tags.p(
        tags.em(
            """
            Please read the following text and select ‘Agree’ if you consent to these terms.
            """
        )
    )

    tags.p(
        """
        I have been informed about the procedures to be used in this experiment and the tasks I need to perform, and I
        have agreed to take part. I understand that taking part in this experiment is voluntary and I can withdraw from
        the experiment at any time.
        """
    )

    tags.p(
        """
        I understand that the data collected in this testing session will be stored on electronic media or on paper and
        it may contribute to scientific publications and presentations. I agree that the data can be made available
        anonymously for other researchers, both inside and outside the Centre for Music and Science and Faculty of
        Music. These data will not be linked to me as an individual.
        """
    )

consent = Module(
    "consent",
    join(
        NoConsent(),
        InfoPage(information_sheet, time_estimate=5),
        ModularPage(
            "consent_form",
            consent_form,
            CheckboxControl(
                choices=["I agree"],
                force_selection=True,
            ),
            time_estimate=10,
        ),
    )
)
