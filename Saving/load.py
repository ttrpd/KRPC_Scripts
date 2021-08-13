import krpc
import os
import shutil
import argparse

parser = argparse.ArgumentParser(
    description='Loads saves from a git repository containing kerbal space program saves'
)
parser.add_argument(
    '-p','--pull-before',
    help='Pulls the latest save from the git repo before loading',
    required=False,
    action='store_true'
)
parser.add_argument(
    '--repo-location',
    help='Copies saves from the given repo location',
    required=False,
    default= os.path.join(os.environ["USERPROFILE"], "KSP_saves")
)
parser.add_argument(
    '--game-location',
    help='Uses the given game saves directory insead of the default',
    required=False,
    default= os.path.join(os.environ["USERPROFILE"], "Kerbal Space Program", "saves")
)
parser.add_argument(
    '--game-name',
    help='Uses the given game name',
    required=True,
    default= 'KRPC'
)
args = vars(parser.parse_args())

if args['pull_before']:
    os.chdir(args['repo_location'])
    os.system("git pull")

# build repo saves location
original_location = os.path.join(args['repo_location'], args['game_name']+'_saves')
# build game saves location
new_location = os.path.join(args['game_location'], args['game_name'])

if not os.path.exists(original_location):
    raise ValueError("Origional save location doesn't exist")
if not os.path.exists(os.path.join(original_location, args['game_name']+"_save.sfs")):
    raise ValueError("The save file being loaded doesn't exist")

# copy save from repo's save folder to game's save folder'
shutil.copy(
    os.path.join(original_location, args['game_name']+'_save.sfs'),
    os.path.join(new_location, args['game_name']+'_save.sfs')
)

# load save
conn = krpc.connect("loading_"+args['game_name']+"_save")
conn.space_center.load(args['game_name']+"_save")
conn.close()