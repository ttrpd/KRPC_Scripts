import krpc
import os
import shutil

save_location = os.path.join(os.environ["USERPROFILE"], "KSP_saves")
ksp_location = os.path.join(os.environ["USERPROFILE"], "Kerbal Space Program", "saves")
game_name = "KRPC"

# build repo saves location
original_location = os.path.join(save_location, game_name+'_saves')
# build game saves location
new_location = os.path.join(ksp_location, game_name)

if not os.path.exists(original_location):
    raise ValueError("Origional save location doesn't exist")
if not os.path.exists(os.path.join(original_location, game_name+"_save.sfs")):
    raise ValueError("The save file being loaded doesn't exist")

# move save from repo's save folder to game's save folder'
shutil.copy(
    os.path.join(original_location, game_name+'_save.sfs'),
    os.path.join(new_location, game_name+'_save.sfs')
)

# load save
conn = krpc.connect("loading_"+game_name+"_save")
conn.space_center.load(game_name+"_save")
conn.close()