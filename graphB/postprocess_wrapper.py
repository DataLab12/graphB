from postprocess_general import postprocess_locally, submit_postprocess_LEAP_job

def submit_postprocess_job(config_obj, process_jobID):

	postprocess_jobID = postprocess_locally(config_obj)
    
	return postprocess_jobID
