import os, sys
images = []
for file in os.listdir('/root/scriptTest/meme/'):
  if os.path.isfile(os.path.join('/root/scriptTest/meme/', file)):
    name, ext = os.path.splitext(os.path.join('/root/scriptTest/meme/', file))
    if ext == ".jpg":
      images.append(file)

i = 1
for img in images:
  os.system("python post_contentMultiChain.py \""+os.path.join('/root/scriptTest/meme/', img)+"\" Post_"+str(i)+" chain1 image")
  i += 1
