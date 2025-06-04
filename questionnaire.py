from dominate import tags

from psynet.modular_page import ModularPage, TextControl, RadioButtonControl
from psynet.demography.general import YearsOfFormalTraining, Age, Gender, CountryOfBirth, CountryOfResidence, HoursOfDailyMusicListening, MoneyFromPlayingMusic
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
            If you want, you will also be able to provide your email to be entered into the prize draw.
            """
        )
    return InfoPage(html, time_estimate=time_estimate)

def jazz_experience(
        time_estimate: float = 10
) -> ModularPage:
    """

    :param time_estimate:
    :return:
    """
    return ModularPage(
        "jazz_experience",
        prompt="How often do you listen to or perform jazz?",
        control=RadioButtonControl(
            [
                "frequently",
                "sometimes",
                "never",
            ],
            [
                "Frequently",
                "Sometimes",
                "Never",
            ],
            name="jazz_experience_control",
        ),
        bot_response="I am just a bot, I don't understand jazz",
        save_answer="jazz_experience",
        time_estimate=time_estimate,
    )


def recognise_assessment(
        time_estimate: float = 10
) -> ModularPage:
    """

    :param time_estimate:
    :return:
    """

    return ModularPage(
        "recognise_feedback",
        "Did you recognise any of the performances you listened to?",
        TextControl(one_line=False),
        bot_response="I am just a bot, I don't understand jazz",
        save_answer="recognise_feedback",
        time_estimate=time_estimate,
    )


def similarity_assessment(
        time_estimate: float = 10
) -> ModularPage:
    """

    :param time_estimate:
    :return:
    """

    return ModularPage(
        "similarity_feedback",
        "When selecting the genre that best matched the performance, what did you listen for?",
        TextControl(one_line=False),
        bot_response="I am just a bot, I can't listen.",
        save_answer="similarity_feedback",
        time_estimate=time_estimate,
    )



def feedback(
        time_estimate: float = 10
) -> ModularPage:
    """

    :param time_estimate:
    :return:
    """

    return ModularPage(
        "feedback",
        "Do you have any other feedback to give us about the experiment?",
        TextControl(one_line=False),
        bot_response="I am just a bot, I don't have any feedback for you.",
        save_answer="feedback",
        time_estimate=time_estimate,
    )


def prize_draw_email(
        time_estimate: float = 10
) -> ModularPage:
    """

    :param time_estimate:
    :return:
    """

    return ModularPage(
        "email",
        "If you want to be entered into the prize draw to win the £50 Amazon voucher, please enter a contact email "
        "address below. The prize will be randomly awarded to one participant once the study has ended. If you do not "
        "wish to be entered into the draw, please leave the box blank.",
        TextControl(one_line=True, block_copy_paste=True, height=None),
        bot_response="I am just a bot, I don't have an email.",
        save_answer="email",
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
        CountryOfBirth(),
        CountryOfResidence(),
        YearsOfFormalTraining(),
        HoursOfDailyMusicListening(),
        MoneyFromPlayingMusic(),
        jazz_experience(),
        recognise_assessment(),
        similarity_assessment(),
        feedback(),
        prize_draw_email(),
    )
