import requests
from utils import *

API_KEY = ''
SPORT = 'upcoming'  # use the sport_key from the /sports endpoint below, or use 'upcoming' to see the next 8 games across all sports
REGIONS = 'eu'  # uk | us | eu | au. Multiple can be specified if comma delimited
MARKETS = 'h2h'  # h2h | spreads | totals. Multiple can be specified if comma delimited
ODDS_FORMAT = 'decimal'  # decimal | american
DATE_FORMAT = 'iso'  # iso | unix


def arb(odds, stake=100):
    """
    Takes in the JSON API request and calculates if there are any arbitrage opportunities. It looks for arbitrage in the current LIVE
    events and the 8 closest upcoming events from all the sports and bookies supported by the https://the-odds-api.com/.

        Parameters:
            stake: How much to play
            odds (dict): JSON dictionary returned from API call with all the betting data

        Returns:
            arb_list (list[dict]): list of dictionaries for each sport event in which arbitrage is possible with bookies, odds,
                                    payoff and betting strategy
    """
    arb_matrices = create_arb_matrices(odds)
    arb_list = []
    for arb_matrix in arb_matrices:
        arb_ = calc_arb(arb_matrix, stake)
        if arb_['arbitrage']:
            arb_list.append(arb_)
    if len(arb_list) == 0:
        return None
    return arb_list


def get_odds():

    odd_response = requests.get(f"https://api.the-odds-api.com/v4/sports/{SPORT}/odds", params={
        'api_key': API_KEY,
        'regions': REGIONS,
        'markets': MARKETS,
        'oddsFormat': ODDS_FORMAT,
        'dateFormat': DATE_FORMAT,
    })

    if odd_response.status_code != 200:
        print(
            f'Failed to get odds: status_code {odd_response.status_code}, response body {odd_response.text}')
        return

    else:
        odds_json = odd_response.json()
        return odds_json
