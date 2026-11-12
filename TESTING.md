# Pairvoy 0.5.16 — testing release

Your goals. Our journey. Pairvoy 0.5.16 completes product naming while retaining the linked-heart logo, light/dark themes, latest goal-planning functionality and compatible data migration. The official connection is labeled Pairvoy cloud; custom-server setup remains available.

## Platforms

- Windows 10/11 x64: NSIS installer, no Node/npm needed. The testing installer is not Authenticode-signed.
- Android: standalone release APK signed with the original private signing identity. Install only the APK and checksum supplied in the verified release.
- Apple releases are outside the initial scope.

## Before upgrading

Keep a backup of your data. The internal app IDs, original Android signing identity and existing desktop data location remain stable for upgrade compatibility. Do not delete old application data just to change the name. New Pairvoy storage keys import legacy settings, cached workspaces and sessions; signing out clears both session-key names.

## Verify a Windows download

```powershell
Set-Location -LiteralPath "$env:USERPROFILE\Downloads"
Get-FileHash -Algorithm SHA256 -LiteralPath '.\Pairvoy_0.5.16_Windows_x64_Setup.exe'
```

Compare the result with the accompanying .sha256 file before opening the installer. Follow Windows security prompts according to your own or your organization's policy. Launch Pairvoy from the Start menu after setup. Choose a local workspace to review the app without an account. Shared-account features require the hosted API.

## Verify an Android download

Compare the APK's SHA256 value to the published .sha256 file. Android may require permission to install a downloaded APK; follow your device or organization policy. Updating the prior app requires the same signing identity, which is retained by this release.

## Verification status

Windows and Android packages were built from private source commit d040d9d8ff95ba327e207813e45fb1cd67aaa7a2. Windows acceptance used the later diagnostics commit cbb85fa132af24a9795a8c8c51ebddf2509292b0 without changing application behavior. The compatible hosted API currently reports Pairvoy 0.5.15.

Native package, installation, emulator, renderer and hosted-API results must be recorded from the matching release files. A JavaScript export is not native-build evidence. Review the release evidence before testing real data. Physical-device UAT, password-recovery email delivery and operational backup/restore remain separate acceptance activities.

Source validation passed TypeScript, release consistency and 71 unit/API tests, with 0 failures and 1 local PostgreSQL fixture skipped. Separate PostgreSQL integration and backend-container checks passed. Windows native packaging, actual installation, API access, clipboard use and Pairvoy cloud/custom-server controls passed. Android signature, package metadata and emulator installation/launch checks passed. The root dependency audit reported 11 findings (1 low, 7 moderate, 3 high); the rebrand does not claim those issues are fixed.

[Project and download status](https://ornbaumkeith.github.io/projects/pairvoy/index.html)
