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


def main():
    # data_frame = pd.DataFrame(dict(
    #     r=[1, 5, 2, 2, 3],
    #     theta=["Early access to documents","Data security","Browsing speed",
    #        "Mobile compatibility", "Design and ergonomics"]
    # ))
    # figure = px.line_polar(data_frame, r="r", theta="theta", line_close=True)
    # figure.show()
    data_frame = pd.read_csv("assets/data.csv")
    # On enlève la colonne Horodateur
    # tilde = complémentaire
    all_answers = data_frame.loc[:, ~data_frame.columns.isin(["Horodateur"])]

    plt.title("Résultats")
    for i, (question, answers) in enumerate(all_answers.items()):
        answers_counts = filtered_counter(answers)
        # Certaines questions son décomposées en "questions fragmentées",
        # donc on les filtre pour le moment.
        # Ces fragments contiennent des bouts de réponse comme "[Logs]"
        if "[" in question or any(";" in key for key in answers_counts):
            continue
        if i > 3:
            break

        # index_line, index_columns = divmod(i, columns)
        # axes[index_line, index_columns].set_title(question)
        # axes[index_line, index_columns].pie(answers_counts.values(), labels=answers_counts.keys())
        plt.title(question)
        plt.pie(answers_counts.values(), labels=answers_counts.keys(), autopct=percentage_format, shadow=True)
        plt.show()


if __name__ == "__main__":
    main()
