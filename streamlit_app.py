
import streamlit;
import pandas;
import requests;
import snowflake.connector;
from urllib.error import URLError;

# HEADER AREA
streamlit.title('My Parent new Healthy Diner');
streamlit.header('Breakfast Menu');
streamlit.text('🥣 Healthy Oatmeal');
streamlit.text('🥗 Chewey Kale - So Gross');
streamlit.text('🐔 Hard Boiled Chicken Poop, Eggs');
streamlit.text('🥑🍞 Avacado Toast');

#  BUILD YOUR OWN
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')


# Import some fruit
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt");
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])

# Filter on selected
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
streamlit.dataframe(fruits_to_show);

#New Section to display fruityvice api response
streamlit.header("Fruityvice Fruit Advice!")

# fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
# streamlit.write('The user entered ', fruit_choice)

# fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
# # take the json version of the response and normalize it
# fruityvice_normalized = pandas.json_normalize(fruityvice_response.json ()) #output it the screen as a table
# streamlit.dataframe (fruityvice_normalized)

#New Section to display fruityvice api response
def get_fruityvice_data(this_fruit_choice):
    fruityvice_response = requests.get ("https://fruityvice.com/api/fruit/" + this_fruit_choice)
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    return fruityvice_normalized;

streamlit.header('Fruityvice Fruit Advice!')
try:
    fruit_choice = streamlit.text_input ('What fruit would you like information about?')
    if not fruit_choice:
        streamlit.error("please select a fruit to get information.")
    else:
        back_from_function = get_fruityvice data(fruit_choice)
        streamlit.dataframe(back_from_function)
except URLError as e:
    streamlit.error();

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor ()
my_cur.execute("select * from fruit_load_list")
# my_data_row = my_cur.fetchone()
my_data_rows = my_cur.fetchall()
streamlit.header("The fruit load list contains:")
streamlit.dataframe(my_data_rows)

add_my_fruit = streamlit.text_input('What would you like to add?')
streamlit.write('Thanks for adding ', add_my_fruit)

#This will not work correctly, but just go with it for now
my_cur.execute(f"insert into fruit_load_list values('{add_my_fruit}')")
