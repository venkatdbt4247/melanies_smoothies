# Import python packages
# import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
streamlit.title("Customize Your Smoothie")
streamlit.write(
    """Replace this example with your own code!
    **And if you're new to st,** check
    out our easy-to-follow guides at
    [docs.st.io](https://docs.st.io).
    """
)

name_on_order = streamlit.text_input ("Name on Smoothie:")
cnx = streamlit.connection("snowflake")

session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
# st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = streamlit.multiselect (
    'Choose upto 5 ingredients:'
    , my_dataframe
    , max_selections=5
)

if ingredients_list:
    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        
        
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """' , '""" + name_on_order + """')"""
    
    time_to_insert = streamlit.button("Submit Order")
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        streamlit.success("Your Smoothie is ordered!")
# st.write(my_insert_stmt)
# st.write(ingredients_string)
