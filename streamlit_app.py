
import streamlit;
import pandas;
import requests

fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
streamlit.text(fruityvice_response)

streamlit.title('My Parent new Healthy Diner');
streamlit.header('Breakfast Menu');
streamlit.text('🥣 Healthy Oatmeal');
streamlit.text('🥗 Chewey Kale - So Gross');
streamlit.text('🐔 Hard Boiled Chicken Poop, Eggs');
streamlit.text('🥑🍞 Avacado Toast');

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

# Import some fruit
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt");
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
# streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index))
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])

# Filter on selected
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
# streamlit.dataframe(my_fruit_list);
streamlit.dataframe(fruits_to_show);
