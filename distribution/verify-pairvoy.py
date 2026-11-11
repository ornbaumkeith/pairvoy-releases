"""Verify an allowlisted Pairvoy release; private source/signing material is never accepted."""
import hashlib,json,pathlib,urllib.request,urllib.parse,zipfile,stat
root=pathlib.Path(__file__).resolve().parent.parent
manifest=json.loads((root/'distribution/pairvoy-0.5.15.json').read_text())
assert manifest['version']=='0.5.15' and manifest['tag']=='pairvoy-v0.5.15'
assert set(manifest['platforms'])<= {'windows','android'} and manifest['platforms']
if manifest['publish']:assert set(manifest['platforms'])=={'windows','android'}
out=root/'public-assets';out.mkdir()
allowed={
 'windows':{'Pairvoy_0.5.15_Windows_x64_Setup.exe','Pairvoy_0.5.15_Windows_x64_Setup.exe.sha256','windows-smoke.json'},
 'android':{'Pairvoy_0.5.15_Android.apk','Pairvoy_0.5.15_Android.apk.sha256','android-signature.txt','android-package.txt','android-permissions.txt','android-launch.txt','android-runtime-errors.txt','android-ui.xml'},
}
for platform,item in manifest['platforms'].items():
 url=urllib.parse.urlsplit(item['url']);assert url.scheme=='https' and url.hostname.endswith('.oaiusercontent.com')
 archive=root/(platform+'.zip')
 with urllib.request.urlopen(item['url'],timeout=120) as response,archive.open('wb') as dest:
  total=0
  while chunk:=response.read(1024*1024):
   total+=len(chunk);assert total<400_000_000;dest.write(chunk)
 assert hashlib.sha256(archive.read_bytes()).hexdigest()==item['archive_sha256']
 with zipfile.ZipFile(archive) as z:
  names=z.namelist();assert len(names)==len(set(names))
  assert all('/' not in n and '\\' not in n and n not in ('.','..') for n in names)
  assert all(not stat.S_ISLNK(x.external_attr>>16) for x in z.infolist())
  for name,expected in item['files'].items():
   assert name in names and name in allowed[platform]
   data=z.read(name);assert hashlib.sha256(data).hexdigest()==expected
   (out/name).write_bytes(data)
for platform in manifest['platforms']:
 name='Pairvoy_0.5.15_Windows_x64_Setup.exe' if platform=='windows' else 'Pairvoy_0.5.15_Android.apk'
 data=(out/name).read_bytes();expected=(out/(name+'.sha256')).read_text(encoding='utf-8-sig').split()[0]
 assert hashlib.sha256(data).hexdigest()==expected
 if platform=='windows':
  assert data[:2]==b'MZ';smoke=json.loads((out/'windows-smoke.json').read_text())
  assert smoke['ok'] and not smoke['hasNode'] and smoke['title']=='Pairvoy' and smoke['version']=='0.5.15'
 else:
  with zipfile.ZipFile(out/name) as apk:assert 'AndroidManifest.xml' in apk.namelist()
  assert "name='com.tandem.goals' versionCode='515' versionName='0.5.15'" in (out/'android-package.txt').read_text()
  assert 'application-debuggable' not in (out/'android-package.txt').read_text()
  assert 'Verified' in (out/'android-signature.txt').read_text()
  if manifest['publish']:
   assert 'Sign in' in (out/'android-ui.xml').read_text()
   assert 'com.tandem.goals' in (out/'android-launch.txt').read_text()
  errors=(out/'android-runtime-errors.txt').read_text() if (out/'android-runtime-errors.txt').exists() else ''
  assert not any(s in errors for s in ['FATAL EXCEPTION','TypeError:','ReferenceError:','Error:'])
  for permission in ['CAMERA','RECORD_AUDIO','READ_EXTERNAL_STORAGE','WRITE_EXTERNAL_STORAGE','READ_MEDIA_IMAGES','READ_MEDIA_VIDEO','SYSTEM_ALERT_WINDOW']:
   assert 'android.permission.'+permission not in (out/'android-permissions.txt').read_text()
if manifest['publish']:
 installed=json.loads((root/'evidence/pairvoy-windows-installation.json').read_text())
 renderer=json.loads((root/'evidence/pairvoy-windows-renderer.json').read_text())
 assert installed['ok'] and installed['version']=='0.5.15' and installed['installerExitCode']==0 and installed['installedFromNsis']
 assert renderer['api']['ok'] and renderer['clipboard']['result']=='passed' and not renderer['hasNode']
for name in ['pairvoy-windows-installation.json','pairvoy-windows-renderer.json','pairvoy-release-status.json']:
 p=root/'evidence'/name
 if p.exists():(out/name).write_bytes(p.read_bytes())
(out/'LICENSE.txt').write_bytes((root/'LICENSE').read_bytes())
(out/'TESTING.md').write_bytes((root/'TESTING.md').read_bytes())
(out/'SHA256SUMS.txt').write_text(''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.name+'\n' for p in sorted(out.iterdir())))
print('Verified allowlisted Pairvoy artifacts; publish='+str(manifest['publish']))
