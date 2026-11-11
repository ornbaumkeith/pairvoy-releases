# Pairvoy 0.5.15 — testing release

Your goals. Our journey. Pairvoy continues the latest 0.5.14 functionality with a new name, linked-heart branding, charcoal/white themes and migration of saved local settings and cached workspaces.

## Platforms

- Windows 10/11 x64: NSIS installer, no Node/npm needed. The testing installer is not Authenticode-signed.
- Android: standalone release APK signed with the original private signing identity. Install only the APK and checksum supplied in the verified release.
- Apple releases are outside the initial scope.

## Before upgrading

Keep a backup of your data. The internal app IDs, original Android signing identity and existing desktop data location remain stable for upgrade compatibility. Do not delete old application data just to change the name. New Pairvoy storage keys import legacy settings, cached workspaces and sessions; signing out clears both session-key names.

## Verify a Windows download

```powershell
Set-Location -LiteralPath "$env:USERPROFILE\Downloads"
Get-FileHash -Algorithm SHA256 -LiteralPath '.\Pairvoy_0.5.15_Windows_x64_Setup.exe'
```

Compare the result with the accompanying .sha256 file before opening the installer. Follow Windows security prompts according to your own or your organization's policy. Launch Pairvoy from the Start menu after setup. Choose a local workspace to review the app without an account. Shared-account features require the hosted API.

## Verify an Android download

Compare the APK's SHA256 value to the published .sha256 file. Android may require permission to install a downloaded APK; follow your device or organization policy. Updating the prior app requires the same signing identity, which is retained by this release.

## Verification status

Native package, installation, emulator, renderer and hosted-API results must be recorded from the matching release files. A JavaScript export is not native-build evidence. Review the release evidence before testing real data. Physical-device UAT, password-recovery email delivery and operational backup/restore remain separate acceptance activities.

The source rebrand passed TypeScript, release consistency, local unit/API regressions, web and Android JavaScript exports. PostgreSQL and backend container checks passed in GitHub Actions. The root dependency audit reported 11 findings (1 low, 7 moderate, 3 high); the rebrand does not claim those issues are fixed.

[Project and download status](https://ornbaumkeith.github.io/projects/pairvoy/index.html)
