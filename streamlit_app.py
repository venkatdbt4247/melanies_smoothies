# Import python packages
import streamlit as st 
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
import requests



# Write directly to the app
st.title("Customize Your Smoothie")
st.write(
    """Replace this example with your own code!
    **And if you're new to st,** check
    out our easy-to-follow guides at
    [docs.st.io](https://docs.st.io).
    """
)

name_on_order = st.text_input ("Name on Smoothie:")
cnx = st.connection( "snowflake")

session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
# st.dataframe(data=my_dataframe, use_container_width=True)
# st.stop

pd_df=my_dataframe.to_pandas()
st.dataframe(pd_df)
st.stop()

ingredients_list = st.multiselect (
    'Choose upto 5 ingredients:'
    , my_dataframe
    , max_selections=5
)

if ingredients_list:
    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        # st.write('The search value for ', fruit_chosen,' is ', search_on, '.')

        st.subheader(fruit_chosen + 'Nutrion Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + fruit_chosen)
        st_df = st.dataframe(data=smoothiefroot_response.json(), user_container_width=True)
        
        
        
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """' , '""" + name_on_order + """')"""
    
    time_to_insert = st.button("Submit Order")
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success("Your Smoothie is ordered!")
st.write(my_insert_stmt)
st.write(ingredients_string)
