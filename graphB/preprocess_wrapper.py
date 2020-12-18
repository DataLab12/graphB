from preprocess_general import preprocess_locally, submit_preprocess_LEAP_job

def submit_preprocess_job(config_obj):
	preprocess_jobID = None

	if config_obj['machine'] == 'current':
		preprocess_jobID = preprocess_locally(config_obj)
	elif config_obj['machine'] == 'LEAP':
		preprocess_jobID = submit_preprocess_LEAP_job(config_obj)
	else:
		print("Invalid machine type. (Options: LEAP, current)")

	print("preprocess_jobID (if 0, then done locally): ", preprocess_jobID)
	print("----------")
	print()
	return preprocess_jobID
