import krpc
import os
import shutil
from datetime import datetime as dt

save_location = os.path.join(os.environ["USERPROFILE"], "KSP_saves")
ksp_location = os.path.join(os.environ["USERPROFILE"], "Kerbal Space Program", "saves")
game_name = "KRPC"

conn = krpc.connect("saving")
# build save_name
#    get today's date
now = dt.now().strftime("%m%d%y-%H-%M-%S")
#    get in-game date
ut = int(conn.space_center.ut)
# save game with save_name
save_info = now+'_'+str(ut)
conn.space_center.save(game_name+"_save")
conn.close()

# move save with save_name from game save folder to saving folder
original_location = os.path.join(ksp_location, game_name)
new_location = os.path.join(save_location, game_name+'_saves')

if not os.path.exists(original_location):
   raise ValueError("Origional save location doesn't exist")

if not os.path.exists(new_location):
    os.makedirs(new_location)

shutil.move(
    os.path.join(original_location, game_name+'_save.sfs'),
    os.path.join(new_location, game_name+'_save.sfs')
)

description = ""# TODO: implement command line argument descriptions for extra information

os.chdir(os.path.join(save_location, game_name+"_saves"))
os.system("git add "+game_name+"_save.sfs")
os.system("git commit -m \""+save_info+"#"+description+"\"")
os.system("git push")
