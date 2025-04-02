
import pandas as pd
import os
import paneltime as pt
import numpy as np
from matplotlib import pyplot as plt
import pickle
import statsmodels.api as sm


FLDR = os.path.dirname(__file__)

pt.options.pqdkm = (0,0,0,2,2)
pt.options.max_iterations = 5000
pt.options.supress_output = True

def main():

	df = pd.read_csv(f'{FLDR}/derivative.csv', sep=';')
	df = df.sort_values('date')
	df['dp'] = np.log(df['Adjusted Price']).diff()
	
	if os.path.exists(f'{FLDR}/output/deriv_pred.dmp'):
		with open(f'{FLDR}/output/deriv_pred.dmp', 'rb') as f:
			res = pickle.load(f)
	
	else:
		pred = []
		observed_vol = []
		observed_setl = []

		start_date = df.index[99]
		r = pt.execute('dp', df[df.index<start_date])
		pred_var = r.predict().loc[(1,start_date), 'Predicted variance']

		res = pd.DataFrame()

		for dt in df.index[100:]:
			data = df[df.index<dt]
			r = pt.execute('dp', data)
			pr = r.predict()
			d = data.iloc[-1]
			new_row = pd.DataFrame([{
					'Date':d['date'], 
				  	'Implicit Volatility':d['VolatilityForValuation'], 
					'Predicted variance': pred_var, 
					'Fitted variance': pr.loc[(1,dt-1), 'Fitted variance'],
					'OptionPrice':d['Settlement'],
					}])
			res = pd.concat([res, new_row], axis=0)
			pred_var = pr.loc[(1,dt), 'Predicted variance']
			res.to_pickle(f'{FLDR}/output/deriv_pred.dmp')
			print(f'Adding row {dt} of {df.index[-1]}')	

	f1 = res.plot.scatter('Predicted variance', 'Fitted variance').get_figure()
	f2 = res.plot.scatter('Predicted variance', 'OptionPrice').get_figure()	
	f1.show()
	f2.show()

	f1.savefig(f'{FLDR}/figures/volatility.png')
	f2.savefig(f'{FLDR}/figures/settlement.png')
	ols(res['Predicted variance'], res['Fitted variance'], 'Predicted variance', 'Fitted variance')
	ols(res['Predicted variance'], res['OptionPrice'], 'Predicted variance', 'OptionPrice')

	a=0



def ols(x, y, namex, namey):
	
	data = pd.DataFrame({namex:x, namey:y})
	data = data.diff().dropna()
	X = sm.add_constant(data[namex])
	model = sm.OLS(data[namey], X).fit()
	print(model.summary())
	return model, X



def plot(x,y, namex, namey):
	fig, ax = plt.subplots(figsize=(8, 8))
	ax.scatter(x, y, alpha=0.7)

	# Labels and title
	ax.set_xlabel(namex)
	ax.set_ylabel(namey)
	ax.set_title(f"{namey} and {namex}")
	return fig


main()