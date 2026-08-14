import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb

from  matplotlib.ticker import LogLocator
from matplotlib.ticker import FuncFormatter

st.set_page_config(
  page_title='Credit Risk Analysis',
  layout='wide'
  )

@st.cache_data
def load_data():
  df = pd.read_csv('cleaned_credit_risk_dataset.csv')
  df = df.rename(columns={
    'Clean_person_age':'Age',
    'Clean_person_income':'Income',
    'Clean_person_home_ownership':'Home Ownership',
    'Clean_person_emp_length':'Employment Length',
    'Clean_loan_intent':'Loan Intent',
    'Clean_loan_grade':'Loan Grade',
    'Clean_loan_amnt':'Loan Amount',
    'Clean_loan_int_rate':'Interest Rate',
    'Clean_loan_status':'Loan Status',
    'Clean_loan_percent_income':'DTI',
    'Clean_cb_person_default_on_file':'Default Status',
    'Clean_cb_person_cred_hist_length':'Credit History Length'
  })
  return df

df = load_data()

st.sidebar.title('Filters')
age_range = st.sidebar.slider(
  'Age Group',
  value=(df['Age'].min(), df['Age'].max()),
  min_value=df['Age'].min(),
  max_value=df['Age'].max()
)
grade_range = st.sidebar.multiselect(
  'Grades',
  df['Loan Grade'].sort_values(ascending=True).unique().tolist(),
  default = df['Loan Grade'].sort_values(ascending=True).unique().tolist()
)

fdf = df[
  (df['Age'] >= age_range[0]) &
  (df['Age'] <= age_range[1]) &
  (df['Loan Grade'].isin(grade_range))
].copy()

# Header and KPI
st.title('Credit Risk Analysis Dashboard')
if fdf.empty:
  st.warning('No data matches the specific filters.')
else:
  st.caption(f'Analyzing {len(fdf):,} records from ages {age_range[0]} to {age_range[1]}')

  avg_income = fdf['Income'].median()
  avg_loan_amount = fdf['Loan Amount'].median()
  avg_int_rate = fdf['Interest Rate'].median()
  avg_dti = fdf['DTI'].median()
  avg_percentage = fdf['Age'].count()/df['Age'].count()

  k1, k2, k3 = st.columns(3)

  k1.metric('Average Income', f'${avg_income:,.2f}')
  k2.metric('Average Loan Amount', f'${avg_loan_amount:,.2f}')
  k3.metric('Average Interest Rate', f'{avg_int_rate:,.2f}%')

  k4, k5 = st.columns(2)
  k4.metric('Average DTI', f'{avg_dti:,.2%}')
  k5.metric('Coverage in %', f'{avg_percentage:,.2%}')

  FIGSIZE=(6,4)
  FIGSIZE2=(10,8)
  # Income Chart
  fig1, ax1 = plt.subplots(figsize=FIGSIZE)
  sb.histplot(
    fdf['Income'],
    bins='fd',
    kde=True,
    stat='count',
    log_scale=True
    )
  ax1.xaxis.set_major_formatter(FuncFormatter(lambda x, _:f'{int(x):,}'))
  ax1.xaxis.set_major_locator(LogLocator(base=10, subs=[1, 0]))

  # Employment Length Chart
  fig2, ax2 = plt.subplots(figsize=FIGSIZE)
  sb.histplot(
    fdf['Employment Length'],
    bins='fd',
    kde=True,
    stat='count',
    )

  # Loan Amount Chart
  fig3, ax3 = plt.subplots(figsize=FIGSIZE)
  sb.histplot(
    fdf['Loan Amount'],
    bins='fd',
    kde=True,
    stat='count',
    )

  # Home Ownership Chart
  ownership_counts = fdf['Home Ownership'].value_counts()
  ownserhip_values = fdf['Home Ownership'].unique().tolist()

  fig4, ax4 = plt.subplots(figsize=FIGSIZE2)
  pie = ax4.pie(
    ownership_counts,
    autopct='%1.1f%%',
    pctdistance=0.75, 
    textprops=dict(color='black', size=14, weight='bold')
  )
  ax4.set_title('Distribution of Home Ownserships')
  ax4.legend(pie.wedges, ownserhip_values, title='Types of Home Ownerships')

  # Loan Intent Chart
  intent_counts = fdf['Loan Intent'].value_counts()
  intent_values = fdf['Loan Intent'].unique().tolist()
  fig5, ax5 = plt.subplots(figsize=FIGSIZE2)
  pie = ax5.pie(
    intent_counts,
    autopct='%1.1f%%',
    pctdistance=0.75, 
    textprops=dict(color='black', size=14, weight='bold')
  )
  ax5.set_title('Distribution Loan Intent/Purpose')
  ax5.legend(pie.wedges, intent_values, title='Type of Loan Intent/Purpose')

  # Default Status
  default_counts = fdf['Default Status'].value_counts()
  fig6, ax6 = plt.subplots(figsize=FIGSIZE2)
  pie = ax6.pie(
    default_counts,
    autopct='%1.1f%%',
    pctdistance=0.75, 
    textprops={'color': 'black', 'size': 14, 'weight': 'bold'}
  )
  ax6.set_title('Distribution of Default Status')
  ax6.legend(pie.wedges, ['Not Defaulted','Defaulted'], title='Default Status')

  # Loan Status
  loan_status_counts = fdf['Loan Status'].value_counts()
  fig7, ax7 = plt.subplots(figsize=FIGSIZE2)
  pie = ax7.pie(
    loan_status_counts,
    autopct='%1.1f%%',
    pctdistance=0.75, 
    textprops={'color': 'black', 'size': 14, 'weight': 'bold'}
  )
  ax7.set_title('Distribution of Loan Status')
  ax7.legend(pie.wedges, ['Inactive','Active'], title='Loan Status' )

  chart1, chart2, chart3 = st.columns(3)
  with chart1:
    st.subheader('Income')
    st.pyplot(fig1)
  with chart2:
    st.subheader('Employment Length')
    st.pyplot(fig2)
  with chart3:
    st.subheader('Loan Amount')
    st.pyplot(fig3)

  chart4, chart5 = st.columns(2)
  with chart4:
    st.subheader('Home Ownsership')
    st.pyplot(fig4)
  with chart5:
    st.subheader('Loan Intent')
    st.pyplot(fig5)


  chart6, chart7 = st.columns(2)
  with chart6:
    st.subheader('Default Status')
    st.pyplot(fig6)
  with chart7:
    st.subheader('Loan Status')
    st.pyplot(fig7)

# Average Borrower Profile

# Personal Info
age_info = df['Age'].median()
income_info = df['Income'].median()

home_ownership_counts = df['Home Ownership'].value_counts()
home_ownership_info = pd.DataFrame(home_ownership_counts.head(2))

emp_length_info = df['Employment Length'].median()

# Credit and loan info
loan_grades_count = df['Loan Grade'].value_counts()
loan_grades_info = pd.DataFrame(loan_grades_count.head(2))

loan_amount_info = df['Loan Amount'].median()

int_rate_info = df['Interest Rate'].median()

loan_status_count = df['Loan Status'].value_counts()
loan_status_info = pd.DataFrame(loan_status_count.head())

dti_info = df['DTI'].median()

default_status_count = df['Default Status'].value_counts()
default_status_info = pd.DataFrame(default_status_count.head())

credit_history_length = df['Credit History Length'].median()


st.title('Average Borrower Profile')
col1, col2 = st.columns(2)

with col1:

  st.subheader('Personal Information')
  col1.metric('The average borrower has an age of',f'{int(age_info)} yrs old')

  col1.metric('The average borrower has an annual income of',f'$ {income_info:,.2f}')

  col1.metric("The average borrower's home is under",
              f'{home_ownership_info.iloc[0].name} or {home_ownership_info.iloc[1].name}')

  col1.metric('The average borrower is employed for ',f'{int(emp_length_info)} years')

with col2:
  st.subheader('Loan and Credit Information')
  col2.metric(
    "The average borrower's purpose for loaning is/are", 
    'Varied and no dominant intent.')
  
  col2.metric(
    'Their loan grade is/are commonly ',
    f'{loan_grades_info.iloc[0].name} or {loan_grades_info.iloc[1].name}',)
  
  col2.metric('Their loan amount is around', f'$ {loan_amount_info:,.2f}')

  col2.metric('Their interest rate is', f'{int_rate_info}%')

  if loan_status_info.iloc[0].name == True:
    status = 'Active'
  else:
    status = 'Inactive'
  col2.metric('The status of their loan is ', status)

  col2.metric('Their DTI is', f'{dti_info:,.2%}')

  if default_status_info.iloc[0].name == True:
    default_status = 'Defaulted'
  else:
    default_status = 'Not Defaulted'
  col2.metric('Their loan is', default_status)

  col2.metric('They have a credit history of', f'{int(credit_history_length)} years')