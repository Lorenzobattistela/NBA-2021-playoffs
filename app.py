from flask import Flask, render_template, request, redirect
import pandas as pd
import os

app = Flask(__name__)

dados = pd.read_csv('playoffs.csv')
default_table = dados.to_html(
    classes="table table-striped table-bordered table-hover", index=False)

teams = list(dados['Team'].drop_duplicates())
players = list(dados['Player'].drop_duplicates())


@app.route('/')
def home():
    return render_template("index.html", table=default_table, teams=teams)


@app.route('/search', methods=['POST', 'GET'])
def search():
    if request.method == 'POST':
        team = request.form.get('teams')
        stats = findTeamStats(team, dados)
        stats.drop(['#'], axis=1, inplace=True)
        stats = stats.to_html(
            open('templates/' + team + '.html', 'w'),
            classes="table table-striped table-bordered table-hover",
            index=False)
        filename = team + '.html'
        return render_template("search.html",
                               table=stats,
                               teams=teams,
                               file=filename,
                               players=players)

    else:
        return render_template("search.html",
                               teams=teams,
                               file='',
                               players=players)


def findTeamStats(team_short, dados):
    stats_index = dados['Team'] == team_short
    stats = dados[stats_index]
    stats.index = range(1, stats.shape[0] + 1)
    return stats


def findPlayerStats(name, dados):
    index = dados['Player'] == name
    stats = dados[index]
    stats.index = range(1, stats.shape[0] + 1)
    return stats