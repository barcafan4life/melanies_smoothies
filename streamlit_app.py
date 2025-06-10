# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(f"Customize Your Smoothie :cup_with_straw: {st.__version__}")
st.write(
  "Choose the fruits you want!"
)

name_on_orders = st.text_input('Name of Smoothie:')
st.write ('Name of your smoothie will be:', name_on_orders)

session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('fruit_name'))
#st.dataframe(data=my_dataframe, use_container_width=True)

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
    
    #st.write(ingredients_string)
    
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """','""" + name_on_orders + """')"""

    #st.write(my_insert_stmt)

    #st.write(ingredients_list)

    time_to_insert = st.button('Sumbit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered, ' + name_on_orders + '!', icon="✅")

