from process_general import process_locally, submit_process_LEAP_job

def submit_process_job(config_obj, preprocess_jobID):
	process_jobID = process_locally(config_obj)

	return process_jobID
