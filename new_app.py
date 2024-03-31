# import streamlit as st
# import pandas as pd
# import pickle

# # Load the model
# pipe = pickle.load(open('pipe.pkl','rb'))

# # Load the dataset
# @st.cache
# def load_data():
#     return pd.read_csv("deliveries.csv")  # Replace "your_dataset.csv" with the actual file path

# df = load_data()

# # Function to display team information
# def display_team_info(team_name):
#     st.subheader(f"Players in {team_name}:")
#     team_players = df[df['batting_team'] == team_name]['batsman'].unique()
#     st.write(team_players)

# # Streamlit layout
# st.title('IPL Win Predictor')

# # Sidebar navigation
# menu_selection = st.sidebar.selectbox("Menu", ["Home", "Team Information"])

# if menu_selection == "Home":
#     st.image('bg1.jpg')

#     teams = sorted(df['batting_team'].unique())
#     col1, col2 = st.columns(2)

#     with col1:
#         batting_team = st.selectbox('Select the batting team', teams)

#     available_teams = [team for team in teams if team != batting_team]
#     with col2:
#         bowling_team = st.selectbox('Select the bowling team', available_teams)

#     cities = sorted(df['city'].unique())
#     selected_city = st.selectbox('Cities', cities)

#     target = st.number_input('Target', min_value=0)

#     col3, col4, col5 = st.columns(3)
#     with col3:
#         score = st.number_input('Score', min_value=0)
#     with col4:
#         wickets = st.number_input('Wickets', min_value=0, max_value=9)
#     with col5:
#         overs = st.number_input('Overs completed', min_value=0, max_value=20)

#     if st.button('Predict Probability'):
#         runs_left = target - score
#         balls_left = 120 - overs * 6
#         wickets = 10 - wickets
#         crr = score / overs
#         rrr = runs_left * 6 / balls_left
#         df_input = pd.DataFrame({'batting_team': [batting_team], 'bowling_team': [bowling_team], 'city': [selected_city],
#                                  'runs_left': [runs_left], 'balls_left': [balls_left], 'wickets': [wickets],
#                                  'total_runs_x': [target], 'crr': [crr], 'rrr': [rrr]})
#         result = pipe.predict_proba(df_input)
#         r_1 = round(result[0][0] * 100)
#         r_2 = round(result[0][1] * 100)
#         st.header('Winning Probability')
#         st.header(f"{batting_team}  : {r_2} % {'👍' if r_2 > r_1 else '👎'}")
#         st.header(f"{bowling_team}  : {r_1} % {'👍' if r_1 > r_2 else '👎'}")

# elif menu_selection == "Team Information":
#     st.title("Team Information")
#     teams = sorted(df['batting_team'].unique())
#     selected_team = st.selectbox("Select Team", teams)
#     display_team_info(selected_team)
import streamlit as st
import pandas as pd
import pickle

# Load the model
pipe = pickle.load(open('pipe.pkl','rb'))

# Load the datasets
@st.cache_data
def load_data():
    matches_df = pd.read_csv("matches.csv")  # Replace "matches.csv" with the actual file path
    deliveries_df = pd.read_csv("deliveries.csv")  # Assuming this is your existing deliveries dataset
    return matches_df, deliveries_df

matches_df, deliveries_df = load_data()

# Function to display team information for a specific season
def display_team_info(team_name, season):
    # Filter matches dataframe for the selected team and season to get match_ids
    team_matches = matches_df[(matches_df['team1'] == team_name) | (matches_df['team2'] == team_name)]
    team_matches_season = team_matches[team_matches['Season'] == season]
    match_ids = team_matches_season['id'].unique()

    # Filter deliveries dataframe for the selected match_ids and team_name to get players
    team_players = deliveries_df[(deliveries_df['match_id'].isin(match_ids)) & (deliveries_df['batting_team'] == team_name)]['batsman'].unique()
    
    st.write(f"**Players in {team_name} for season {season}:**")
    st.table(pd.DataFrame({"Players": team_players}, index=range(1, len(team_players)+1)))

# Streamlit layout
st.title('IPL Win Predictor')

# Sidebar navigation
menu_selection = st.sidebar.selectbox("Menu", ["Home", "Team Information"])

if menu_selection == "Home":
    st.image('bg1.jpg')

    teams = sorted(['Sunrisers Hyderabad',
        'Mumbai Indians',
        'Royal Challengers Bangalore',
        'Kolkata Knight Riders',
        'Kings XI Punjab',
        'Chennai Super Kings',
        'Rajasthan Royals',
        'Delhi Capitals'])
    col1, col2 = st.columns(2)

    with col1:
        batting_team = st.selectbox('Select the batting team', teams)

    available_teams = [team for team in teams if team != batting_team]
    with col2:
        bowling_team = st.selectbox('Select the bowling team', available_teams)

    cities = ['Hyderabad', 'Bangalore', 'Mumbai', 'Indore', 'Kolkata', 'Delhi',
       'Chandigarh', 'Jaipur', 'Chennai', 'Cape Town', 'Port Elizabeth',
       'Durban', 'Centurion', 'East London', 'Johannesburg', 'Kimberley',
       'Bloemfontein', 'Ahmedabad', 'Cuttack', 'Nagpur', 'Dharamsala',
       'Visakhapatnam', 'Pune', 'Raipur', 'Ranchi', 'Abu Dhabi',
       'Sharjah', 'Mohali']

    selected_city = st.selectbox('Cities',sorted(cities))
    

    target = st.number_input('Target', min_value=0)

    col3, col4, col5 = st.columns(3)
    with col3:
        score = st.number_input('Score', min_value=0)
    with col4:
        wickets = st.number_input('Wickets', min_value=0, max_value=9)
    with col5:
        overs = st.number_input('Overs completed', min_value=0, max_value=20)

    if st.button('Predict Probability'):
        runs_left = target - score
        balls_left = 120 - overs * 6
        wickets = 10 - wickets
        crr = score / overs
        rrr = runs_left * 6 / balls_left
        df_input = pd.DataFrame({'batting_team': [batting_team], 'bowling_team': [bowling_team], 'city': [selected_city],
                                 'runs_left': [runs_left], 'balls_left': [balls_left], 'wickets': [wickets],
                                 'total_runs_x': [target], 'crr': [crr], 'rrr': [rrr]})
        result = pipe.predict_proba(df_input)
        r_1 = round(result[0][0] * 100)
        r_2 = round(result[0][1] * 100)
        st.header('Winning Probability')
        st.header(f"{batting_team}  : {r_2} % {'👍' if r_2 > r_1 else '👎'}")
        st.header(f"{bowling_team}  : {r_1} % {'👍' if r_1 > r_2 else '👎'}")

elif menu_selection == "Team Information":
    st.title("Team Information")
    st.image('all_ipl.jpg',width=800)
    # teams = sorted(deliveries_df['batting_team'].unique())
    teams = sorted(['Sunrisers Hyderabad',
       'Mumbai Indians',
       'Royal Challengers Bangalore',
       'Kolkata Knight Riders',
       'Kings XI Punjab',
       'Chennai Super Kings',
       'Rajasthan Royals',
       'Delhi Capitals'])
    selected_team = st.selectbox("Select Team", teams)
    seasons = sorted(matches_df['Season'].unique())
    selected_season = st.selectbox("Select Season", seasons)
    display_team_info(selected_team, selected_season)
