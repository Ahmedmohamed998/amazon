import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(layout="wide", initial_sidebar_state="expanded", page_title="Amazon Sales Report", page_icon=":bar_chart:")

st.title('')

df = pd.read_csv('Amazon Sale Report.csv')
df = df.drop_duplicates()

df['currency'].fillna(df['currency'].mode()[0], inplace=True)
df.drop(['New','PendingS','fulfilled-by'], axis=1, inplace=True)
df['Amount'].fillna(df['Amount'].mean(), inplace=True)
df['ship-postal-code'].fillna(df['ship-postal-code'].median(), inplace=True)
df['ship-city'].fillna(df['ship-city'].mode()[0], inplace=True)
df['ship-state'].fillna(df['ship-state'].mode()[0], inplace=True)
df['ship-country'].fillna(df['ship-country'].mode()[0], inplace=True)
df['Date'] = pd.to_datetime(df['Date'])
df['month'] = df['Date'].dt.month
monthly_data = df.groupby('month').agg({'Amount': 'sum', 'Qty': 'sum'})

col1, col2 = st.columns(2)

# Plot 1: Orders Per Month Pie Chart
col1.header('# of Orders Per Month In 2022')
category_counts = monthly_data['Qty']
labels = category_counts.index
sizes = category_counts.values
fig, ax = plt.subplots(figsize=(10, 6))
ax.pie(sizes, labels=labels, autopct='%1.1f%%', colors=plt.cm.Paired.colors)
ax.axis('equal')
col1.pyplot(fig)
plt.close(fig)

# Plot 2: Selling by Fulfillment Bar Plot
col2.header('Selling by Fulfillment')
F = df['Fulfilment'].value_counts()
F_counts = F.reset_index()
F_counts.columns = ['Fulfilment', 'Count']

fig, ax = plt.subplots(figsize=(8, 5))
bars = sns.barplot(x=F_counts['Fulfilment'], y=F_counts['Count'], color='b', lw=3, alpha=.6, ax=ax)

for bar in bars.patches:
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 100,
            f'{int(bar.get_height())}',
            ha='center', va='bottom')

ax.set_ylabel('Number of Units')
plt.tight_layout()
col2.pyplot(fig)
plt.close(fig)

st.divider()

# Plot 3: Order Status vs. Count
st.header('Order Status vs. Count')
S = df['Status'].value_counts()

shipped = S[['Shipped', 'Shipped - Delivered to Buyer', 'Shipped - Picked Up', 'Shipped - Returned to Seller',
        'Shipped - Returning to Seller', 'Shipped - Rejected by Buyer']]

shipping = S[['Pending - Waiting for Pick Up', 'Pending', 'Shipped - Out for Delivery']]

non_shipped = S[['Cancelled', 'Shipped - Lost in Transit']]

fig, ax = plt.subplots(figsize=(10, 6))
ax.barh(shipped.index, shipped.values, color='green', label='Arrived to Buyer')
ax.barh(shipping.index, shipping.values, color='blue', label='Waiting for Pickup')
ax.barh(non_shipped.index, non_shipped.values, color='red', label='Not Arrived to Buyer')
ax.set_xlabel('Count')
ax.set_ylabel('Order Status')
ax.legend()
plt.tight_layout()
st.pyplot(fig)
plt.close(fig)

st.divider()

# Plot 4: Ship Service Level Pie Chart
st.header('Ship Service Level')
SCL = df['ship-service-level'].value_counts()
labels = SCL.index
sizes = SCL.values

fig, ax = plt.subplots(figsize=(10, 6))
ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=plt.cm.Paired.colors)
ax.axis('equal')
st.pyplot(fig)
plt.close(fig)

st.divider()

# Plot 5: Top Selling Categories Bar Plot
st.header('Top Selling')
C = df['Category'].value_counts()
C_counts = C.reset_index()
C_counts.columns = ['Category', 'Count']

fig, ax = plt.subplots(figsize=(13, 6))
bars = sns.barplot(x=C_counts['Category'], y=C_counts['Count'], color='b', lw=6, alpha=.7, ax=ax)
for bar in bars.patches:
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height(),
            f'{int(bar.get_height())}',
            ha='center', va='bottom')

plt.xticks(rotation=45, ha='right')
ax.set_ylabel('Number Of Units')
plt.tight_layout()
st.pyplot(fig)
plt.close(fig)

st.divider()

# Plot 6: Category Distribution per Month
st.header('Category Distribution per Month')

# Data preparation for categories
categories = ['T-shirt', 'Shirt', 'Blazzer', 'Trousers']
category_data = {}
for category in categories:
    category_df = df[df['Category'] == category]
    category_counts = category_df['month'].value_counts().reset_index()
    category_counts.columns = ['month', 'Count']
    category_data[category] = category_counts

fig, axes = plt.subplots(2, 2, figsize=(12, 7))

# Plotting for each category
for ax, (category, data) in zip(axes.flatten(), category_data.items()):
    sns.histplot(data=data, x='month', weights='Count', ax=ax, kde=False)
    ax.set_title(f'Distribution of {category} per Month')
    ax.set_xlabel('Month')
    ax.set_ylabel('Count')

plt.tight_layout()
st.pyplot(fig)
plt.close(fig)

st.divider()

# Plot 7: Comparison of Sales by Category per Month
st.header('Comparison of Sales by Category per Month')
combined_data = pd.DataFrame({
    'month': category_data['T-shirt']['month'],
    'T-shirt': category_data['T-shirt']['Count'],
    'Shirt': category_data['Shirt']['Count'],
    'Blazzer': category_data['Blazzer']['Count'],
    'Trousers': category_data['Trousers']['Count']
})
combined_data_melt = combined_data.melt(id_vars='month', var_name='Category', value_name='Count')

fig, ax = plt.subplots(figsize=(15, 7))
sns.barplot(data=combined_data_melt, x='month', y='Count', hue='Category', ax=ax)
ax.set_xlabel('Month')
ax.set_ylabel('Sales Count')
ax.legend(title='Category')
st.pyplot(fig)
plt.close(fig)

st.divider()

# Plot 8: Courier Status Bar Plot
st.header('Courier Status')
CS = df['Courier Status'].value_counts()
cs_counts = CS.reset_index()
cs_counts.columns = ['Courier Status', 'Count']

fig, ax = plt.subplots(figsize=(13, 6))
bars = sns.barplot(x=cs_counts['Courier Status'], y=cs_counts['Count'], color='b', lw=6, alpha=.7, ax=ax)
for bar in bars.patches:
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height(),
            f'{int(bar.get_height())}',
            ha='center', va='bottom')

plt.xticks(rotation=45, ha='right')
ax.set_ylabel('Count')
plt.tight_layout()
st.pyplot(fig)
plt.close(fig)

st.divider()

col1, col2 = st.columns(2)

# Plot 9: Heatmap of Status vs. Courier Status
col1.header('Heatmap of Status vs. Courier Status')
status_vs_courier = df.pivot_table(index='Status', columns='Courier Status', aggfunc='size', fill_value=0)

fig, ax = plt.subplots(figsize=(10, 6))
sns.heatmap(status_vs_courier, annot=True, cmap="Blues", fmt="d", ax=ax)
col1.pyplot(fig)
plt.close(fig)

# Plot 10: Heatmap of Quantity vs. Courier Status
col2.header('Heatmap of Quantity vs. Courier Status')
QH = df.pivot_table(index='Qty', columns='Courier Status', aggfunc='size', fill_value=0)

fig, ax = plt.subplots(figsize=(10, 6))
sns.heatmap(QH, annot=True, cmap="Blues", fmt="d", ax=ax)
col2.pyplot(fig)
plt.close(fig)

st.divider()

# Plot 11: Number of Orders by City
st.header('Number of Orders by City')
sci = df['ship-city'].value_counts().head(15)
sci_counts = sci.reset_index()
sci_counts.columns = ['ship-city', 'Count']

fig, ax = plt.subplots(figsize=(12, 8))
sci_counts.sort_values('Count', ascending=False, inplace=True)
ax.bar(sci_counts['ship-city'], sci_counts['Count'], color='skyblue')
plt.xticks(rotation=45)
ax.set_xlabel('City')
ax.set_ylabel('Number of Orders')
plt.tight_layout()
st.pyplot(fig)
plt.close(fig)

st.divider()

# Plot 12: Amount & Ship Postal Code Boxplot
st.header('Amount & Ship Postal Code')

fig, axes = plt.subplots(1, 2, figsize=(12, 6))

# Amount boxplot
sns.boxplot(y=df['Amount'], color='skyblue', ax=axes[0])
axes[0].set_title('Amount')

# Ship Postal Code boxplot
sns.boxplot(y=df['ship-postal-code'], color='lightgreen', ax=axes[1])
axes[1].set_title('Ship Postal Code')

plt.tight_layout()
st.pyplot(fig)
plt.close(fig)
