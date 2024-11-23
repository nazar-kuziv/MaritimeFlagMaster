from datetime import datetime

import matplotlib.pyplot as plt

from logic.environment import Environment


class Session:
    def __init__(self, number_of_questions):
        self.number_of_questions = number_of_questions
        self.number_of_correct_answers = 0
        self.current_question = 0

    def get_statistics(self):
        number_of_wrong_answers = self.number_of_questions - self.number_of_correct_answers

        fig, ax = plt.subplots()
        fig.set_facecolor("#ffffff")

        wedges, text, autotext = ax.pie([self.number_of_correct_answers, number_of_wrong_answers],
                                        colors=['#59e8b5', '#ff983a'], startangle=90, autopct='%1.1f%%')
        for text in autotext:
            text.set_visible(False)
        plt.setp(wedges, width=0.25)
        ax.set_aspect("equal")
        plt.tight_layout()
        # plot_img_path = Environment.resource_path('static/tmp/' + Session._generate_filename_for_statistics())
        # plt.savefig(plot_img_path, format='png', dpi=600, transparent=True)
        return fig

    def get_procent_of_correct_answers(self):
        return round((self.number_of_correct_answers / self.number_of_questions)*100)

    @staticmethod
    def _generate_filename_for_statistics():
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S%f')
        return f'{timestamp}.png'
