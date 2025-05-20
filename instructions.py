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
                
                You will hear an initial performance, and then two subsequent performances. You will be asked to compare
                the second two performances to the first performance in response to several questions. For instance, 
                you might be asked to indicate which of the two performances are more similar to the first.
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


# def genres():
#     html = tags.div()
#     with html:
#         tags.h1("Jazz Genres")
#
#         with tags.p():
#             tags.span(
#                 """
#                 You will hear the following subgenres of jazz: "Avant-Garde", "Traditional", "Straight-Ahead",
#                 and "Global".
#                 """
#             )
#         with tags.p():
#             tags.strong('Avant-Garde Jazz')
#             tags.span(
#                 """
#                 is an experimental sub-genre that breaks conventional musical forms and harmonies,
#                 often embracing free improvisation and abstract expression. Example performers include
#                 Cecil Taylor and Keith Jarrett.
#                 """
#             )
#         with tags.p():
#             tags.strong('Traditional Jazz')
#             tags.span(
#                 """
#                 refers to the early styles of jazz such as New Orleans jazz and Dixieland,
#                 rooted in blues, ragtime, and brass band music. Example performers include Art Tatum and
#                 Teddy Wilson.
#                 """
#             )
#         with tags.p():
#             tags.strong('Straight-Ahead Jazz')
#             tags.span(
#                 """
#                 is an extension of the bebop jazz subgenre, maintaining a strong focus on swing rhythms
#                 and traditional harmonies. Example performers include Tommy Flanagan, Bill Evans, and
#                 Kenny Barron.
#                 """
#             )
#         with tags.p():
#             tags.strong('Global Jazz')
#             tags.span(
#                 """
#                 blends jazz with musical elements and rhythms from cultures around the world into a cross-cultural
#                 fusion. Example performers include Abdullah Ibrahim, Tete Montoliu, and Chick Corea.
#                 """
#             )
