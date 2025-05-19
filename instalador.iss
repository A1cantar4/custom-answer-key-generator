; instalador.iss - Instala o Gerador de Gabaritos Personalizados

[Setup]
AppName=Gerador de Gabaritos Personalizados
AppVersion=1.8.0
DefaultDirName={autopf}\GabaritoApp
DefaultGroupName=GabaritoApp
OutputBaseFilename=GabaritoInstaller
Compression=lzma
SolidCompression=yes
DisableDirPage=no
DisableProgramGroupPage=yes
PrivilegesRequired=admin

[Files]
Source: "dist\GabaritoApp.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{commondesktop}\Gerador de Gabaritos"; Filename: "{app}\GabaritoApp.exe"
Name: "{group}\Gerador de Gabaritos"; Filename: "{app}\GabaritoApp.exe"

[Run]
Filename: "{app}\GabaritoApp.exe"; Description: "Executar agora"; Flags: nowait postinstall skipifsilent