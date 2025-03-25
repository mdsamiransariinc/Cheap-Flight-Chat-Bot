import os

# class clutter:
#     def organize(self,type):
#         print(os.getcwd)


# s = input("What type of file do you want to organize (eg. .pdf , .png , .docs): ")
# i = clutter()
# clutter.organize(s.split("\n")[0])



i = 1
for files in os.listdir(os.getcwd()):
    if( files.endswith(".txt")):
        os.rename(files,f"{i}.txt")
    i = i + 1