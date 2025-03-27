
import pandas as pd
import os
import paneltime as pt
import numpy as np
from matplotlib import pyplot as plt
import pickle
import statsmodels.api as sm


FLDR = os.path.dirname(__file__)

pt.options.pqdkm = (0,0,0,2,1)
pt.options.max_iterations = 5000
pt.options.supress_output = True

def main():

	df = pd.read_pickle(f'{FLDR}/output/derivative.dmp')
	df['dp'] = np.log(df['Adjusted Price']).sort_index().diff()
	
	if os.path.exists(f'{FLDR}/output/deriv_pred.dmp'):
		with open(f'{FLDR}/output/deriv_pred.dmp', 'rb') as f:
			(observed_vol, observed_setl, pred) = pickle.load(f)
	
	else:
		pred = []
		observed_vol = []
		observed_setl = []
		for dt in df.index[100:]:
			data = df[df.index<dt]
			r = pt.execute('dp', data)
			pr = r.predict()
			pred.append(pr.loc[dt, 'Predicted variance'])
			observed_vol.append(df.loc[dt,'Volatility'])
			observed_setl.append(df.loc[dt,'Settlement'])
			print(f"Predicted for date {dt} of {df.index[-1]}")

		with open(f'{FLDR}/output/deriv_pred.dmp', 'wb') as f:
			pickle.dump((observed_vol, observed_setl, pred), f)

	f1 = plot(observed_vol, pred, 'Observed Volatility', 'Predicted Volatility')	
	f2 = plot(observed_setl, pred, 'Observed Settlement', 'Predicted Volatility')
	f1.show()
	f2.show()
	f1.savefig(f'{FLDR}/figures/volatility.png')
	f2.savefig(f'{FLDR}/figures/settlement.png')
	ols(observed_vol, pred, 'Observed Volatility', 'Predicted Volatility')
	ols(observed_setl, pred,  'Observed Settlement', 'Predicted Volatility')

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