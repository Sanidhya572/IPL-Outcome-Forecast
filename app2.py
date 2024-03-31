import streamlit as st
import pandas as pd
import pickle

# Load the trained model
pipe = pickle.load(open('pipe.pkl', 'rb'))
# st.image('bg1.jpg', caption='Sunrise by the mountains')

# Select batting and bowling teams
teams = sorted(['Sunrisers Hyderabad', 'Mumbai Indians', 'Royal Challengers Bangalore', 'Kolkata Knight Riders',
                'Kings XI Punjab', 'Chennai Super Kings', 'Rajasthan Royals', 'Delhi Capitals'])

batting_team = st.selectbox('Select the batting team', teams)
bowling_team = st.selectbox('Select the bowling team', teams)

# Select city and input target
cities = ['Hyderabad', 'Bangalore', 'Mumbai', 'Indore', 'Kolkata', 'Delhi', 'Chandigarh', 'Jaipur', 'Chennai',
          'Cape Town', 'Port Elizabeth', 'Durban', 'Centurion', 'East London', 'Johannesburg', 'Kimberley',
          'Bloemfontein', 'Ahmedabad', 'Cuttack', 'Nagpur', 'Dharamsala', 'Visakhapatnam', 'Pune', 'Raipur',
          'Ranchi', 'Abu Dhabi', 'Sharjah', 'Mohali', 'Bengaluru']

selected_city = st.selectbox('Select the city', sorted(cities))
target = st.number_input('Enter the target runs', min_value=0)

# Input score, wickets, and overs completed
score = st.number_input('Enter the current score', min_value=0)
wickets = st.number_input('Enter the number of wickets lost', min_value=0, max_value=9)
overs = st.number_input('Enter the number of overs completed', min_value=0, max_value=20)

# Predict probability button
if st.button('Predict Probability'):
    runs_left = target - score
    balls_left = 120 - overs * 6
    wickets_left = 10 - wickets
    crr = score / overs
    rrr = runs_left * 6 / balls_left
    df = pd.DataFrame({'batting_team': [batting_team], 'bowling_team': [bowling_team], 'city': [selected_city],
                       'runs_left': [runs_left], 'balls_left': [balls_left], 'wickets_left': [wickets_left],
                       'target_runs': [target], 'crr': [crr], 'rrr': [rrr]})
    result = pipe.predict_proba(df)
    batting_prob = round(result[0][0] * 100)
    bowling_prob = round(result[0][1] * 100)

    # Display winning probability
    st.markdown(f"#### Winning Probability")
    st.markdown(f"{batting_team}: **{batting_prob}%**")
    st.markdown(f"{bowling_team}: **{bowling_prob}%**")
    # st.markdown(bg1_img, unsafe_allow_html=True)

