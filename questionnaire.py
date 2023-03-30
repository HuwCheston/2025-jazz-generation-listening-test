from dominate import tags

from psynet.modular_page import ModularPage, TextControl
from psynet.demography.general import Age, Gender, CountryOfBirth, CountryOfResidence, FormalEducation
from psynet.demography.general import YearsOfFormalTraining, HoursOfDailyMusicListening, MoneyFromPlayingMusic
from psynet.page import InfoPage
from psynet.timeline import join


def introduction(
        time_estimate: float = 6
) -> InfoPage:
    """

    :param time_estimate:
    :return:
    """

    html = tags.div()
    with html:
        tags.h1(
            'Task component finished'
        )
        tags.p(
            """
            Congratulations, you completed the task component of this experiment!
            """
        )
        tags.p(
            """
            Before we finish, we just have a few more questions to ask you. 
            They should only take a couple of minutes to complete.
            """
        )
    return InfoPage(html, time_estimate=time_estimate)


def feedback(
        time_estimate: float = 10
) -> ModularPage:
    """

    :param time_estimate:
    :return:
    """

    return ModularPage(
        "feedback",
        "Do you have any feedback to give us about the experiment?",
        TextControl(one_line=False),
        bot_response="I am just a bot, I don't have any feedback for you.",
        save_answer="feedback",
        time_estimate=time_estimate,
    )


def questionnaire() -> list:
    """

    :return:
    """

    return join(
        introduction(),
        Age(),
        Gender(),
        CountryOfResidence(),
        CountryOfBirth(),
        FormalEducation(),
        YearsOfFormalTraining(),
        HoursOfDailyMusicListening(),
        MoneyFromPlayingMusic(),
        feedback(),
    )
