import os
head = """

<html>
  <head>
    <title>INSAgag</title>
    <link href='https://fonts.googleapis.com/css?family=Open+Sans:400,700' rel='stylesheet' type='text/css'>
    <link href='https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css' rel='stylesheet' type='text/css'>
  </head>
  <body>

"""

foot = """
    </body>
  </html>
"""
images = []
#with open("index.html", 'w') as f:
for file in os.listdir('/home/energie/Script/Imgur100/'):
  if os.path.isfile(os.path.join('/home/energie/Script/Imgur100/', file)):
    name, ext = os.path.splitext(os.path.join('/home/energie/Script/Imgur100/', file))
    if ext == ".jpg":
      images.append(file)
i = 1
for img in images:
  cont = '<div class=\"container\" style=\"text-align:center;\" id=\"post_'+str(i)+'\">\n<h2>'+img[:-4]+'</h2>\n<img style=\"width:auto;height:auto;max-width:500px;max-height:500px;\" src=\"' + img + '\"'
  i += 1
  cont += " />\n"
  cont += """<p id="like_"""+ str(i) +""""></p><p id="dislike_"""+ str(i)  +""""></p><a style=\"margin:10px;\" href="#" onclick="Like()" class="btn btn-primary">Like</a><a href="#" onclick="Dislike()" class="btn btn-danger">Dislike</a>"""
  cont += "</div>\n"

  head += cont

head += foot
with open("index.html", "w") as f:
  f.write(head)
