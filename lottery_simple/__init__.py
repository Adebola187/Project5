from otree.api import *

import random

cu = Currency


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'lottery_simple'
    PLAYERS_PER_GROUP = None
    questions = ['Question', 'Question2', 'Question3']
    NUM_ROUNDS = 1

    payoff_hi = cu(4.00)
    payoff_lo = cu(0)
    payoff_hi2 = cu(30.00)
    payoff_mid = cu(0.5)
    payoff_lo2 = cu(0)
    payoff_2_hi = cu(5.00)
    payoff_2_lo = cu(1.4)
    probability_hi = 80
    probability_lo = 20
    sure_payoff = cu(3.2)
    payoff_hi3 = cu(7.20)
    payoff_mid3 = cu(0.45)
    payoff_lo3 = cu(0)
    payoff_3_hi = cu(4.00)
    payoff_3_mid3 = cu(3.4)
    payoff_3_lo = cu(2)


class Subsession(BaseSubsession):
    pass


def creating_session(subsession: Subsession):
    # if subsession.round_number == 1:
    # for p in subsession.get_players():
    #     round_numbers = list(range(1, C.NUM_ROUNDS + 1))
    #     random.shuffle(round_numbers)
    #     task_rounds = dict(zip(C.questions, round_numbers))
    #     p.participant.task_rounds = task_rounds

    for p in subsession.get_players():
        round_numbers = list(range(1, C.NUM_ROUNDS + 1))
        random.shuffle(round_numbers)
        selected_round = random.randint(1, C.NUM_ROUNDS)
        p.participant.selected_round = selected_round


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    Question = models.StringField(
        choices=[[
            ["Lottery 1: You have 80% chance to win 4 and 20% chance to win 0", 4, 0, '80%', '20%'],
            "Lottery 1: You have 80% chance to win 4 and 20% chance to win 0"],
            [["Lottery 2: You have 100% chance to win 3.2", 3.2, 3.2, '100%'],
             "Lottery 2: You have 100% chance to win 3.2"]],
        doc='Players decision', widget=widgets.RadioSelect
    )
    Question2 = models.StringField(
        choices=[[['Lottery 1: You have 10% chance to win 30; 40% chance to win 0.5 and 50% chance to win 0', 30, 0.5, 0, '10%', '40%', '50%'],
                  'Lottery 1: You have 10% chance to win 30, 40% chance to win 0.5 and 50% chance to win 0 ', ],
                 [['Lottery 2: You have 50% chance to win 5 and 50% chance to win 1.4', 5, 1.4, '50%', '50%'],
                  'Lottery 2: You have 50% chance to win 5, 50% chance to win 1.4', ]],
        doc='Players decision', widget=widgets.RadioSelect
    )
    Question3 = models.StringField(
        choices=[[['Lottery 1: You have 42% chance to win 7.2; 40% chance to win 0.45 and 18% chance to win 0', 7.2, 0.45, 0, '42%', '40%', '18%'],
                  'Lottery 1: You have 42% chance to win 7.2, 40% chance to win 0.45 and 18% chance to win 0', ],
                 [['Lottery 2: You have 40% chance to win 4; 40% chance to win 3.4 and 20% chance to win 2', 4, 3.4, 2, '40%', '40%', '20%'],
                  'Lottery 2: You have 40% chance to win 4, 40% chance to win 3.4 and 20% chance to win 2']],
        doc='Players decision', widget=widgets.RadioSelect,
    )
    selected_round = models.IntegerField()
    choice = models.IntegerField()
    choice_in_round = models.StringField()
    answer = models.FloatField()
    random_num_prob = models.IntegerField()


# PAGES
class Introduction(Page):
    form_model = 'player'

    def is_displayed(player: Player):
        return player.round_number == 1

# create dict for answers to each question
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.session.answers = {0: "0", 1: "1", 2: "2", 3: "3", 4: "4", }


class Question(Page):
    form_model = 'player'
    form_fields = ['Question']

    # @staticmethod
    # def is_displayed(player: Player):
    #     participant = player.participant
    #
    #     return player.round_number == participant.task_rounds['Question']

    @staticmethod
    def vars_for_template(player: Player):
        return dict(player_in_rounds=player.in_rounds(1, C.NUM_ROUNDS))

# create dict for payoff for each question
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.choice = player.in_rounds(1, C.NUM_ROUNDS) == player.Question
        choice = {player.Question: player.in_rounds(1, C.NUM_ROUNDS)}
        print(choice)
        player.session.answers[1] = player.Question


class Question2(Page):
    form_model = 'player'
    form_fields = ['Question2']

    # @staticmethod
    # def is_displayed(player: Player):
    #     participant = player.participant
    #
    #     return player.round_number == participant.task_rounds['Question2']

    @staticmethod
    def vars_for_template(player: Player):
        return dict(player_in_rounds=player.in_rounds(1, C.NUM_ROUNDS))

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.session.answers[2] = player.Question2


class Question3(Page):
    form_model = 'player'
    form_fields = ['Question3']

    # @staticmethod
    # def is_displayed(player: Player):
    #     participant = player.participant
    #
    #     return player.round_number == participant.task_rounds['Question3']

    @staticmethod
    def vars_for_template(player: Player):
        return dict(player_in_rounds=player.in_rounds(1, C.NUM_ROUNDS))

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.session.answers[3] = player.Question3

    @staticmethod
    def app_after_this_page(player: Player, upcoming_apps):
        player.session.answers[3] = player.Question3
        import random
        participant = player.participant
        if player.round_number == C.NUM_ROUNDS:
            random_round = random.randint(1, 3)
            participant.selected_round = random_round
            player.selected_round = random_round

        # if participant.selected_round == 1:
        #     player.choice_in_round = player.Question
        # elif participant.selected_round == 2:
        #     player.choice_in_round = player.Question2
        # else:
        #     player.choice_in_round = player.Question3


def replacechar(self):
    return self.replace("%", "").replace("'", "").replace("[", "").replace("]", "").replace(" ", "")


class Results(Page):
    form_model = 'player'

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS

    # @staticmethod
    # def replacechar(self):
    #     return self.replace("%", "").replace("'", "").replace("[", "").replace("]", "").replace(" ", "")
    #
    @staticmethod
    def vars_for_template(player: Player):
        probability = random.randint(1, 100)
        random_num_pay = probability
        player.random_num_prob = random_num_pay
        split = player.session.answers[player.participant.selected_round].split(",")
        if len(split) == 7:
            index = 4
        elif len(split) == 5:
            index = 3
        else:
            index = 5
        if split[3] == "100%":
            answer = split[1].replace("[", "").replace("]", "")
        elif len(split) == 5 and probability <= int(
                split[index].replace("%", "").replace("'", "").replace(" ' ", "").replace("[", "").replace("]", "")):
            answer = split[1].replace("[", "").replace("]", "")
        elif len(split) == 5 and probability >= int(
                split[index].replace("%", "").replace("'", "").replace(" ' ", "").replace("[", "").replace("]", "")):
            answer = split[2].replace("[", "").replace("]", "")
        # elif len(split) == 5 and probability >= (int(replacechar(split[index])) + int(replacechar(split[++index]))):
        #     answer = split[2].replace("[", "").replace("]", "")
        elif len(split) == 7 and probability <= int(
                split[++index].replace("%","").replace ("'", "").replace("[", "").replace("]", "").replace(" ","")):
            answer = split[1].replace("[", "").replace("]", "")
        elif len(split) == 7 and int(
                split[++4].replace("%", "").replace("'", "").replace("[", "").replace("]", "").replace(" ",
                                                                                                       "")) <= probability <= (int(replacechar(split[++4])) + int(replacechar(split[++5]))):
            answer = split[2].replace("[", "").replace("]", "")
        elif len(split) == 7 and probability >= (int(replacechar(split[++4])) + int(replacechar(split[++5]))):
                # >= int(split[+++5].replace("%", "").replace("'", "").replace("'", "").replace("[", "").replace("]","").replace(" ","")):
            answer = split[3].replace("[", "").replace("]", "")
        else:
            answer = 3.2
        player.payoff = answer

        return {
            "answer": player.payoff,
            "question": player.session.answers[player.participant.selected_round].split(",")[0].replace("[", "").replace("'", " ").replace( ";", ","),
            "info": player.session.answers[player.participant.selected_round],
            "probability_number": random_num_pay,
        }


class Results2(Page):
    form_model = 'player'

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS




page_sequence = [Introduction, Question,Question2, Question3, Results]
