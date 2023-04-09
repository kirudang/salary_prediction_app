import streamlit as st
import pandas as pd
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import seaborn as sns



# COUNTRY
top_country_names = ['United States of America',
                    'Germany',
                    'United Kingdom of Great Britain and Northern Ireland',
                    'India',
                    'Brazil',
                    'Canada',
                    'France',
                    'Poland',
                    'Spain',
                    'Netherlands',
                    'Italy',
                    'Australia',
                    'Sweden',
                    'Russian Federation',
                    'Turkey']

def clean_country(x):
    if x in top_country_names:
        return x
    else:
        return "Others"


def clean_experience(x):
    if x ==  'More than 50 years':
        return 50
    if x == 'Less than 1 year':
        return 0.5
    return float(x)


def clean_education(x):
    if 'Bachelor’s degree' in x:
        return 'Bachelor’s degree'
    if 'Master’s degree' in x:
        return 'Master’s degree'
    if 'Professional degree' in x or 'Other doctoral' in x:
        return 'Post grad'
    return 'Less than a Bachelors'


def clean_coding_experience(x):
    if x ==  'More than 50 years':
        return 51
    if x == 'Less than 1 year':
        return 0.5
    return float(x)


def clean_employment(x):
    if x in ["Employed, full-time",
            "Employed, full-time;Independent contractor, freelancer, or self-employed",
             "Employed, full-time;Employed, part-time",
             "Employed, full-time;Independent contractor, freelancer, or self-employed;Employed, part-time",
             "Employed, full-time;Independent contractor, freelancer, or self-employed;Retired",
             "Employed, full-time;Retired"
            ]:
        return "Full-time Employment"
    elif  x in ["Employed, part-time",
                "Employed, part-time;Retired"
                ]:
        return "Part-time Employment"
    elif  x in ["Independent contractor, freelancer, or self-employed",
                "Independent contractor, freelancer, or self-employed;Employed, part-time"
                ]:
        return "Independent Contractor"
    else:
        return "I prefer not to say / Others"
    
def clean_gender(x):
    if x ==  'Man':
        return "Man"
    elif x ==  'Woman':
        return "Woman"
    else:
        return "Others"

@st.cache_data 
def load_data():
    # Load data
    df = pd.read_csv("./data/survey_results_public.csv")
    # Keep variables
    df = df[["Country", "EdLevel", "YearsCodePro", "Employment", "ConvertedCompYearly","WorkExp","Gender","Age"]]
    # Rename variables
    df = df.rename({"ConvertedCompYearly": "Salary",
               "EdLevel": "Education",
               "YearsCodePro": "Year_of_Code",
               "WorkExp": "Year_of_Experience"}, 
               axis=1
              )
    # Remove empty observations
    df = df.dropna()
    # Remove outlier
    q25_salary = df['Salary'].quantile(0.025)
    q975_salary = df['Salary'].quantile(0.975)
    # Filter data, only keep Salary from 1% to 98% quantile
    df = df[(df["Salary"]>= q25_salary) & (df["Salary"]<= q975_salary)]

    # Apply functions to data
    df['Country'] = df['Country'].apply(clean_country)
    df['Education'] = df['Education'].apply(clean_education)
    df['Year_of_Code'] = df['Year_of_Code'].apply(clean_coding_experience)
    df['Employment'] = df['Employment'].apply(clean_employment)
    df['Gender'] = df['Gender'].apply(clean_gender)

    return df

df = load_data()

def show_EDA_page():
    st.title("**:blue[Explanatory Analysis - Software Engineer Salaries]**")

    st.write(
        """
    ### Based on Stack Overflow Developer Survey 2022
    """
    )

        
    st.write(
        """
    #### **:green[1. Average Salary by Country:]**
    """
    )
    # Data
    country_mean_salary = df.groupby('Country')['Salary'].mean().sort_values(ascending=False)
    #st.bar_chart(country_mean_salary, x("Country"), y("Average Salary"))

    # Create a bar chart using Matplotlib
    fig, ax = plt.subplots()
    plt.bar(country_mean_salary.index, country_mean_salary.values)
    plt.xticks(rotation=90)
    plt.xlabel('Country')
    plt.ylabel('Average Salary')

    # Show the chart in the Streamlit app
    st.pyplot(fig)


    st.write(
        """
    #### **:green[2. Salary by Education Level:]**
    """
    )
    # Create a boxplot using Matplotlib
    fig, ax = plt.subplots()
    sns.boxplot(x='Education', y='Salary', data=df)
    plt.xticks(rotation=90)
    # add axis labels and a title to the plot
    plt.xlabel('Education Level')
    plt.ylabel('Salary')
    
    # Show the chart in the Streamlit app
    st.pyplot(fig)

    
    st.write(
        """
    #### **:green[3. Histogram of Coding Experience:]**
    """
    )
    fig, ax = plt.subplots()
    # create the histogram of salary using Seaborn
    sns.histplot(data=df, x='Year_of_Code', kde=True)
    # add axis labels and a title to the histogram plot
    plt.xlabel('Coding Experience')
    plt.ylabel('Frequency')
    
    # Show the chart in the Streamlit app
    st.pyplot(fig)

    st.write(
        """
    #### **:green[4. Year of Code vs Year of Experience Scatter Plot:]**
    """
    )
    fig, ax = plt.subplots()
    # create plot
    plt.scatter(df["Year_of_Code"], df["Year_of_Experience"])
    # add axis labels and a title to the histogram plot
    plt.xlabel("Year of Code")
    plt.ylabel("Year of Experience")
    
    # Show the chart in the Streamlit app
    st.pyplot(fig)

    corr = df["Year_of_Experience"].corr(df["Year_of_Code"])
    print("Correlation between Year_of_Experience and Year_of_Code:" + " {:,.02f}".format(corr))

    st.write(
        """
    #### **:green[5. Distribution of Salary by Gender:]**
    """
    )
    fig, ax = plt.subplots()
    # create plot
    sns.boxplot(x='Gender', y='Salary', data=df)
    # add axis labels and a title to the histogram plot
    plt.xlabel('Gender')
    plt.ylabel('Salary')
    
    # Show the chart in the Streamlit app
    st.pyplot(fig)


    st.write(
        """
    #### **:green[6. Share of Gender:]**
    """
    )
    # Plot share of Gender in data
    gender_counts = df['Gender'].value_counts()
    labels = gender_counts.index.tolist()
    sizes = gender_counts.values.tolist()
    # Plot
    fig, ax = plt.subplots()
    # create plot
    plt.pie(sizes, labels=labels, autopct='%1.1f%%')
    plt.axis('equal')
    plt.title("Share of Gender")
    
    # Show the chart in the Streamlit app
    st.pyplot(fig)
   

    st.write(
        """
    #### **:green[7. Average Salary by Age group:]**
    """
    )
    # Data
    age_mean_salary = df.groupby('Age')['Salary'].mean().sort_values(ascending=False)

    # Create a bar chart using Matplotlib
    fig, ax = plt.subplots()
    plt.bar(age_mean_salary.index, age_mean_salary.values)
    plt.xticks(rotation=90)
    plt.xlabel('Age Group')
    plt.ylabel('Average Salary')

    # Show the chart in the Streamlit app
    st.pyplot(fig)