rem This is a TCC script, ".w" is an alias for whereis (see the whereis project, https://github.com/ConceptJunkie/whereis/)
.w *.jpg %WALLPAPER_DIR% /r /i *.png *.bmp *.gif > %WALLPAPER_DIR%\wallpaper2.txt
move %WALLPAPER_DIR\wallpaper2.txt %WALLPAPER_DIR%\wallpaper.idx >& NUL
wc -l %WALLPAPER_DIR%\wallpaper.idx
