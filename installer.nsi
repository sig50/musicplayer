; Optional NSIS installer. Build the EXE first (python build_exe.py), then:
;   makensis installer.nsi   ->  dist\musicplayer-setup.exe
!define APP "MusicPlayer"
Name "${APP}"
OutFile "dist\musicplayer-setup.exe"
InstallDir "$PROGRAMFILES\${APP}"
RequestExecutionLevel admin
Page directory
Page instfiles
UninstPage uninstConfirm
UninstPage instfiles

Section "Install"
  SetOutPath "$INSTDIR"
  File "dist\musicplayer.exe"
  File "assets\icon.ico"
  CreateDirectory "$SMPROGRAMS\${APP}"
  CreateShortcut "$SMPROGRAMS\${APP}\${APP}.lnk" "$INSTDIR\musicplayer.exe" "" "$INSTDIR\icon.ico"
  CreateShortcut "$DESKTOP\${APP}.lnk" "$INSTDIR\musicplayer.exe" "" "$INSTDIR\icon.ico"
  WriteUninstaller "$INSTDIR\uninstall.exe"
SectionEnd

Section "Uninstall"
  Delete "$INSTDIR\musicplayer.exe"
  Delete "$INSTDIR\icon.ico"
  Delete "$INSTDIR\uninstall.exe"
  Delete "$SMPROGRAMS\${APP}\${APP}.lnk"
  RMDir "$SMPROGRAMS\${APP}"
  Delete "$DESKTOP\${APP}.lnk"
  RMDir "$INSTDIR"
SectionEnd
