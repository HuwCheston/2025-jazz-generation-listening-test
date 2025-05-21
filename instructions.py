from dominate import tags

from psynet.page import InfoPage


def instructions():
    html = tags.div()

    with html:
        tags.h1("Experiment instructions")

        with tags.p():
            tags.strong('Description:')
            tags.span(
                """
                In this experiment, you will listen to multiple piano performances.
                
                You will hear an initial performance 
                """
            )
            tags.strong("(the anchor), ")
            tags.span("and then two subsequent performances")
            tags.strong("(A and B).")

        with tags.p():
            tags.strong("Task:")
            tags.span(
                """
                You will be asked several questions about the performances.
                For instance, you might be asked to indicate which of A or B sounded more like the anchor.
                You may also be asked to indicate which of A or B you enjoyed more.
                """
            )

        with tags.p():
            tags.strong('Advice:')
            tags.em(
                """
                There are no right or wrong answers:
                """
            )
            tags.span(
                """
                give us your overall impression of the performances you just heard and try to be consistent 
                with how you answer. 
                """
            )
            with tags.ul():
                tags.li(
                    """
                    Take as much time as you need to answer the questions.
                    """
                )
                tags.li(
                    """
                    Some performances may sound unusual, but you should do the best to complete the task regardless.
                    """
                )
                tags.li(
                    """
                    When rating a performance, try to focus on the quality of the musical composition and not on the 
                    quality of the virtual instruments or the music production mix.
                    """
                )
                tags.li(
                    """
                    When you cannot perceive any differences between the two performances, you can indicate "No Preference".
                    However, we encourage you to try and take a stand and choose one of the two performances wherever 
                    possible.
                    """
                )

        tags.p(
            """
            Press 'Next' when you are ready to continue.
            """
        )

    return InfoPage(html, time_estimate=15)
