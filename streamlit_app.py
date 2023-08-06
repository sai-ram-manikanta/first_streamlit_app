import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('My Parents New Healthy Diner')
streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avacado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

# import pandas
my_fruits_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruits_list = my_fruits_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruits_list.index), ['Avocado', 'Strawberries'])
fruits_to_show = my_fruits_list.loc[fruits_selected]


# display table on the page
streamlit.dataframe(fruits_to_show)

# function creatiom
def get_fruityvice_data(this_fruit_choice):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    return fruityvice_normalized
  

# header
streamlit.header("Fruityvice Fruit Advice!")
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error('Please select a fruit to get information.')
  else:
    back_from_function = get_fruityvice_data(fruit_choice)
    # fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
    # fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    streamlit.dataframe(back_from_function)
except URLError as e:
  streamlit.error()
    
streamlit.write('The user entered ', fruit_choice)

# display fruityvice api response 
# import requests
# fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
#streamlit.text(fruityvice_response.json())

# normalize the JSON response
# fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())

#Output the data on the screen as table 
# streamlit.dataframe(fruityvice_normalized)

# don't run anything past here while we troubleshoot


# import snowflake.connector
streamlit.header("The fruit load list contains:")
# SF related functions
def get_fruits_load_list():
    with my_cnx.cursor() as my_cur:
        my_cur.execute("select * from fruit_load_list")
        return my_cur.fetchall()

# Add a button to load the fruit
if streamlit.button('Get Fruit Load List'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_data_rows = get_fruit_load_lsit()
    streamlit.dataframe(my_data_rows)

# my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
# my_cur = my_cnx.cursor()
# my_cur.execute("select * from fruit_load_list")
# my_data_rows = my_cur.fetchall()
# streamlit.header("The fruit load list contains:")
# streamlit.dataframe(my_data_rows)

streamlit.stop()

# Allow user to add fruit to the list
def insert_row_snowflake(new_fruit):
    with my_cnx.cursor() as my_cur:
        my_cur.execute("insert into fruit_load_list_values ('from streamlit')")
        return "Thanks for adding " + new_fruit
        
add_my_fruit = streamlit.text_input('What fruit would you like to add?')
if streamlit.button('Add a Fruit to the List'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    back_from_function = insert_row_snowflake(add_my_fruit)
    streamlit.text(back_from_function)
# fruit_choice2 = streamlit.text_input('What fruit would you like to add?','Jackfruit')
# streamlit.write('Thanks for adding ', fruit_choice2)

# test 1
# my_cur.execute("insert into fruit_load_list values('from streamlit')")


