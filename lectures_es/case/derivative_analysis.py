
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

	# Get data from csv file
	df = pd.read_csv(f'{FLDR}/derivative.csv', sep=';')
	df = df.sort_values('date')
	df['dp'] = np.log(df['Adjusted Price']).diff()
	
	#Check if the predictions are already in the output folder
	if os.path.exists(f'{FLDR}/output/deriv_pred.dmp') and False:
		with open(f'{FLDR}/output/deriv_pred.dmp', 'rb') as f:
			res = pickle.load(f)
	
	else:
		# Obtaining the initial prediction for start_date, using only data prior to start_date
		# Will be compared to the observed data next day
		start_date = df.index[99]
		r = pt.execute('dp', df[df.index<start_date])
		pred_var = r.predict().loc[(1,start_date), 'Predicted variance']

		#Creating a new dataframe to store the results
		res = pd.DataFrame()

		# Starting predicting variance and price for each date in the dataframe
		for dt in df.index[100:]:
			
			#Obtaining additional predictions for start_date, using only data prior to start_date
			data = df[df.index<dt]
			r = pt.execute('dp', data)
			pr = r.predict()

			# The data for the last observation in the subsample
			d = data.iloc[-1]

			#selecting the data to be stored in the new dataframe
			new_row = pd.DataFrame([{
					'Date':d['date'], 
				  	'Implicit Volatility':d['VolatilityForValuation'], 
					'Predicted variance': pred_var, 
					'Fitted variance': pr.loc[(1,dt-1), 'Fitted variance'],
					'OptionPrice':d['Settlement'],
					}])
			
			#Adding the new row to the dataframe
			res = pd.concat([res, new_row], axis=0)
			
			#preparing the prediction for the next date
			pred_var = pr.loc[(1,dt), 'Predicted variance']

			#Saving the dataframe to a pickle file for easier access later
			res.to_pickle(f'{FLDR}/output/deriv_pred.dmp')


			print(f'Adding row {dt} of {df.index[-1]}')	

	# Plotting the observed variance ("Fitted variance") with the predicted variance and the option price
	f1 = res.plot.scatter('Predicted variance', 'Fitted variance').get_figure()
	f2 = res.plot.scatter('Predicted variance', 'OptionPrice').get_figure()	
	f1.show()
	f2.show()

	f1.savefig(f'{FLDR}/figures/volatility.png')
	f2.savefig(f'{FLDR}/figures/settlement.png')

	# Running OLS regression on the data to see if there is any
	# relationship between the predicted variance and the fitted variance
	# and the option price
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