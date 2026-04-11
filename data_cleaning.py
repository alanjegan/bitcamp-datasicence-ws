# import file and upload csv file
import pandas as pd
from google.colab import files
files.upload()

# shows us the number of rows followed by columns
df.shape

# gives us info on the data frame like data type, columns, ect.
df.info()

# count of null values
df.isna().sum()

# dropping nulls before changing data types
df = df.dropna()
# filtering out values that contain letters
df = df[df['annual_spend'].str.contains(r'^\d+\.\d+')]
# stripping any trailing whitespaces
df['signup_date'] = df['signup_date'].astype(str).str.strip()

# converting data types
df = df.astype({'full_name':'string',
                'email':'string',
                'phone': 'string',
                'age':'int',
                'annual_spend':'float',
                'country':'string',
                'status':'string'})

# datetime formats for converting date column
formats = ['%Y-%m-%d', '%d/%m/%Y', '%m/%d/%Y', '%B %d, %Y', '%b %d %Y', '%Y/%m/%d', '%d-%m-%Y']

def try_formats(val):
    for fmt in formats:       # try each format one by one
        try:
            return pd.to_datetime(val, format=fmt)  # if it works, return immediately
        except:
            continue          # if it fails, move on to the next format
    return pd.NaT
df['signup_date'] = df['signup_date'].apply(try_formats)

df.isna().sum()

df = df.dropna()
# changing all dates into a singular format
df['signup_date'] = df['signup_date'].dt.strftime('%Y-%m-%d')

# changing to lowercase
df['status'] = df['status'].str.strip().str.lower()
# anything that starts with in, is inactive
df['status'] = df['status'].mask(df['status'].str.startswith('in'), 'inactive')
# replacing any incorrect spelling
df['status'] = df['status'].replace({
    'activ': 'active',
    'actve': 'active',
    'pendng': 'pending'
})

# gives all the unique values
df['country'].unique()

# standardizing all the country names
country_map = {
    # USA
    'USA': 'USA', 'US': 'USA', 'U.S.A': 'USA', 'u.s.': 'USA',
    'United States': 'USA', 'united states': 'USA', 'UNITED STATES': 'USA',
    'USA ': 'USA', 'Us': 'USA',

    # Canada
    'Canada': 'Canada', 'canada': 'Canada', 'CANADA': 'Canada',
    'CA': 'Canada', 'Can.': 'Canada',

    # UK
    'UK': 'UK', 'U.K.': 'UK', 'GB': 'UK', 'England': 'UK',
    'United Kingdom': 'UK', 'united kingdom': 'UK',

    # Australia
    'Australia': 'Australia', 'australia': 'Australia', 'AUSTRALIA': 'Australia',
    'AUS': 'Australia', 'Aus': 'Australia',

    # Germany
    'Germany': 'Germany', 'germany': 'Germany', 'GERMANY': 'Germany',
    'DE': 'Germany', 'Deutschland': 'Germany',

    # France
    'France': 'France', 'france': 'France', 'FRANCE': 'France', 'FR': 'France',

    # India
    'India': 'India', 'india': 'India', 'INDIA': 'India', 'IN': 'India',

    # Brazil
    'Brazil': 'Brazil', 'brasil': 'Brazil', 'BRAZIL': 'Brazil', 'BR': 'Brazil',

    # Mexico
    'Mexico': 'Mexico', 'mexico': 'Mexico', 'MEXICO': 'Mexico', 'MX': 'Mexico',

    # Japan
    'Japan': 'Japan', 'japan': 'Japan', 'JAPAN': 'Japan', 'JP': 'Japan',
}
# striping whitespace and replacing incorrect country names
df['country'] = df['country'].str.strip().replace(country_map)

# completely stripping the phone column before reformatting
df['phone'] = df['phone'].str.replace(r'\D', '', regex=True)
# standardizing phonenumbers that initially had +1
def standardizing_phone(phone):
    if len(phone) == 11 and phone[0] == '1':
        return phone[1:]
    else:
        return phone
# applying the function
df['phone'] = df['phone'].apply(standardizing_phone)

# function to reformat
def insert_dashes(phone):
    if len(phone) == 10:
        return f"{phone[:3]}-{phone[3:6]}-{phone[6:]}"
    else:
        return phone
# applying the function
df['phone'] = df['phone'].apply(insert_dashes)


df.head()

# Remove any incorrect ages
df = df[df['age'] <= 100]

# filtering out emails that are not in the proper format using regex
df = df[df['email'].str.contains(r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$')]
# making emails lowercase
df['email'] = df['email'].str.lower()


# making names lowercase
df['full_name'] = df['full_name'].str.lower()
# making the first letter of first and last name uppercase
df['full_name'] = df['full_name'].str.title()

# dropping the customer_id
df = df.drop(columns='customer_id')
# gets rid of the old index
df = df.reset_index(drop=True)
# shifts the new index by one
df.index = df.index + 1
# makes the new index a column and renames
df = df.reset_index(names='customer_id')


# final overview of cleaned data
df.head()
