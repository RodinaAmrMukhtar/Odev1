#define MyAppName "Block Dodger"
#define MyAppVersion "1.0"
#define MyAppPublisher "Rodina"
#define MyAppExeName "BlockDodger.exe"

[Setup]
AppId={{4B3AA9D6-91AA-4B89-8F4E-7E2C44D77A11}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
OutputDir=Output
OutputBaseFilename=BlockDodgerSetup
Compression=lzma
SolidCompression=yes
PrivilegesRequired=admin

[Files]
Source: "dist\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "Launch {#MyAppName}"; Flags: nowait postinstall skipifsilent

[Registry]
Root: HKLM; Subkey: "Software\Rodina\BlockDodger"; ValueType: string; ValueName: "InstalledBefore"; ValueData: "1"
Root: HKLM; Subkey: "Software\Rodina\BlockDodger"; ValueType: string; ValueName: "InstallPath"; ValueData: "{app}"

[Code]
function InitializeSetup(): Boolean;
begin
  if RegValueExists(HKEY_LOCAL_MACHINE, 'Software\Rodina\BlockDodger', 'InstalledBefore') then
  begin
    MsgBox(
      'This game was already installed on this PC before. Reinstall is blocked.',
      mbError, MB_OK
    );
    Result := False;
  end
  else
  begin
    Result := True;
  end;
end;