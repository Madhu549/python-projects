import shutil, traceback
try:
    shutil.copy2('C:\\Users\MADHU\Desktop\\acldeploymentstatus.log', 'C:\\Users\\MADHU\Desktop\\test_folder\madhu')
    print('Completed with moving the file to the destination')
except:
    print('error while copying the file from source to destination')
    traceback.print_exc()