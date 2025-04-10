import plotly.express as px
import pandas as pd
from collections import Counter
from numpy import nan
import matplotlib.pyplot as plt


def filtered_counter(answers):
    result = dict(Counter(answers))
    if nan in result:
        result.pop(nan)
    return result


def percentage_format(x):
    return f"{x:.2f}%"


def has_multiple_choices(answers_counts):
    return any(";" in key for key in answers_counts)


def show_bar_chart(answers_counts):
    singles_answers_counts = dict()
    for key, value in answers_counts.items():
        single_answers = key.split(";")
        for a in single_answers:
            singles_answers_counts[a] = singles_answers_counts.get(a, 0) + value
    plt.bar(
        x=singles_answers_counts.keys(),
        height=singles_answers_counts.values()
    )


def main():
    data_frame = pd.read_csv("assets/data.csv")
    # On enlève la colonne Horodateur
    # Le tilde correspond au complémentaire
    all_answers = data_frame.loc[:, ~data_frame.columns.isin(["Horodateur"])]
    #all_answers = data_frame.loc[:]
    plt.title("Résultats")
    for question, answers in all_answers.items():
        answers_counts = filtered_counter(answers)
        # Certaines questions son décomposées en "questions fragmentées",
        # donc on les filtre pour le moment.
        # Ces fragments contiennent des bouts de réponse comme "[Logs]"
        if "[" in question:
            continue
        if has_multiple_choices(answers_counts):
            show_bar_chart(answers_counts)
        else:
            # index_line, index_columns = divmod(i, columns)
            # axes[index_line, index_columns].set_title(question)
            # axes[index_line, index_columns].pie(answers_counts.values(), labels=answers_counts.keys())
            plt.pie(answers_counts.values(), labels=answers_counts.keys(), autopct=percentage_format, shadow=True)
        plt.title(question)
        plt.show()


if __name__ == "__main__":
    main()
