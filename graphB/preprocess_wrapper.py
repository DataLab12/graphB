from preprocess_general import preprocess_locally, submit_preprocess_LEAP_job

def submit_preprocess_job(config_obj):
	preprocess_jobID  = preprocess_locally(config_obj)
	return preprocess_jobID
