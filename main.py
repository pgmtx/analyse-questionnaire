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
    open_questions = (
        "According to you, why?",
        "Do you take measures to protect your data when you connect to your LMS? If so, which ones?"
    )

    for i, (question, answers) in enumerate(all_answers.items()):
        answers_counts = filtered_counter(answers)
        # Certaines questions son décomposées en "questions fragmentées",
        # donc on les filtre pour le moment.
        # Ces fragments contiennent des bouts de réponse comme "[Logs]"
        if "[" in question:
            continue

        if "example" in question or question in open_questions:
            with open(f"output/question{i+1}.txt", 'w') as file:
                file.write(f"Question : {question}\n\n")
                file.write('\n'.join('- ' + key for key in answers_counts.keys()))
            continue

        print(question)
        if has_multiple_choices(answers_counts):
            plt.figure(figsize=(13, 7))
            plt.title(question)
            plt.tight_layout()
            show_bar_chart(answers_counts)
        else:
            plt.figure(figsize=(12, 7))
            plt.title(question)
            plt.tight_layout()
            plt.pie(answers_counts.values(), labels=answers_counts.keys(), autopct=percentage_format, shadow=True)
        plt.savefig(f"output/question{i+1}.png")
        plt.close()


if __name__ == "__main__":
    main()
