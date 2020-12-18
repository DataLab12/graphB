from postprocess_general import postprocess_locally, submit_postprocess_LEAP_job

def submit_postprocess_job(config_obj, process_jobID):
	postprocess_jobID = None

	if config_obj['machine'] == 'current':
		postprocess_jobID = postprocess_locally(config_obj)
	elif config_obj['machine'] == 'LEAP':
		postprocess_jobID = submit_postprocess_LEAP_job(config_obj, process_jobID)
	else:
		print("Invalid machine type. (Options: LEAP, current)")

	print("postprocess_jobID (if None, then done locally): ", postprocess_jobID)
	return postprocess_jobID
