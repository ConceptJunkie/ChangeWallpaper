import argparse
import os.path
import PIL.Image as PIL
import random
import sys

if sys.platform == 'win32':
    import pythoncom
    import shutil

    from win32com.shell import shell, shellcon
elif sys.platform == 'darwin':
    import appscript

screen_width = 3840
screen_height = 2160

screen_aspect = screen_width / screen_height

PROGRAM_NAME = "ChangeWallpaper"
VERSION = "1.2.0"
COPYRIGHT_MESSAGE = "copyright (c) 2020 (2013), Rick Gutleber"

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
target2 = os.path.join( sysDir, 'wallpaper2' + os.path.splitext( newWallpaper )[ 1 ] )

image = PIL.open( newWallpaper )

image_width, image_height = image.size
image_aspect = image_width / image_height

if ( image_aspect > screen_aspect ):
    scaling = screen_width / image_width
else:
    scaling = screen_height / image_height

# we don't want to scale too much or it just looks awful
if scaling > 2.0:
    scaling = 2.0

print( image_width, image_height, scaling )

resized_image = image.resize( ( int( image_width * scaling ), int( image_height * scaling ) ),
                              PIL.BICUBIC if scaling > 2.0 else PIL.ANTIALIAS )

useTarget2 = False

if sys.platform == 'darwin':
    if os.path.isfile( target ):
        useTarget2 = True
        os.remove( target )
        resized_image.save( target2 )
    else:
        os.remove( target2 )
        resized_image.save( target )
else:
    resized_image.save( target )

with open( os.path.join( sysDir, 'wallpaper.log' ), 'a' ) as logfile:
    logfile.write( wallpaper )

if sys.platform == 'win32':
    # Windows juju to change the wallpaper
    iAD = pythoncom.CoCreateInstance( shell.CLSID_ActiveDesktop, None,
                                      pythoncom.CLSCTX_INPROC_SERVER, shell.IID_IActiveDesktop )
    iAD.SetWallpaper( target, 0 )
    iAD.ApplyChanges( shellcon.AD_APPLY_ALL )
elif sys.platform == 'darwin':
    # OSX juju to change the wallpaper (including swapping between different file names
    # so you don't have to restart Dock)
    systemEvents = appscript.app( 'System Events' )
    desktops = systemEvents.desktops.display_name.get( )

    for desktop in desktops:
        desk = systemEvents.desktops[ appscript.its.display_name == desktop ]
        desk.picture.set( appscript.mactypes.File( target2 if useTarget2 else target ) )


