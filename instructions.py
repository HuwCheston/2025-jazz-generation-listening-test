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
                In this experiment, you will listen to different styles of jazz played on the piano.
                
                Some are real performances, and others are generated with artificial intelligence.
                """
            )

        with tags.p():
            tags.strong("Task:")
            tags.span(
                """
                You will be asked several questions about each performance.
                For instance, you might be asked to rate how creative or diverse the performance was, or to 
                suggest a potential style of jazz for the performance.
                """
            )

        with tags.p():
            tags.strong("Genres:")
            tags.span(
                """
                You will hear three different styles of jazz during the experiment.
                """
            )
            with tags.ul():
                tags.li(
                    """
                    Avant-Garde: this might include performances by pianists like Paul Bley and Geri Allen
                    """
                )
                tags.li(
                    """
                    Mainstream or "Straight-Ahead": this might include performances by pianists like Oscar Peterson and Bill Evans
                    """
                )
                tags.li(
                    """
                    Traditional & Early: this might include performances by pianists like Art Tatum and Teddy Wilson
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
                    Some performances may start and end abruptly. This is normal and you should not let it affect your ratings.
                    """
                )
                tags.li(
                    """
                    When rating a performance, try to focus on the quality of the musical composition and not on the 
                    quality of the virtual instruments or the music production mix.
                    """
                )

        tags.p(
            """
            Press 'Next' when you are ready to continue.
            """
        )

    return InfoPage(html, time_estimate=15)
