from process_general import process_locally, submit_process_LEAP_job

def submit_process_job(config_obj, preprocess_jobID):
	process_jobID = None

	if config_obj['machine'] == 'current':
		process_jobID = process_locally(config_obj)
	elif config_obj['machine'] == 'LEAP':
		process_jobID = submit_process_LEAP_job(config_obj, preprocess_jobID)
	else:
		print("Invalid machine type. (Options: LEAP, current)")

	print("process_jobID (if 0, then done locally): ", process_jobID)
	return process_jobID
