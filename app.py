import streamlit as st
import joblib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from PIL import Image
matplotlib.use('agg')

@st.cache
def load_data(dataset):
    df = pd.read_csv(dataset)
    return df

bedroom ={'1': 1, '2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,}
bathrooms = {'1': 1, '2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,}
toilets = {'1': 1, '2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,}
estate = {'Yes':1, 'No':0}
duplex = {'Yes':1, 'No':0}
serviced = {'Yes':1, 'No':0}
new = {'Yes':1, 'No':0}

location = {"Ajah":'ajah', "Gbagada":'gbagada', "Ikeja":'ikeja', "Lekki":'lekki',"Ikorodu":'ikorodu', 
            "Iyana Ipaja": 'iyana ipaja' ,"Ogba":'ogba', "Surulere":'surulere',"Yaba":'yaba',
            }

data = load_data('data.csv')

rank_dict = dict(data.groupby('locationbed')['rank'].median())
estate_price_dict = dict(data.groupby('locationbed')['estate_price'].median())
new_price_dict = dict(data.groupby('locationbed')['new_price'].median())
terraced_price_dict = dict(data.groupby('locationbed')['terraced_price'].median())

#Get the keys
def get_value(val, my_dict):
    for key, value in my_dict.items():
        if val == key:
            return value

#Find the keys in the dictionary
def get_key(val, my_dict):
    for key, value in my_dict.items():
        if val == value:
            return key
        
#Find the keys in the dictionary        
def get_key_str(val, my_dict):
    for key, value in my_dict.items():
        if val in value:
            return key
        
def load_prediction_model(model_file):
    loaded_model = joblib.load(model_file)
    return loaded_model
    
modelz = load_prediction_model("rfg_base.pkl")    

img1 = Image.open("serviced.jpeg")
img2 = Image.open("terraced.png")
img3 = Image.open("estate.jpg")
img4 = Image.open("old.jpg")

#st.image(img,width=300,caption="SimpleImage")

def main():
    """Housing Ml App"""
    st.title("House Rent Solution")
    st.markdown("**_Developer: Adebayo Aonullahi_** :sunglasses:") 
    
    #menu
    menu = ["About", "Analysis", "Estimator"]
    choices = st.sidebar.selectbox("Select Activities",menu)


    if choices == 'Estimator':
        st.subheader("**House Rent Estimator**")
        Number_of_Bedrooms = st.sidebar.slider("Number of Bedrooms", 1,8)
        Number_of_Toilet = st.sidebar.slider("Number of Toilet", 1,8)
        Number_of_Bathrooms = st.sidebar.slider("Number of Bathrooms", 1,8)
        locations = st.sidebar.selectbox("Your preferred location",tuple(location.keys()) )
        estate_or_not = st.sidebar.selectbox("Do you want to live in an Estate ?",tuple(estate.keys()) )
        terrace_or_not = st.sidebar.selectbox("Do you want to live in a terracced apartment ?",tuple(duplex.keys()) )
        serviced_flag = st.sidebar.selectbox("Do you prefer a serviced apartment ?",tuple(serviced.keys()) )
        new_flag = st.sidebar.selectbox("Do you prefer a new apartment ?",tuple(new.keys()) )
        locationbed = locations.lower()+str(Number_of_Bedrooms)
       
        #encoding
        v_estate_or_not = get_value(estate_or_not,estate )
        v_serviced_flag = get_value(serviced_flag,serviced )      
        v_terrace_or_not = get_value(terrace_or_not,duplex )
        v_new_flag = get_value(new_flag, new)
        
        v_rank = get_value(locationbed , rank_dict)
        v_mid_est = get_value(locationbed , estate_price_dict )
        v_mid_new = get_value(locationbed , new_price_dict )
        v_mid_ter = get_value(locationbed , terraced_price_dict )
        
        v_amenities= Number_of_Bathrooms + Number_of_Toilet
        v_value = v_estate_or_not + v_terrace_or_not + v_new_flag + v_serviced_flag
        
        
        predictor_data= [v_amenities, Number_of_Bedrooms, Number_of_Bathrooms, Number_of_Toilet, 
                         v_new_flag, v_terrace_or_not, v_serviced_flag, v_estate_or_not, v_mid_est,
                          v_mid_ter, v_mid_new, v_value,  v_rank] 
                         
    
        pretty_data = {
        "No. of Bedrooms":Number_of_Bedrooms,
        "No. of Toilets":Number_of_Toilet,
        "No. of Bathrooms":Number_of_Bathrooms,
        "Preferred Location":locations,
        "Estate ?":estate_or_not ,
        "Terraced ?":terrace_or_not,
        "Serviced ?":serviced_flag,
        "New ?":new_flag,
        }
        
        st.write("*options selected...*")
        st.json(pretty_data)
        
       
        
        predictor_data= np.array(predictor_data).reshape(1,-1)
    


        if st.button("Evaluate"):
                
            predicted = modelz.predict(predictor_data)
            predicted =  int(predicted)            
            predicted = int(round(predicted, -3))
            predicted =  f"{predicted:,}"
            #st.write("The predicted price for this apartment in ", locations,"is ₦",str(predicted))
            st.success("The predicted price for your choice apartment in " + locations + " is ₦" + predicted)
            
            if (v_serviced_flag==1):
                st.image(img1, use_column_width=True)
            
            elif (v_terrace_or_not==1):
                st.image(img2,use_column_width=True)
            
            elif ((v_estate_or_not==1)|(v_new_flag==1)):
                st.image(img3,use_column_width=True)
            
            else:
                st.image(img4,use_column_width=True)
    

    if choices == 'Analysis':
        st.subheader("**House Rent Distribution**")
        Number_of_Bedrooms = st.sidebar.slider("Number of Bedrooms", 1,8)
        Number_of_Toilet = st.sidebar.slider("Number of Toilet", 1,8)
        Number_of_Bathrooms = st.sidebar.slider("Number of Bathrooms", 1,8)
        locations = st.sidebar.selectbox("Your preferred location",tuple(location.keys()) )
        locations = locations.lower()

        

       
        data['Price'][(data['Location']==locations)&(data['Bedroom']==Number_of_Bedrooms)
        											&(data['Bathroom']==Number_of_Bathrooms)
        											&(data['Toilet']==Number_of_Toilet)].plot(kind="hist")
        
     
        plt.xlabel('House Rent (₦)')  
        st.pyplot()
        


    if choices == 'About':
        st.subheader("**About**")
        st.markdown("**House Rent Solution Application** helps predict rent of houses in some areas in Lagos and also provide details of the rent distribution by location. This application was built with streamlit and the data used for modeling was scrapped from a Real Estate website operating in Nigeria. The predictions from this app is reliable with an error of **_+/- ₦150,000_**.")
   
        st.markdown('**_Inspired by Technidus NG..._**')


if __name__ == "__main__":
    main()