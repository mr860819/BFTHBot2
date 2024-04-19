states_ids = {
        'Alabama': 1,
        'Alaska': 2,
        'Arizona': 3,
        'Arkansas': 4,
        'California': 5,
        'Colorado': 6,
        'Connecticut': 7,
        'Delaware': 8,
        'Florida': 9,
        'Georgia': 10,
        'Hawaii': 11,
        'Idaho': 12,
        'Illinois': 13,
        'Indiana': 14,
        'Iowa': 15,
        'Kansas': 16,
        'Kentucky': 17,
        'Louisiana': 18,
        'Maine': 19,
        'Maryland': 20,
        'Massachusetts': 21,
        'Michigan': 22,
        'Minnesota': 23,
        'Mississippi': 24,
        'Missouri': 25,
        'Montana': 26,
        'Nebraska': 27,
        'Nevada': 28,
        'New Hampshire': 29,
        'New Jersey': 30,
        'New Mexico': 31,
        'New York': 32,
        'North Carolina': 33,
        'North Dakota': 34,
        'Ohio': 35,
        'Oklahoma': 36,
        'Oregon': 37,
        'Pennsylvania': 38,
        'Rhode Island': 39,
        'South Carolina': 40,
        'South Dakota': 41,
        'Tennessee': 42,
        'Texas': 43,
        'Utah': 44,
        'Vermont': 45,
        'Virginia': 46,
        'Washington': 47,
        'West Virginia': 48,
        'Wisconsin': 49,
        'Wyoming': 50,
        'Washington D.C.': 51,
        'Puerto Rico': 52
    }
state_abbvs = {
    "AL": 1,
    "AK": 2,
    "AZ": 3,
    "AR": 4,
    "CA": 5,
    "CO": 6,
    "CT": 7,
    "DE": 8,
    "FL": 9,
    "GA": 10,
    "HI": 11,
    "ID": 12,
    "IL": 13,
    "IN": 14,
    "IA": 15,
    "KS": 16,
    "KY": 17,
    "LA": 18,
    "ME": 19,
    "MD": 20,
    "MA": 21,
    "MI": 22,
    "MN": 23,
    "MS": 24,
    "MO": 25,
    "MT": 26,
    "NE": 27,
    "NV": 28,
    "NH": 29,
    "NJ": 30,
    "NM": 31,
    "NY": 32,
    "NC": 33,
    "ND": 34,
    "OH": 35,
    "OK": 36,
    "OR": 37,
    "PA": 38,
    "RI": 39,
    "SC": 40,
    "SD": 41,
    "TN": 42,
    "TX": 43,
    "UT": 44,
    "VT": 45,
    "VA": 46,
    "WA": 47,
    "WV": 48,
    "WI": 49,
    "WY": 50,
    "DC": 51,
    "PR": 52
}
def switch_state_to_id(state):
    state_id = str(states_ids[state])
    return state_id

def switch_abbv_to_id(abbv):
    state_id = state_abbvs.get(abbv.upper())
    return state_id

def switch_id_to_state_name(id):
    state_name = next((key for key, value in states_ids.items() if value == int(id)), None)
    return state_name

def switch_abbv_to_name(abbv):
    id = switch_abbv_to_id(abbv)
    name = switch_id_to_state_name(id)
    return name


