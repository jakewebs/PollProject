import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('raw-polls.csv')


#This statement removes national, congressional district, and non-state polls (ex. Puerto Rico)
state_filter = (df['location'] != 'US') & (df['location'] != 'M2') & (df['location'] != 'M1') & (df['location'] != 'PR') & (df['location'] != 'N2') & (df['location'].str.len()==2)
only_states = df[state_filter]


#Makes a dictionary with states as keys and two lists as values: All the errors and biases for each state's polls
state_values = {}
for index,poll in only_states.iterrows():
	
	if poll['location'] not in state_values:
		state_values[poll['location']] = [ [], [] ]

	state_values[poll['location']][0].append(poll['error'])

	#Some polls did not have a bias. Removes those.
	if pd.isnull(poll['bias']) == False:
		state_values[poll['location']][1].append(poll['bias'])


#Calculates the errors and biases per state and adds to a dictionary
final_results = {}
for state in state_values:
	mean_error = sum(state_values[state][0])/len(state_values[state][0])
	mean_bias = sum(state_values[state][1])/len(state_values[state][1])
	final_results[state] = [mean_error, mean_bias]

#print(final_results)

#Looking at specific regions to see if error and bias changes based off of this. Regions based off of the US Census Bureau's definitions.
midwest = {'ND':final_results['ND'], 'SD':final_results['SD'], 'NE':final_results['NE'], 'KS':final_results['KS'], 'MN':final_results['MN'], 'IA':final_results['IA'],
		   'MO':final_results['MO'], 'WI':final_results['WI'], 'IL':final_results['IL'], 'MI':final_results['MI'], 'IN':final_results['IN'], 'OH':final_results['OH']}
west = {'AK':final_results['AK'], 'HI':final_results['HI'], 'WA':final_results['WA'], 'OR':final_results['OR'], 'CA':final_results['CA'], 'NV':final_results['NV'],
		'ID':final_results['ID'], 'UT':final_results['UT'], 'AZ':final_results['AZ'], 'MT':final_results['MT'], 'WY':final_results['WY'], 'CO':final_results['CO'],
		'NM':final_results['NM']}
south = {'OK':final_results['OK'], 'TX':final_results['TX'], 'AR':final_results['AR'], 'LA':final_results['LA'], 'KY':final_results['KY'], 'TN':final_results['TN'],
		 'MS':final_results['MS'], 'AL':final_results['AL'], 'GA':final_results['GA'], 'FL':final_results['FL'], 'SC':final_results['SC'], 'NC':final_results['NC'], 
		 'VA':final_results['VA'], 'WV':final_results['WV'], 'DC':final_results['DC'], 'MD':final_results['MD'], 'DE':final_results['DE']}
northeast = {'PA':final_results['PA'], 'NJ':final_results['NJ'], 'NY':final_results['NY'], 'CT':final_results['CT'], 'RI':final_results['RI'], 'MA':final_results['MA'],
			 'VT':final_results['VT'], 'NH':final_results['NH'], 'ME':final_results['ME']}
#Positive bias: dem bias. Negative bias: republican bias. Error: avg amount off

#Figure 1: Scatterplot of states by region. 
cum_error, cum_bias = 0, 0
fig = plt.figure(figsize = (10,8))
ax = fig.add_subplot(111)
ax.set_ylabel('Average Bias')
ax.set_xlabel('Average Error')
ax.set_title('Bias and Error in State Polls, 1998-present (By Region)')

for point in final_results:
   x = final_results[point][0]
   y = final_results[point][1]
   if point in midwest:
      plt.scatter(x,y, c = 'green', alpha = 0.7, s = 30)
      plt.annotate(point, (x,y), textcoords = "offset points", xytext = (0,5), ha = 'center',alpha=0.4)	
   elif point in west:
      plt.scatter(x,y, c = 'magenta', alpha = 0.7, s = 30)
      plt.annotate(point, (x,y), textcoords = "offset points", xytext = (0,5), ha = 'center',alpha=0.4)
   elif point in south:
      plt.scatter(x,y, c = 'cyan', alpha = 0.7, s = 30)
      plt.annotate(point, (x,y), textcoords = "offset points", xytext = (0,5), ha = 'center',alpha=0.4)
   else:
   	  plt.scatter(x,y, c = 'yellow', alpha = 0.7, s = 30)
   	  plt.annotate(point, (x,y), textcoords = "offset points", xytext = (0,5), ha = 'center',alpha=0.4)
   cum_error, cum_bias = cum_error + x, cum_bias + y

print('Total average error: ' + str(cum_error/51)) #Avg poll is off by about 6.25 % pts
print('Total average bias: ' + str(cum_bias/51)) #Avg poll is about 0.5 % pts skewed Democratic- not a huge bias
plt.show()


#Competitive categories made using Cook PVI. PVI <= 5: Competitive. 5 < PVI < 10: Semi-Competitive. PVI >= 10: Not competitive
competitive = {'OR':final_results['OR'], 'ME':final_results['ME'], 'NM':final_results['NM'], 'CO':final_results['CO'], 'MI':final_results['MI'], 'MN':final_results['MN'],
			   'NV':final_results['NV'], 'NH':final_results['NH'], 'VA':final_results['VA'], 'PA':final_results['PA'], 'WI':final_results['WI'], 'FL':final_results['FL'],
			   'IA':final_results['IA'], 'NC':final_results['NC'], 'OH':final_results['OH'], 'AZ':final_results['AZ'], 'GA':final_results['GA']}
semi_competitive = {'IL':final_results['IL'], 'NJ':final_results['NJ'], 'WA':final_results['WA'], 'CT':final_results['CT'],'DE':final_results['DE'], 'SC':final_results['SC'],
					'TX':final_results['TX'], 'AK':final_results['AK'], 'IN':final_results['IN'], 'MS':final_results['MS'], 'MO':final_results['MO']}
not_competitive = {'HI':final_results['HI'], 'VT':final_results['VT'], 'CA':final_results['CA'], 'MD':final_results['MD'], 'MA':final_results['MA'], 'NY':final_results['NY'],
				   'RI':final_results['RI'], 'LA':final_results['LA'], 'MT':final_results['MT'], 'KS':final_results['KS'], 'AL':final_results['AL'], 'NE':final_results['NE'],
				   'SD':final_results['SD'], 'TN':final_results['TN'], 'AR':final_results['AR'], 'KY':final_results['KY'], 'ND':final_results['ND'], 'ID':final_results['ID'],
				   'WV':final_results['WV'], 'OK':final_results['OK'], 'UT':final_results['UT'], 'WY':final_results['WY']}

#Figure 2: Scatterplot of states by competitiveness. 
fig = plt.figure(figsize = (10,8))
ax = fig.add_subplot(111)
ax.set_ylabel('Average Bias')
ax.set_xlabel('Average Error')
ax.set_title('Bias and Error in State Polls, 1998-present (By PVI)')

for point in final_results:
   x = final_results[point][0]
   y = final_results[point][1]
   if point in competitive:
      plt.scatter(x,y, c = 'green', alpha = 0.7, s = 30)
      plt.annotate(point, (x,y), textcoords = "offset points", xytext = (0,5), ha = 'center',alpha=0.4)
   elif point in semi_competitive:
      plt.scatter(x,y, c = 'magenta', alpha = 0.7, s = 30)
      plt.annotate(point, (x,y), textcoords = "offset points", xytext = (0,5), ha = 'center',alpha=0.4)
   elif point in not_competitive:
      plt.scatter(x,y, c = 'cyan', alpha = 0.7, s = 30)
      plt.annotate(point, (x,y), textcoords = "offset points", xytext = (0,5), ha = 'center',alpha=0.4)

plt.show()
