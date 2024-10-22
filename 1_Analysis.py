import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(layout="wide", initial_sidebar_state="expanded", page_title="Amazon Sales Report", page_icon=":bar_chart:")

st.title('')

df=pd.read_csv('Amazon Sale Report.csv')
df=df.drop_duplicates()


df['currency'].fillna(df['currency'].mode()[0], inplace=True)
df.drop(['New','PendingS','fulfilled-by'],axis=1,inplace=True)
df['Amount'].fillna(df['Amount'].mean(), inplace=True)
df['ship-postal-code'].fillna(df['ship-postal-code'].median(), inplace=True)
df['ship-city'].fillna(df['ship-city'].mode()[0], inplace=True)
df['ship-state'].fillna(df['ship-state'].mode()[0], inplace=True)
df['ship-country'].fillna(df['ship-country'].mode()[0], inplace=True)
df['Date'] = pd.to_datetime(df['Date'])
df['month'] = df['Date'].dt.month
monthly_data = df.groupby('month').agg({'Amount': 'sum', 'Qty': 'sum'})

col1, col2 = st.columns(2)

col1.header('# of Orders Ber Month In 2022')
category_counts =monthly_data['Qty']
labels = category_counts.index
sizes = category_counts.values
plt.figure(figsize=(10, 6))
plt.pie(sizes, labels=labels, autopct='%1.1f%%', colors=plt.cm.Paired.colors)
plt.axis('equal')
col1.pyplot(plt)


col2.header('Selling by Fulfilment')
F=df['Fulfilment'].value_counts()
F_counts = F.reset_index()
F_counts.columns = ['Fulfilment', 'Count']

plt.figure(figsize=(8, 5))
bars = sns.barplot(x=F_counts['Fulfilment'], y=F_counts['Count'], color='b', lw=3, alpha=.6)

for bar in bars.patches:
    plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 100,
             f'{int(bar.get_height())}',
             ha='center', va='bottom')

plt.ylabel('Number of Units')
plt.tight_layout()
col2.pyplot(plt)


st.divider()

st.header('Order Status vs. Count')
S = df['Status'].value_counts()

shipped = S[['Shipped', 'Shipped - Delivered to Buyer', 'Shipped - Picked Up', 'Shipped - Returned to Seller',
        'Shipped - Returning to Seller','Shipped - Rejected by Buyer']]

shipping = S[['Pending - Waiting for Pick Up', 'Pending','Shipped - Out for Delivery']]

non_shipped = S[['Cancelled','Shipped - Lost in Transit']]

plt.figure(figsize=(10, 6))
plt.barh(shipped.index, shipped.values, color='green', label='Arrived to Buyer')
plt.barh(shipping.index, shipping.values, color='blue', label='Waitting for Picked Up')
plt.barh(non_shipped.index, non_shipped.values, color='red', label='Not Arrived to Buyer')
plt.xlabel('Count')
plt.ylabel('Order Status')
plt.legend()
plt.tight_layout()
st.pyplot(plt)

st.divider()

st.header('Ship Service Level')
SC=df['Sales Channel'].value_counts()
SCL=df['ship-service-level'].value_counts()
labels = SCL.index
sizes = SCL.values
plt.figure(figsize=(10, 6))
plt.pie(sizes, labels=labels, autopct='%1.1f%%',startangle=90, colors=plt.cm.Paired.colors)
plt.axis('equal')
st.pyplot(plt)

st.divider()

st.header('Top Selling')
C=df['Category'].value_counts()
C_counts = C.reset_index()
C_counts.columns = ['Category', 'Count']

plt.figure(figsize=(13, 6))
bars = sns.barplot(x=C_counts['Category'],y=C_counts['Count'],color='b',lw=6,alpha=.7)
for bar in bars.patches:
    plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(),
             f'{int(bar.get_height())}',
             ha='center', va='bottom')

plt.xticks(rotation=45, ha='right')
plt.ylabel('Number Of Unit')
plt.tight_layout()
st.pyplot(plt)

st.divider()


st.header('Category Distribution per Month')
dS=df[df['Category']=='T-shirt']
ds=dS['month'].value_counts()
ds_counts = ds.reset_index()
ds_counts.columns = ['month', 'Count']

S=df[df['Category']=='Shirt']
s=S['month'].value_counts()
s_counts = s.reset_index()
s_counts.columns = ['month', 'Count']

B=df[df['Category']=='Blazzer']
b=B['month'].value_counts()
b_counts = b.reset_index()
b_counts.columns = ['month', 'Count']

T=df[df['Category']=='Trousers']
t=T['month'].value_counts()
t_counts = t.reset_index()
t_counts.columns = ['month', 'Count']

# إعداد الشكل مع 4 محاور فرعية
fig, axes = plt.subplots(2, 2, figsize=(12, 7))

# رسم هيستوغرام لـ T-shirt
sns.histplot(data=ds_counts, x='month', weights='Count', color='#1f77b4', binwidth=1, ax=axes[0, 0], kde=False)
axes[0, 0].set_title('Distribution of T-shirt per Month')
axes[0, 0].set_xlabel('Month')
axes[0, 0].set_ylabel('Count')

# رسم هيستوغرام لـ Shirt
sns.histplot(data=s_counts, x='month', weights='Count', color='#d62728', binwidth=1, ax=axes[0, 1], kde=False)
axes[0, 1].set_title('Distribution of Shirt per Month')
axes[0, 1].set_xlabel('Month')
axes[0, 1].set_ylabel('Count')

# رسم هيستوغرام لـ Blazzer
sns.histplot(data=b_counts, x='month', weights='Count', color='#2ca02c', binwidth=1, ax=axes[1, 0], kde=False)
axes[1, 0].set_title('Distribution of Blazzer per Month')
axes[1, 0].set_xlabel('Month')
axes[1, 0].set_ylabel('Count')

# رسم هيستوغرام لـ Trousers
sns.histplot(data=t_counts, x='month', weights='Count', color='#ff7f0e', binwidth=1, ax=axes[1, 1], kde=False)
axes[1, 1].set_title('Distribution of Trousers per Month')
axes[1, 1].set_xlabel('Month')
axes[1, 1].set_ylabel('Count')

# تحسين المظهر
plt.tight_layout()
st.pyplot(fig)

st.divider()

st.header('Comparison of Sales by Category per Month')
combined_data = pd.DataFrame({
    'month': ds_counts['month'],
    'T-shirt': ds_counts['Count'],
    'Shirt': s_counts['Count'],
    'Blazzer': b_counts['Count'],
    'Trousers': t_counts['Count']
})
combined_data_melt = combined_data.melt(id_vars='month', var_name='Category', value_name='Count')
plt.figure(figsize=(15, 7))
sns.barplot(data=combined_data_melt, x='month', y='Count', hue='Category')
plt.xlabel('Month')
plt.ylabel('Sales Count')

plt.legend(title='Category')
st.pyplot(plt)

st.divider()

st.header('Courier Status')
CS=df['Courier Status'].value_counts()
cs_counts = CS.reset_index()
cs_counts.columns = ['Courier Status', 'Count']
plt.figure(figsize=(13, 6))
bars = sns.barplot(x=cs_counts['Courier Status'],y=cs_counts['Count'],color='b',lw=6,alpha=.7)
for bar in bars.patches:
    plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(),
             f'{int(bar.get_height())}',
             ha='center', va='bottom')

plt.xticks(rotation=45, ha='right')
plt.ylabel('Count')
st.pyplot(plt)

st.divider()

col1, col2 = st.columns(2)
col1.header('Heatmap of Status vs. Courier Status')
status_vs_courier = df.pivot_table(index='Status', columns='Courier Status', aggfunc='size', fill_value=0)
plt.figure(figsize=(10, 6))
sns.heatmap(status_vs_courier, annot=True, cmap="Blues", fmt="d")
col1.pyplot(plt)

col2.header('Heatmap of Quantity vs. Courier Status')
QH=df.pivot_table(index='Qty', columns='Courier Status', aggfunc='size', fill_value=0)
plt.figure(figsize=(10, 6))
sns.heatmap(QH, annot=True, cmap="Blues", fmt="d")
col2.pyplot(plt)

st.divider()

st.header('Number of Orders by City')
sci=df['ship-city'].value_counts()
sci_counts = sci.reset_index()
sci_counts.columns = ['ship-city', 'Count']
sci_counts=sci_counts.head(15)
plt.figure(figsize=(12, 8))
sci_counts.sort_values('Count', ascending=False, inplace=True)
plt.bar(sci_counts['ship-city'], sci_counts['Count'], color='skyblue')
plt.xticks(rotation=45)
plt.xlabel('City')
plt.ylabel('Number of Orders')
st.pyplot(plt)

st.divider()

st.header('Amount & Ship Postal Code')
plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)
sns.boxplot(y=df['Amount'], color='skyblue')
plt.title('Boxplot of Amount')
plt.ylabel('Amount')

plt.subplot(1, 2, 2)
sns.boxplot(y=df['ship-postal-code']/10, color='lightgreen')
plt.title('Boxplot of ship-postal-code')
plt.ylabel('ship-postal-code  x10')
plt.tight_layout()
st.pyplot(plt)

st.divider()

st.header('Number of Orders by State')
ss=df['ship-state'].value_counts()
ss_counts = ss.reset_index()
ss_counts.columns = ['ship-state', 'Count']
ss_counts=ss_counts.head(15)
plt.figure(figsize=(12, 6))
plt.bar(ss_counts['ship-state'], ss_counts['Count'], color='skyblue')

plt.xticks(rotation=45)
plt.xlabel('State')
plt.ylabel('Count')
plt.tight_layout()
st.pyplot(plt)
