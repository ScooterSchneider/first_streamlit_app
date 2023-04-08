
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
        back_from_function = get_fruityvice_data(fruit_choice)
        streamlit.dataframe(back_from_function)
except URLError as e:
    streamlit.error();
    
streamlit. header ("The fruit load list contains:") #Snowflake-related functions
def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
        my_cur.execute("select * from fruit_load_list")
        return my_cur.fetchall()

# Add a button to load the fruit
if streamlit.button ('Get Fruit Load List'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_data_rows = get_fruit_load_list()
    streamlit.dataframe (my_data_rows)

# ADD FRUIT
# Allow the end user to add a fruit to the list
def insert_row_snowflake(new_fruit):
    with my_cnx.cursor() as my_cur:
        my_cur.execute(f"insert into fruit_load_list values('{new_fruit}')")
        return "Thanks for adding " + new_fruit
    
# add_my_fruit = streamlit.text_input('What fruit would you like to add?')
# if streamlit.button('Add a Fruit to the List'):
#     my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake")
#     back_from_function = insert_row_snowflake(add_my_fruit)
#     streamlit.text(back_from_function)
