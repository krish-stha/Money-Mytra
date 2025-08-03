import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import sys
import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from dotenv import load_dotenv
from utils.logging_utils import setup_logging

log = setup_logging("expense_tracker_analytics")
st.set_page_config(layout='wide')
load_dotenv()



@st.cache_resource
def get_google_sheets_service():
    try:
        creds = service_account.Credentials.from_service_account_file(
            os.getenv('GOOGLE_SHEETS_CREDENTIALS'),
            scopes=['https://www.googleapis.com/auth/spreadsheets']
        )
        service = build('sheets', 'v4', credentials=creds)
        return service
    except Exception as e:
        log.error(f"❌ Failed to connect to Google Sheets: {e}")
        raise

try:
    service = get_google_sheets_service()
    SHEET_ID = os.getenv('GOOGLE_SHEET_ID')
except Exception:
    st.error("Failed to connect to Google Sheets. Please check your credentials.")
    sys.exit(1)

@st.cache_data(ttl=300)
def get_transactions_data():
    try:
        result = service.spreadsheets().values().get(
            spreadsheetId=SHEET_ID,
            range='Expenses!A1:F'
        ).execute()
        values = result.get('values', [])
        if not values:
            log.warning("No transaction data found in sheet")
            return pd.DataFrame(columns=['Date', 'Amount', 'Type', 'Category', 'Subcategory', 'Description'])

        df = pd.DataFrame(values[1:], columns=['Date', 'Amount', 'Type', 'Category', 'Subcategory', 'Description'])
        df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce')
        df['Date_raw'] = df['Date'].astype(str)
        df['Date'] = pd.to_datetime(df['Date_raw'], format='%Y-%m-%d', errors='coerce')
        mask_serial = df['Date'].isna() & df['Date_raw'].str.match(r'^\d+$')
        if mask_serial.any():
            df.loc[mask_serial, 'Date'] = (
                pd.to_datetime('1899-12-30') + 
                pd.to_timedelta(df.loc[mask_serial, 'Date_raw'].astype(int), unit='D')
            )
        df.dropna(subset=['Date', 'Amount', 'Type'], inplace=True)
        log.info(f"Retrieved {len(df)} transaction records after cleaning")
        return df
    except Exception as e:
        log.error(f"❌ Failed to fetch transactions data: {e}")
        raise

@st.cache_data(ttl=300)
def get_pending_transactions() -> pd.DataFrame:
    try:
        result = service.spreadsheets().values().get(
            spreadsheetId=SHEET_ID,
            range='Pending!A1:G'
        ).execute()
        values = result.get('values', [])
        if not values:
            log.warning("No data found in Pending sheet")
            return pd.DataFrame(columns=['Date', 'Amount', 'Type', 'Category', 'Description', 'Due Date', 'Status'])

        df = pd.DataFrame(values[1:], columns=['Date', 'Amount', 'Type', 'Category', 'Description', 'Due Date', 'Status'])
        df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce')

        df['Date_raw'] = df['Date'].astype(str)
        df['Date'] = pd.to_datetime(df['Date_raw'], format='%Y-%m-%d', errors='coerce')
        serial_mask = df['Date'].isna() & df['Date_raw'].str.match(r'^\d+$')
        if serial_mask.any():
            df.loc[serial_mask, 'Date'] = (
                pd.to_datetime('1899-12-30') + 
                pd.to_timedelta(df.loc[serial_mask, 'Date_raw'].astype(int), unit='D')
            )

        df['Due_Date_raw'] = df['Due Date'].astype(str)
        df['Due Date'] = pd.to_datetime(df['Due_Date_raw'], format='%Y-%m-%d', errors='coerce')
        serial_due_mask = df['Due Date'].isna() & df['Due_Date_raw'].str.match(r'^\d+$')
        if serial_due_mask.any():
            df.loc[serial_due_mask, 'Due Date'] = (
                pd.to_datetime('1899-12-30') + 
                pd.to_timedelta(df.loc[serial_due_mask, 'Due_Date_raw'].astype(int), unit='D')
            )

        df['Type'] = df['Type'].str.strip().str.title()
        df['Status'] = df['Status'].str.strip().str.title()

        df = df[df['Status'] == 'Pending']

        df.dropna(subset=['Date', 'Amount', 'Type'], inplace=True)
        log.info(f"📊 Retrieved {len(df)} pending transactions")
        return df
    except Exception as e:
        log.error(f"❌ Failed to fetch pending transactions: {e}")
        raise

def initialize_filters():
    if 'global_filter_type' not in st.session_state:
        st.session_state.global_filter_type = "All Time"
    if 'global_selected_year' not in st.session_state:
        st.session_state.global_selected_year = datetime.now().year
    if 'global_selected_month' not in st.session_state:
        st.session_state.global_selected_month = datetime.now().month
    if 'global_start_date' not in st.session_state:
        st.session_state.global_start_date = datetime.now() - timedelta(days=30)
    if 'global_end_date' not in st.session_state:
        st.session_state.global_end_date = datetime.now()

def get_date_filters(key:str="global_filter"):
    initialize_filters()
    st.sidebar.subheader("📅 Date Filter")
    df = get_transactions_data()
    if not df.empty:
        min_date = df['Date'].min()
        max_date = df['Date'].max()
    else:
        min_date = max_date = datetime.now()
    st.session_state.global_filter_type = st.sidebar.radio(
        "Select Time Period",
        ["All Time", "Year", "Month", "Custom Range"],
        key=key
    )
    if st.session_state.global_filter_type == "Year":
        st.session_state.global_selected_year = st.sidebar.selectbox(
            "Select Year",
            sorted(df['Date'].dt.year.unique(), reverse=True),
            key=key+"_year"
        )
        start_date = datetime(st.session_state.global_selected_year, 1, 1)
        end_date = datetime(st.session_state.global_selected_year, 12, 31)
    elif st.session_state.global_filter_type == "Month":
        st.session_state.global_selected_year = st.sidebar.selectbox(
            "Select Year",
            sorted(df['Date'].dt.year.unique(), reverse=True),
            key=key+"_month_year"
        )
        st.session_state.global_selected_month = st.sidebar.selectbox(
            "Select Month",
            range(1, 13),
            format_func=lambda x: datetime(2000, x, 1).strftime('%B'),
            key=key+"_month"
        )
        year = st.session_state.global_selected_year
        month = st.session_state.global_selected_month
        start_date = datetime(year, month, 1)
        if month < 12:
            end_date = datetime(year, month+1, 1) - timedelta(days=1)
        else:
            end_date = datetime(year+1, 1, 1) - timedelta(days=1)
    elif st.session_state.global_filter_type == "Custom Range":
        col1, col2 = st.sidebar.columns(2)
        with col1:
            st.session_state.global_start_date = st.date_input(
                "Start Date", 
                min_date.date(),
                key=key+"_start"
            )
        with col2:
            st.session_state.global_end_date = st.date_input(
                "End Date", 
                max_date.date(),
                key=key+"_end"
            )
        start_date = datetime.combine(st.session_state.global_start_date, datetime.min.time())
        end_date = datetime.combine(st.session_state.global_end_date, datetime.max.time())
    else:
        start_date = min_date
        end_date = max_date
    return start_date, end_date

def filter_dataframe(df, start_date, end_date):
    if df.empty:
        return df
    return df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]

def show_overview_analytics(df):
    st.subheader("📈 Financial Overview")
    if df.empty:
        st.info("No transactions found for the selected period.")
        return
    total_income = df[df['Type'] == 'Income']['Amount'].sum()
    total_expense = df[df['Type'] == 'Expense']['Amount'].sum()
    net_savings = total_income - total_expense
    saving_rate = (net_savings / total_income * 100) if total_income > 0 else 0
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Income", f"Rs. {total_income:,.2f}")
    with col2:
        st.metric("Total Expenses", f"Rs. {total_expense:,.2f}")
    with col3:
        st.metric("Net Savings", f"Rs. {net_savings:,.2f}",
                 delta_color="normal" if net_savings >= 0 else "inverse")
    with col4:
        st.metric("Saving Rate", f"{saving_rate:.1f}%")
    monthly = df.groupby([df['Date'].dt.strftime('%Y-%m'), 'Type'])['Amount'].sum().unstack(fill_value=0)
    monthly['Net'] = monthly.get('Income', 0) - monthly.get('Expense', 0)
    fig_monthly = px.bar(monthly, 
                         title='Monthly Income vs Expenses',
                         barmode='group',
                         labels={'value': 'Amount (Rs.)', 'index': 'Month'})
    st.plotly_chart(fig_monthly, use_container_width=True)
    st.dataframe(monthly.style.format({
        'Income': 'Rs. {:,.2f}',
        'Expense': 'Rs. {:,.2f}',
        'Net': 'Rs. {:,.2f}'
    }), height=200, use_container_width=True)
    st.subheader("Recent Transactions")
    recent_df = df.sort_values('Date', ascending=False).head(5)
    st.dataframe(
        recent_df[['Date','Type','Category','Subcategory','Amount','Description']].style.format({
            'Amount': 'Rs. {:,.2f}',
            'Date': lambda x: x.strftime('%Y-%m-%d')
        }), 
        use_container_width=True, hide_index=True
    )
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Top Income Categories")
        income_by_cat = df[df['Type']=='Income'].groupby('Category')['Amount'].sum().nlargest(5)
        fig_inc = px.pie(values=income_by_cat.values, names=income_by_cat.index, title='Top Income Sources')
        st.plotly_chart(fig_inc, use_container_width=True)
    with col2:
        st.subheader("Top Expense Categories")
        expense_by_cat = df[df['Type']=='Expense'].groupby('Category')['Amount'].sum().nlargest(5)
        fig_exp = px.pie(values=expense_by_cat.values, names=expense_by_cat.index, title='Top Expense Categories')
        st.plotly_chart(fig_exp, use_container_width=True)
    st.subheader("💡 Spending Insights")
    df['Day_Type'] = df['Date'].dt.dayofweek.map(lambda x: 'Weekend' if x>=5 else 'Weekday')
    daily_spend = df[df['Type']=='Expense'].groupby('Day_Type')['Amount'].agg(['sum','count'])
    daily_spend['avg'] = daily_spend['sum'] / daily_spend['count']
    st.caption("Weekday vs Weekend Spending")
    st.dataframe(daily_spend.style.format({
        'sum': 'Rs. {:,.2f}',
        'avg': 'Rs. {:,.2f}/day'
    }))
    df['Week_of_Month'] = df['Date'].dt.day.map(lambda x: (x-1)//7 + 1)
    weekly_avg = df[df['Type']=='Expense'].groupby('Week_of_Month')['Amount'].mean()
    fig_weekly = px.bar(weekly_avg, title='Average Spending by Week of Month',
                        labels={'value': 'Amount (Rs.)','Week_of_Month':'Week'})
    st.plotly_chart(fig_weekly, use_container_width=True)

def show_income_analytics(df):
    st.subheader("💰 Income Analytics")
    if df.empty or 'Income' not in df['Type'].unique():
        st.info("No income transactions found for the selected period.")
        return
    income_df = df[df['Type']=='Income']
    monthly_income = income_df.groupby(income_df['Date'].dt.strftime('%Y-%m'))['Amount'].sum()
    fig_month_inc = px.bar(monthly_income, title='Monthly Income Trend',
                           labels={'value': 'Amount (Rs.)','index': 'Month'})
    st.plotly_chart(fig_month_inc, use_container_width=True)
    col1, col2 = st.columns(2)
    with col1:
        fig_cat_inc = px.pie(income_df, values='Amount', names='Category', title='Income by Category')
        st.plotly_chart(fig_cat_inc, use_container_width=True)
    with col2:
        st.subheader("Top Income Sources")
        top_src = income_df.groupby('Category')['Amount'].sum().sort_values(ascending=False)
        st.dataframe(top_src.to_frame().style.format({'Amount': 'Rs. {:,.2f}'}), height=300, use_container_width=True)
    st.subheader("Income by Subcategory")
    subcat_inc = income_df.groupby('Subcategory')['Amount'].sum().sort_values(ascending=False)
    fig_sub_inc = px.bar(subcat_inc, title='Income by Subcategory',
                         labels={'value': 'Amount (Rs.)','index':'Subcategory'})
    st.plotly_chart(fig_sub_inc, use_container_width=True)
    monthly_totals = monthly_income
    stats = {
        'Average Monthly Income': monthly_totals.mean(),
        'Income Volatility': (monthly_totals.std() / monthly_totals.mean() if monthly_totals.mean()!=0 else 0),
        'Highest Income Month': monthly_totals.max(),
        'Lowest Income Month': monthly_totals.min(),
        'Months of Income': len(monthly_totals)
    }
    st.subheader("💰 Income Stability Analysis")
    st.dataframe(pd.Series(stats).to_frame('Value').style.format({
        'Value': lambda x: f"Rs. {x:,.2f}" if isinstance(x, (int, float)) and x > 100 else f"{x:.2%}" if isinstance(x, float) else x
    }))

def show_expense_analytics(df):
    st.subheader("💸 Expense Analytics")
    if df.empty or 'Expense' not in df['Type'].unique():
        st.info("No expense transactions found for the selected period.")
        return
    expense_df = df[df['Type']=='Expense']
    monthly_exp = expense_df.groupby(expense_df['Date'].dt.strftime('%Y-%m'))['Amount'].sum()
    fig_month_exp = px.bar(monthly_exp, title='Monthly Expense Trend',
                           labels={'value': 'Amount (Rs.)','index':'Month'})
    st.plotly_chart(fig_month_exp, use_container_width=True)
    col1, col2 = st.columns(2)
    with col1:
        fig_cat_exp = px.pie(expense_df, values='Amount', names='Category', title='Expenses by Category')
        st.plotly_chart(fig_cat_exp, use_container_width=True)
    with col2:
        st.subheader("Top Expense Categories")
        top_exp = expense_df.groupby('Category')['Amount'].sum().sort_values(ascending=False)
        st.dataframe(top_exp.to_frame().style.format({'Amount': 'Rs. {:,.2f}'}), height=300, use_container_width=True)
    st.subheader("Expenses by Subcategory")
    subcat_exp = expense_df.groupby('Subcategory')['Amount'].sum().sort_values(ascending=False)
    fig_sub_exp = px.bar(subcat_exp, title='Expenses by Subcategory',
                         labels={'value': 'Amount (Rs.)','index':'Subcategory'})
    st.plotly_chart(fig_sub_exp, use_container_width=True)

    # Average Daily Spending by Month
    expense_df['Month'] = expense_df['Date'].dt.to_period('M')
    monthly_totals = expense_df.groupby('Month')['Amount'].sum()
    days_in_month = expense_df.groupby('Month')['Date'].apply(lambda x: x.dt.daysinmonth.iloc[0])
    avg_daily = (monthly_totals / days_in_month).rename("Avg_Daily")
    st.subheader("Average Daily Spending by Month")
    st.dataframe(avg_daily.to_frame().style.format({'Avg_Daily': 'Rs. {:,.2f}'}))

    # Expense Consistency Analysis
    monthly_cat = expense_df.groupby(['Category', expense_df['Date'].dt.strftime('%Y-%m')])['Amount'].sum()
    consistency = monthly_cat.groupby('Category').agg(['mean','std'])
    consistency['variation'] = consistency['std'] / consistency['mean']

    fixed = consistency[consistency['variation'] < 0.2]
    variable = consistency[consistency['variation'] >= 0.2]

    col1, col2 = st.columns(2)
    with col1:
        st.caption("Fixed Expenses (Low Variation)")
        st.dataframe(fixed.style.format({'mean': 'Rs. {:,.2f}', 'std': 'Rs. {:,.2f}', 'variation': '{:.2%}'}))
    with col2:
        st.caption("Variable Expenses (High Variation)")
        st.dataframe(variable.style.format({'mean': 'Rs. {:,.2f}', 'std': 'Rs. {:,.2f}', 'variation': '{:.2%}'}))

def main():
    st.title("💸Money Mytra's Analytics")
    start_date, end_date = get_date_filters()
    
    df = get_transactions_data()
    filtered_df = filter_dataframe(df, start_date, end_date)

        # Refresh button
    if st.sidebar.button("🔄 Refresh Data"):
        get_transactions_data.clear()
        get_pending_transactions.clear()
        st.rerun()


    # Sidebar for navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Overview", "Income Analytics", "Expense Analytics", "Pending Transactions"])

    if page == "Overview":
        show_overview_analytics(filtered_df)
    elif page == "Income Analytics":
        show_income_analytics(filtered_df)
    elif page == "Expense Analytics":
        show_expense_analytics(filtered_df)
    elif page == "Pending Transactions":
        pending_df = get_pending_transactions()
        st.subheader("🕓 Pending Transactions")
        if pending_df.empty:
            st.info("No pending transactions found.")
        else:
            st.dataframe(pending_df.style.format({
                'Amount': 'Rs. {:,.2f}',
                'Date': lambda x: x.strftime('%Y-%m-%d'),
                'Due Date': lambda x: x.strftime('%Y-%m-%d')
            }), use_container_width=True)
if __name__ == "__main__":
    main()
       
