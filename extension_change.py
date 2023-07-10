import os

# Selecting the list
print('Before rename:')
file = 'C:\\Users\MADHU\Desktop\python\Python_Coding\\test.xml'
print(file)

# Renaming the file
for root, dir, file_name in os.walk(file):

# construct full file path

    print('test1')
    old_file_name = os.path.join(root, file_name)

    # Change the extension from txt to pdf
    new_file_name = old_file_name.replace('.xsl', '.xml')
    os.rename(old_file_name, new_file_name)
    print('After rename:')
    print(file)