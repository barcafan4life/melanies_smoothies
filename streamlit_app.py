# Import python packages
import streamlit as st
import requests
import pandas as pd
from snowflake.snowpark.functions import col





# Write directly to the app
st.title(f"Customize Your Smoothie :cup_with_straw: {st.__version__}")
st.write(
  "Choose the fruits you want!"
)

name_on_orders = st.text_input('Name of Smoothie:')
st.write ('Name of your smoothie will be:', name_on_orders)

cnx = st.connection("snowflake")
session = cnx.session()  
my_dataframe = session.table("smoothies.public.fruit_options").select(col('fruit_name'),col('search_on'))
#st.dataframe(data=my_dataframe, use_container_width=True)
#st.stop()

#Convert to Pandas

pd_df = my_dataframe.to_pandas()
#st.dataframe(pd_df)
#st.stop()

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:', 
    my_dataframe,
    max_selections=5
    )


if ingredients_list:

    ingredients_string = ''
    order_filled = False
    
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        #st.write('The search value for ', fruit_chosen,' is ', search_on, '.')
        
        st.subheader(fruit_chosen + 'Nutrition Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + search_on)
        sf_df = st.dataframe(data=smoothiefroot_response.json(),use_container_width=True)
        
    
        #st.write(ingredients_string)
    
        my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """','""" + name_on_orders + """')"""

    #st.write(my_insert_stmt)

    #st.write(ingredients_list)

    time_to_insert = st.button('Sumbit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered, ' + name_on_orders + '!', icon="✅")


