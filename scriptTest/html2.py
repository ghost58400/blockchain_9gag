import os,sys
from Naked.toolshed.shell import muterun_js
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
    	<script src="https://cdn.rawgit.com/ethereum/web3.js/develop/dist/web3.js"></script>
	<script src="https://code.jquery.com/jquery-3.1.1.slim.min.js"></script>
	<script src="./index.js"></script>
    </body>
  </html>
"""
images = []
for file in os.listdir('/home/energie/Script/Imgur100/'):
  if os.path.isfile(os.path.join('/home/energie/Script/Imgur100/', file)):
    name, ext = os.path.splitext(os.path.join('/home/energie/Script/Imgur100/', file))
    if ext == ".jpg":
      images.append(file)
i = 1
for img in images:
  response = muterun_js('deploy.js')
  if response.exitcode == 0:
    addr = str(response.stdout[:-1])[2:-1]
    print(addr)
  else:
    print('Deploy contract error')
    sys.exit(-1)
  cont = '<div class=\"container\" style=\"text-align:center;\" id=\"post_'+str(i)+'\">\n<h2>'+img[:-4]+'</h2>\n<img id=\"'+addr+'\" style=\"width:auto;height:auto;max-width:500px;max-height:500px;\" src=\"' + img + '\"'
  cont += " />\n"
  cont += """<p><em id="like_"""+ str(i) +""""></em><em id="dislike_"""+ str(i)  +""""></em></p><a style=\"margin:10px;\" onclick="Like("""+str(i)+""")" class="btn btn-primary">Like</a><a onclick="Dislike("""+str(i)+""")" class="btn btn-danger">Dislike</a>"""
  cont += "</div>\n"
  i += 1
  head += cont

head += foot
with open("index.html", "w") as f:
  f.write(head)
