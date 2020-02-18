The list of folders uploaded
1. Attacksynthesizer: The gurobi files that optimise the networks to synthesize attacks.
2. network_files:
	1. These contain four types of network files which is the AP_predict, AP_high, AP_low and AP_plant
		These files contain different models for producing the same output. 
		The models want to compute an optimal schedule for insulin injection for K amount of time.
		Hence, conducting a FDI that changes the model prediction would be the attacker model in this 
		case. 
	2. The sample inputs or the seed inputs to predict the insulin in Kt time. Based on them the model is built. 	

