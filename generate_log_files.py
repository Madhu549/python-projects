
# to generate temperory files for completed and failed artifacts for global variables
import sys,traceback

def generate_log_files(log_file_path,for_deployment,devops_shared_path,release_name):

    # read logs from log file
    with open(log_file_path,'r') as f:
        logs = f.readlines()
    
    # prepare completed and failed log data
    completd_artifacts = ''
    failed_artifacts = ''
    
    # prepare completed & failed artifacts
    for log in logs :
        log = log.split("    ")
        if( log[2].upper() == 'SUCCESS' ):
            completd_artifacts += f'{log[0]}    {log[1]}\n'
        elif( log[2].upper() == 'FAILURE' ):
            failed_artifacts += f'{log[0]}    {log[1]}\n'

    try:
        if(for_deployment.upper() == 'DEPLOY'):
            deployment_completed_path = f'{devops_shared_path}/globalVariableLogs/{release_name}_completed_deployment_acl.log'
            deployment_failed_path = f'{devops_shared_path}/globalVariableLogs/{release_name}_failed_deployment_acl.log'

            # write to deployment completed artifacts file
            with open(deployment_completed_path,'w+') as f:
                f.write(completd_artifacts)
            
            # write to deployment failed artifacts file
            with open(deployment_failed_path,'w+') as f:
                f.write(failed_artifacts)
        elif(for_deployment.upper() == 'ROLLBACK' or for_deployment.upper() == 'OVERALLROLLBACK'):
            rollback_completed_path = f'{devops_shared_path}/globalVariableLogs/{release_name}_completed_rollback_acl.log'
            rollback_failed_path = f'{devops_shared_path}/globalVariableLogs/{release_name}_failed_rollback_acl.log'

            # write to rollback completed artifacts file
            with open(rollback_completed_path,'w+') as f:
                f.write(completd_artifacts)
            
            # write to rollback failed artifacts file
            with open(rollback_failed_path,'w+') as f:
                f.write(failed_artifacts)
        else:
            return 1
        return 0
    except:
        traceback.print_exc()
        sys.stderr.write("Failed to write in log files\n")
        return 1