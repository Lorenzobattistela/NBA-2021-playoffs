from flask import Flask, render_template, request, redirect
import pandas as pd
import os

app = Flask(__name__)

dados = pd.read_csv('playoffs.csv')
default_table = dados.to_html(
    classes="table table-striped table-bordered table-hover", index=False)

teams = list(dados['Team'].drop_duplicates())
players = list(dados['Player'].drop_duplicates())
filenames = []


@app.route('/')
def home():
    eraseHTMLfiles()
    return render_template("index.html", table=default_table, teams=teams)


@app.route('/search', methods=['POST', 'GET'])
def search():
    if request.method == 'POST':
        team = request.form.get('teams')
        if team:
            stats = findTeamStats(team, dados)
            stats.drop(['#'], axis=1, inplace=True)
            stats = stats.to_html(
                open('templates/' + team + '.html', 'w'),
                classes="table table-striped table-bordered table-hover",
                index=False)
            filename = team + '.html'
            filenames.append(filename)
            return render_template("search.html",
                                   table=stats,
                                   teams=teams,
                                   file=filename,
                                   players=players)
        player = request.form.get('player')
        if player:
            stats = findPlayerStats(player, dados)
            stats.drop(['#'], axis=1, inplace=True)
            stats = stats.to_html(
                open('templates/' + player + '.html', 'w'),
                classes="table table-striped table-bordered table-hover",
                index=False)
            filename = player + '.html'
            filenames.append(filename)
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


@app.route('/compare', methods=['POST', 'GET'])
def compare():
    if request.method == 'POST':
        firstPlayer = request.form.get('firstPlayer')
        secondPlayer = request.form.get('secondPlayer')
        firstPlayerStats = findPlayerStats(firstPlayer, dados)
        secondPlayerStats = findPlayerStats(secondPlayer, dados)
        firstPlayerStats.drop(['#'], axis=1, inplace=True)
        secondPlayerStats.drop(['#'], axis=1, inplace=True)
        comparedStats = firstPlayerStats.compare(secondPlayerStats,
                                                 align_axis=0)
        comparedStats = comparedStats.to_html(
            open('templates/' + firstPlayer + secondPlayer + '.html', 'w'),
            classes="table table-striped table-bordered table-hover",
            index=False)
        filename = firstPlayer + secondPlayer + '.html'
        filenames.append(filename)
        return render_template("compare.html",
                               table=comparedStats,
                               players=players,
                               file=filename)
    else:
        return render_template("compare.html", players=players, file='')


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


def eraseHTMLfiles():
    for file in filenames:
        os.remove('templates/' + file)