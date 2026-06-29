import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
st.title("IBM Churn Dashboard")
@st.cache_data
def load_data():
  df = pd.read_csv("data/IBM_Churn.csv")
  
  # Convert TotalCharges to numeric
  df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
  df = df.dropna()
  
  return df

df = load_data()


# -----------------------------------
# Sidebar Filters
# -----------------------------------
st.sidebar.header("Filters")

# Churn Filter
churn_option = st.sidebar.selectbox(
    "Select Churn Status",
    ["Both", "Yes", "No"]
)

# Contract Filter
contract_option = st.sidebar.multiselect(
    "Select Contract Type",
    options=df["Contract"].unique(),
    default=df["Contract"].unique()
)

# Tenure Slider
tenure_range = st.sidebar.slider(
    "Tenure Range",
    int(df["tenure"].min()),
    int(df["tenure"].max()),
    (
        int(df["tenure"].min()),
        int(df["tenure"].max())
    )
)

# -----------------------------------
# Apply Filters
# -----------------------------------
filtered_df = df.copy()

filtered_df = filtered_df[
    filtered_df["Contract"].isin(contract_option)
]

filtered_df = filtered_df[
    (filtered_df["tenure"] >= tenure_range[0]) &
    (filtered_df["tenure"] <= tenure_range[1])
]

if churn_option != "Both":
    filtered_df = filtered_df[
        filtered_df["Churn"] == churn_option
    ]

# -----------------------------------
# KPI Metrics
# -----------------------------------
st.subheader("Dashboard Summary")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Total Customers",
        len(filtered_df)
    )

with col2:
    st.metric(
        "Average Monthly Charges",
        f"${filtered_df['MonthlyCharges'].mean():.2f}"
    )

with col3:
    churn_rate = (
        filtered_df["Churn"]
        .value_counts(normalize=True)
        .get("Yes", 0) * 100
    )

    st.metric(
        "Churn Rate",
        f"{churn_rate:.2f}%"
    )

st.divider()

# ===================================
# Chart 1
# Histogram
# ===================================
st.subheader("1. Distribution of Monthly Charges")

fig1, ax1 = plt.subplots(figsize=(8,5))

sns.histplot(
    filtered_df["MonthlyCharges"],
    bins=20,
    kde=True,
    color="steelblue",
    ax=ax1
)

ax1.set_xlabel("Monthly Charges")
ax1.set_ylabel("Count")

st.pyplot(fig1)

# ===================================
# Chart 2
# Scatter Plot
# ===================================
st.subheader("2. Tenure vs Monthly Charges")

fig2, ax2 = plt.subplots(figsize=(8,6))

sns.scatterplot(
    data=filtered_df,
    x="tenure",
    y="MonthlyCharges",
    hue="Churn",
    alpha=0.7,
    ax=ax2
)

ax2.set_xlabel("Tenure")
ax2.set_ylabel("Monthly Charges")

st.pyplot(fig2)

# ===================================
# Chart 3
# Count Plot
# ===================================
st.subheader("3. Contract Type vs Churn")

fig3, ax3 = plt.subplots(figsize=(8,5))

sns.countplot(
    data=filtered_df,
    x="Contract",
    hue="Churn",
    ax=ax3
)

ax3.set_xlabel("Contract")
ax3.set_ylabel("Customer Count")

st.pyplot(fig3)

# -----------------------------------
# Display Data
# -----------------------------------
st.divider()

st.subheader("Filtered Dataset")

st.dataframe(filtered_df)

# -----------------------------------
# Download Button
# -----------------------------------
csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📥 Download Filtered Data",
    data=csv,
    file_name="filtered_telco_customers.csv",
    mime="text/csv"
)
