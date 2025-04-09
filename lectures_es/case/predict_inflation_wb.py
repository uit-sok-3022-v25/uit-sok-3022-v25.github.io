import pandas as pd
import numpy as np
import wbdata
import matplotlib.pyplot as plt
import statsmodels.api as sm
import paneltime as pt
import os

FLDR = os.path.dirname(__file__)
FIGPATH = f'{FLDR}/figures/scatter_wb.png'
PRED_DATAFILE = f'{FLDR}/output/pred_wb.dmp'

def main():
	data = get_data()
	data = santitize_pick_data(data)

	rng = np.sort(data['Year'].unique())
	rng = rng[rng>rng[30]] # Skip first 20 years	

	# Predict and compare if not already done
	if os.path.exists(PRED_DATAFILE):
		df_obs_vs_pred = pd.read_pickle(PRED_DATAFILE)
	else:
		df_obs_vs_pred = pd.DataFrame()
		for year in rng:
			df = predict_and_compare(data, year)
			df_obs_vs_pred = pd.concat((df_obs_vs_pred, df), axis=0)
			print(f"Predicted and compared for year {year}")
		df_obs_vs_pred.to_pickle(PRED_DATAFILE)
	model, X = ols(df_obs_vs_pred)
	fig = plot(df_obs_vs_pred, model, X)
	fig.show()
	fig.savefig(FIGPATH)


def get_data():
	# Fetch data from WB
	# Defining indicators to fetch from World Bank API
	indicators = {
		'NY.GDP.MKTP.KD.ZG': 'GDP_growth',        # GDP growth (% annual)
		'FP.CPI.TOTL.ZG': 'Inflation',            # Inflation (consumer price index, % annual)
		'FR.INR.LEND': 'Interest_rate',           # Lending interest rate (%)
		'NY.GNS.ICTR.ZS': 'Gross_Savings',        # Gross savings (% of GDP)
		'NE.CON.GOVT.ZS': 'Gov_Consumption',      # Government consumption (% of GDP)
		'SL.UEM.TOTL.ZS': 'Unemployment_rate',    # Unemployment rate (% of total labor force)
		'SL.EMP.TOTL.SP.ZS': 'Employment_rate',   # Employment to population ratio (% age 15+)
	}

	#Download if not already downloaded
	if os.path.exists(f'{FLDR}/data/wbdata.dmp'):
		data = pd.read_pickle(f'{FLDR}/data/wbdata.dmp')
	else:
		data = wbdata.get_dataframe(indicators)
		data.to_pickle(f'{FLDR}/data/wbdata.dmp')

	return data

def santitize_pick_data(data):
	data.reset_index(inplace=True)
	data.rename(columns={'date': 'Year', 'country': 'Country'}, inplace=True)
	data['Year'] = data['Year'].astype(int)
	data = data[abs(data['Inflation'])<30]


	data = pd.DataFrame(data[['Inflation', 'GDP_growth','Interest_rate',
						'Gross_Savings','Gov_Consumption','Year','Country']].dropna())
	
	return data

def predict_and_compare(data, max_year):

	data_test = data[data['Year']<max_year]

	pt.options.pqdkm = (1, 1, 0, 1, 2)
	m = pt.execute('Inflation~Intercept+GDP_growth+L(Inflation)+L(Interest_rate)+'
						'L(Gross_Savings)+D(L(Gov_Consumption))', data_test, 'Year', 'Country' )
	print(m)
	df = m.predict()

	df_observed = data[data['Year']==max_year].set_index(['Country', 'Year'])['Inflation']
	df_predicted = df.loc[(slice(None), max_year), m.prediction_names['Predicted']]
	df_obs_vs_pred = pd.concat((df_observed, df_predicted), axis=1).dropna()[['Inflation', 'Predicted Inflation']]

	return df_obs_vs_pred

def plot(df_obs_vs_pred, model, X, labels=False):
	# Scatter plot using Matplotlib
	MINVAL, MAXVAL = -15, 30
	fig, ax = plt.subplots(figsize=(8, 8))
	ax.scatter(df_obs_vs_pred['Inflation'], df_obs_vs_pred['Predicted Inflation'], alpha=0.7)

	# Annotate each point with the country name from the MultiIndex
	if labels:
		for (country, year), (x, y) in zip(df_obs_vs_pred.index, df_obs_vs_pred[['Inflation', 'Predicted Inflation']].values):
			ax.text(x, y, f"{country[:4]}({str(int(year))[-2:]})", fontsize=9, ha='right', va='bottom')

	# Labels and title
	ax.set_xlabel("Actual Inflation")
	ax.set_ylabel("Predicted Inflation")
	ax.set_title("Predicted and Actual Inflation 2023")
	ax.set_xlim(MINVAL, MAXVAL)
	ax.set_ylim(MINVAL, MAXVAL)

	intercept, slope = model.params
	x = np.linspace(min(X.iloc[:, 1]), max(X.iloc[:, 1]), 100) 
	ax.plot(intercept + slope * x, x, color='red', label='OLS')
	x = np.linspace(MINVAL, MAXVAL , 100) 
	ax.plot( x, x, color='lightgray', label='45 degree line')

	return fig


def ols(df_obs_vs_pred):
	# OLS regression
	X = sm.add_constant(df_obs_vs_pred['Predicted Inflation'])
	Y = df_obs_vs_pred['Inflation']
	model = sm.OLS(Y, X).fit()
	print(model.summary())

	return model, X

main()
