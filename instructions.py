from dominate import tags

from psynet.page import InfoPage


def instructions():
    html = tags.div()

    with html:
        tags.h1("Experiment  instructions")

        with tags.p():
            tags.strong('Description:')
            tags.span(
                """
                In this experiment, you will listen to and watch a series of musical performances by different pianists 
                and drummers. You will see the pianist on the left side of your screen and the drummer on the right. 
                Both musicians were performing together over the Internet and were improvising, meaning that they 
                were making the music up on-the-spot.
                """
            )

        with tags.p():
            tags.strong('Task:')
            tags.span(
                """
                After listening to each performance, you will be asked to rate how successful you think it was. 
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
                give us your overall impression of the performance you just heard and try to be consistent 
                with how you answer. 
                """
            )
            with tags.ul():
                tags.li(
                    """
                    When making your judgement, you might want to watch the video as well as listen to the audio. 
                    """
                )
                tags.li(
                    """
                    Take as much time as you need to answer the question after each performance.
                    """
                )
                tags.li(
                    """
                    Some performances may sound unusual, but you should do your best to complete the task regardless.
                    """
                )

        with tags.p():
            tags.strong('Bonuses:')
            tags.span(
                """
                We will monitor the answers you give throughout the experiment, and will give a small additional bonus
                if you give high-quality and reliable responses. Listen and watch carefully and give it your best shot!
                """
            )

        tags.p(
            """
            Press 'Next' when you are ready to continue.
            """
        )

    return InfoPage(html, time_estimate=15)
