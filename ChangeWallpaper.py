import argparse
import pythoncom
import shutil
from win32com.shell import shell, shellcon
import random
import os.path
import PIL.Image as PIL

screen_width = 1920
screen_height = 1080

screen_aspect = screen_width / screen_height

PROGRAM_NAME = "ChangeWallaper"
VERSION = "1.1"
COPYRIGHT_MESSAGE = "copyright (c) 2013, Rick Gutleber"

parser = argparse.ArgumentParser( prog=PROGRAM_NAME, description=PROGRAM_NAME + ' - ' + VERSION +
                                  ' - ' + COPYRIGHT_MESSAGE )

parser.add_argument( '-v', '--version', action='version', version='%(prog)s ' + VERSION )
parser.add_argument( 'filename', nargs='?', default='' )

args = parser.parse_args( )

newWallpaper = args.filename

wallpaperDir = os.environ[ 'WALLPAPER_DIR' ]
sysDir = os.environ[ 'SYS_DIR' ]

if newWallpaper == '':
    wallpaper = random.choice( list( open( os.path.join( wallpaperDir, 'wallpaper.idx' ) ) ) )
    newWallpaper = os.path.join( wallpaperDir, wallpaper[ : -1 ] )  # eat the trailing newline

print( newWallpaper )

target = os.path.join( sysDir, 'wallpaper' + os.path.splitext( newWallpaper )[ 1 ] )

image = PIL.open( newWallpaper )

image_width, image_height = image.size
image_aspect = image_width / image_height

if ( image_aspect > screen_aspect ):
    scaling = screen_width / image_width
else:
    scaling = screen_height / image_height

print( image_width, image_height, scaling )

# we don't want to scale too much or it just looks awful
if scaling > 2.0:
    scaling = 2.0

resized_image = image.resize( ( int( image_width * scaling ), int( image_height * scaling ) ),
                              PIL.BICUBIC if scaling > 2.0 else PIL.ANTIALIAS )

resized_image.save( target )

with open( os.path.join( sysDir, 'wallpaper.log' ), 'a' ) as logfile:
    logfile.write( wallpaper )

# Windows juju to change the wallpaper
iAD = pythoncom.CoCreateInstance( shell.CLSID_ActiveDesktop, None,
                                  pythoncom.CLSCTX_INPROC_SERVER, shell.IID_IActiveDesktop )
iAD.SetWallpaper( target, 0 )
iAD.ApplyChanges( shellcon.AD_APPLY_ALL )

