import pandas as pd

total_risk_path = r"C:\\Users\\matthewsm\\OneDrive - Enstargroup\\ERM Risk Folder\\Group\\Model Risk Management\\CTAL\\2026\\2026 01 Update\\0. Data\\_sims\\5954 (exported by AP)\\One-Year Total Risk Sims.csv"
num_sims = 51

return_periods = [2,5,10,20,50,100,200,500]
percentiles = [1/rp for rp in return_periods]

df = pd.read_csv(total_risk_path)

#Removing non egl_group fields
df = df.loc[(df['Entity'] == 'egl_group')]

#Manipulating table for ease in excel
df = df.pivot(index='Sim', columns='Risk', values='Value')
df = df.reset_index()  # brings back sim column

#DF Can now be exported for plotting in AllRisk

#Finding corridor for sims
tot_sims = len(df)
lower_bound = int(tot_sims*0.05 - num_sims//2 - 1)
upper_bound = int(tot_sims*0.05 + num_sims//2)

corridor = df[lower_bound:upper_bound]

#Taking percentiles and ajusting cols
loss_table = df.drop(columns=['Risk','Sim'], errors = 'ignore')
loss_table = loss_table.quantile(percentiles)
loss_table = loss_table.reset_index()

#Convert to Milions for all but first col
loss_table = loss_table.iloc[:,1:]/1_000_000

#Formatting Headers
headers = [f'1 in {rp} Year' for rp in return_periods]

#Insert return periods, reorder and transpose
loss_table.insert(0, 'Return Period', headers)
col_order = [ "Total Insurance Risk",
    "Total Market Risk",
    "Total Credit Risk",
    "Total Operational Risk",
    "Total SCR"
]


loss_table = loss_table.reindex(columns=col_order)
loss_table= loss_table.T

print(loss_table)

#Write to excel
#table.to_excel('total_risk_table.xlsx', index = False)
#corridor.to_excel('simulation_corridor_data.xlsx, index = False')

