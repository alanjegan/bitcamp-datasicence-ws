# import file and upload csv file
import pandas as pd
import matplotlib as plt
from google.colab import files
files.upload()

# create a data frame from the csv file
df = pd.read_csv("messy_customers_large.csv")

# You can filter data frames for specific categories of data
# a data from of all people who are 30 and above in the USA
df[(df['age'] >= 30) & (df['country'] == 'USA')]

# more filtering
# filter for all names that start with s
df[df['full_name'].str.startswith('S')]

# you can also sort using pandas
df.sort_values(by='annual_spend')

# you can group by certain columns of data, so that you can find aggregate values
# mean spending per country
average_spending = df.groupby('country')['annual_spend'].mean().reset_index()
display(average_spending)

plt.bar(average_spending['country'], average_spending['annual_spend'])
plt.xlabel('Country')
plt.ylabel('Average Spending')
plt.xticks(fontsize=12, rotation=45)
plt.title('Average Spending per Country')
plt.show()

# If i wanted to see if there is a correlation between age and spending:
age_to_spend = df[['age', 'annual_spend']]
display(age_to_spend)
sample = age_to_spend.sample(100, random_state=42)

# Calculating correlation
sample['age'].corr(sample['annual_spend'])

# Visualizing the correlation between spending and age
plt.scatter(sample['age'], sample['annual_spend'])
plt.xlabel('Age')
plt.ylabel('Annual Spend')
plt.title('Age vs. Annual Spend')
plt.show()

# pivot tables to present avaerage spending per country per status
df.pivot_table(values='annual_spend', index='country', columns='status', aggfunc='mean')
