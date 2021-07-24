#!/usr/bin/env python
# coding: utf-8

# ### Note
# * Instructions have been included for each segment. You do not have to follow them exactly, but they are included to help you think through the steps.

# In[8]:


# Dependencies and Setup
import pandas as pd

# File to Load (Remember to Change These)
file_to_load = "reference/purchase_data.csv"

# Read Purchasing File and store into Pandas data frame
purchase_data_df = pd.read_csv(file_to_load)


# ## Player Count

# * Display the total number of players
# 

# In[9]:


#list of all columns within the DataFrame
purchase_data_df.columns


# In[10]:


#display first 5 rows of data for reference
purchase_data_df.head()


# In[11]:


#total number of players
unique_purchase_id = purchase_data_df["SN"].value_counts()
total_players = unique_purchase_id.count()
pd.DataFrame({"Total Players": [total_players]})


# ## Purchasing Analysis (Total)

# * Run basic calculations to obtain number of unique items, average price, etc.
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display the summary data frame
# 

# In[12]:


#Total Number of Unique Items
unique_items = purchase_data_df["Item ID"].value_counts()
total_unqiue_items = unique_items.count()
total_unqiue_items


# In[13]:


#Average Price of All Items
average_item_price = round((purchase_data_df["Price"].mean()),2)
average_item_price


# In[14]:


#Number of Purchases
total_purchases = purchase_data_df["Purchase ID"].count()
total_purchases


# In[15]:


#Total Revenue 
total_revenue = purchase_data_df["Price"].sum()
total_revenue


# In[16]:


#Data Frame display of Number of Unique Items, Average Price,Number of Purchases, and Total Revenue

summary_table = pd.DataFrame({
                                "Number of Unique Items": [total_unqiue_items],
                                "Average Price": [average_item_price], 
                                "Number of Purchases": [total_purchases], 
                                "Total Revenue": [total_revenue]
                            })
#Formatting of the data
summary_table["Average Price"] = summary_table["Average Price"].map("${:,.2f}".format)
summary_table["Number of Purchases"] = summary_table["Number of Purchases"].map("{:,}".format)
summary_table["Total Revenue"] = summary_table["Total Revenue"].map("${:,.2f}".format)
summary_table


# ## Gender Demographics

# * Percentage and Count of Male Players
# 
# 
# * Percentage and Count of Female Players
# 
# 
# * Percentage and Count of Other / Non-Disclosed
# 
# 
# 

# In[17]:


#Player demographics with duplicate purchases dropped
player_demographics = purchase_data_df.loc[:, ["Gender", "SN", "Age"]]
player_demographics = player_demographics.drop_duplicates()
player_demographics


# In[18]:


#Gender count and % of the players

gender_demographics_total = player_demographics["Gender"].value_counts()
gender_demographics_percent = gender_demographics_total / total_players
gender_demographics = pd.DataFrame({"Total Count": gender_demographics_total,
                                    "Percentage of Players": gender_demographics_percent
                                   })
#Formatting of the data
gender_demographics["Percentage of Players"] = gender_demographics["Percentage of Players"].map("{:,.2%}".format)
                                                                                    
gender_demographics                                                                                    


# In[ ]:





# 
# ## Purchasing Analysis (Gender)

# * Run basic calculations to obtain purchase count, avg. purchase price, avg. purchase total per person etc. by gender
# 
# 
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display the summary data frame

# In[19]:


#Calculations for each gender
gender_purchase_total = purchase_data_df.groupby(["Gender"]).sum() ["Price"].rename("Total Purchase Value")
gender_average = purchase_data_df.groupby(["Gender"]).mean() ["Price"].rename("Average Purchase Price")
gender_counts = purchase_data_df.groupby(["Gender"]).count() ["Price"].rename("Purchase Count")

#Calc Normalized Purchasing Total
normalized_total = gender_purchase_total / gender_demographics ["Total Count"]

#DataFrame conversion
gender_data = pd.DataFrame({"Purchase Count": gender_counts,
                          "Average Purchase Price": gender_average,
                          "Total Purchase Value": gender_purchase_total,
                          "Normalized Totals": normalized_total
                        })

#cleaning the data
gender_data["Average Purchase Price"] = gender_data["Average Purchase Price"].map("${:,.2f}".format)
gender_data["Total Purchase Value"] = gender_data["Total Purchase Value"].map("${:,.2f}".format)
gender_data["Purchase Count"] = gender_data["Purchase Count"].map("{:,}".format)
gender_data["Avg Total Purchase per Person"] = gender_data["Normalized Totals"].map("${:,.2f}".format)
gender_data[["Purchase Count", "Average Purchase Price", "Total Purchase Value", "Avg Total Purchase per Person"]]


# ## Age Demographics

# * Establish bins for ages
# 
# 
# * Categorize the existing players using the age bins. Hint: use pd.cut()
# 
# 
# * Calculate the numbers and percentages by age group
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Optional: round the percentage column to two decimal points
# 
# 
# * Display Age Demographics Table
# 

# In[ ]:





# In[20]:


#Establish bins for ages
age_bins = [0, 9.90, 14.90, 19.90, 24.90, 29.90, 34.90, 39.90, 999999]
group_names = ["<10", "10-14", "15-19", "20-24", "25-29", "30-34", "35-39", "40+"]

#Categoroze the players using the age bins
player_demographics["Age Ranges"] = pd.cut(player_demographics["Age"], age_bins, labels=group_names)

age_demographics_totals = player_demographics["Age Ranges"].value_counts()
age_demographics_percents = age_demographics_totals / total_players
age_demographics = pd.DataFrame ({
                                "Total Count": age_demographics_totals,
                                "Percentage of Players": age_demographics_percents
})

#Clean and sort
age_demographics["Percentage of Players"] = age_demographics["Percentage of Players"].map("{:,.2%}".format)
age_demographics = age_demographics.sort_index()

#Display Data
age_demographics


# #Purchasing Analysis (Age)

# * Bin the purchase_data data frame by age
# 
# 
# * Run basic calculations to obtain purchase count, avg. purchase price, avg. purchase total per person etc. in the table below
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display the summary data frame

# In[21]:


#bins for purchase data
purchase_data_df["Age Ranges"] = pd.cut(purchase_data_df["Age"], age_bins, labels=group_names)

#calculations for Purchase Count, Average Purchase Price, Total Purchase Value, and Avg Total Purchase per Person
age_purchase_total = purchase_data_df.groupby(["Age Ranges"]).sum()["Price"].rename("Total Purchase Value")
age_average = purchase_data_df.groupby(["Age Ranges"]).mean()["Price"].rename("Average Purchase Price")
age_count = purchase_data_df.groupby(["Age Ranges"]).count()["Price"].rename("Purchase Count")

#Calc Normalized Total
normalized_age_purchase_total = age_purchase_total / age_demographics ["Total Count"]

#Convert to DataFrame
age_data = pd.DataFrame({
                        "Purchase Count": age_count,
                        "Average Purchase Price": age_average,
                        "Total Purchase Value": age_purchase_total,
                        "Avg Total Purchase per Person": normalized_age_purchase_total
                        })
#Clean
age_data["Average Purchase Price"] = age_data["Average Purchase Price"].map("${:,.2f}".format)
age_data["Total Purchase Value"] = age_data["Total Purchase Value"].map("${:,.2f}".format)
age_data["Purchase Count"] = age_data["Purchase Count"].map("${:,}".format)
age_data["Avg Total Purchase per Person"] = age_data["Avg Total Purchase per Person"].map("${:,.2f}".format)

#Display
age_data[["Purchase Count", "Average Purchase Price", "Total Purchase Value", "Avg Total Purchase per Person"]]


# ## Top Spenders

# * Run basic calculations to obtain the results in the table below
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Sort the total purchase value column in descending order
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display a preview of the summary data frame
# 
# 

# In[22]:


#calculations Purchase Count, Average Purchase Price, and Total Purchase Value

user_total = purchase_data_df.groupby(["SN"]).sum()["Price"].rename("Total Purchase Value")
user_average = purchase_data_df.groupby(["SN"]).mean()["Price"].rename("Average Purchase Price")
user_count = purchase_data_df.groupby(["SN"]).count()["Price"].rename("Purchase Count")

#Convert to DataFrame
user_data = pd.DataFrame({
                        "Total Purchase Value": user_total,
                        "Average Purchase Price": user_average,
                        "Purchase Count": user_count
                        })
#Clean and sorted
user_sorted = user_data.sort_values("Total Purchase Value", ascending=False)

user_sorted["Average Purchase Price"] = user_sorted["Average Purchase Price"].map("${:,.2f}".format)
user_sorted["Total Purchase Value"] = user_sorted["Total Purchase Value"].map("${:,.2f}".format)

#Display
user_sorted[["Purchase Count", "Average Purchase Price", "Total Purchase Value"]].head()



# ## Most Popular Items

# * Retrieve the Item ID, Item Name, and Item Price columns
# 
# 
# * Group by Item ID and Item Name. Perform calculations to obtain purchase count, average item price, and total purchase value
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Sort the purchase count column in descending order
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display a preview of the summary data frame
# 
# 

# In[23]:


#Retrieve the Item ID, Item Name, and Item Price columns
item_data = purchase_data_df[["Item ID", "Item Name", "Price"]]

#Calculations purchase count, average item price, and total purchase value
total_item_purchase = item_data.groupby(["Item ID", "Item Name"]).sum()["Price"].rename("Total Purchase Price")
average_item_purchase = item_data.groupby(["Item ID", "Item Name"]).mean()["Price"]
item_count = item_data.groupby(["Item ID", "Item Name"]).count()["Price"].rename("Purchase Count")

#Convert to DataFrame
item_data_pd = pd.DataFrame({
                            "Total Purchase Value": total_item_purchase,
                            "Item Price": average_item_purchase,
                            "Purchase Count": item_count
                            })

#Sort
item_data_count_sorted = item_data_pd.sort_values("Purchase Count", ascending=False)

#Clean and Display Data
item_data_count_sorted["Item Price"] = item_data_count_sorted["Item Price"].map("${:,.2f}".format)
item_data_count_sorted["Purchase Count"] = item_data_count_sorted["Purchase Count"].map("{:,}".format)
item_data_count_sorted["Total Purchase Value"] = item_data_count_sorted["Total Purchase Value"].map("${:,.2f}".format)

item_data_count_sorted[["Purchase Count", "Item Price", "Total Purchase Value"]].head()


# ## Most Profitable Items

# * Sort the above table by total purchase value in descending order
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display a preview of the data frame
# 
# 

# In[24]:


#Item table

#Sort
item_total_purchase = item_data_pd.sort_values("Total Purchase Value", ascending=False)

#Clean
item_total_purchase["Item Price"] = item_total_purchase["Item Price"].map("${:,.2f}".format)
item_total_purchase["Purchase Count"] = item_total_purchase["Purchase Count"].map("{:,}".format)
item_total_purchase["Total Purchase Value"] = item_total_purchase["Total Purchase Value"].map("${:,.2f}".format)

#Display
item_total_purchase[["Purchase Count", "Item Price", "Total Purchase Value"]].head()


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




