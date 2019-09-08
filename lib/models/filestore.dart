import 'dart:io';
import 'dart:convert';
import 'package:intouch/models/models.dart';
import 'package:path_provider/path_provider.dart';

Future<File> storedCredentialFile() => storedFile("credential.json");
Future<File> storedUserFile() => storedFile("user.json");

Future<String> _appPath() async {
  return (await getApplicationDocumentsDirectory()).path;
}

Future<File> storedFile(String name) async {
  var path = (await _appPath()) + "/" + name;
  var f = File(path);
  if (!(await f.exists())) {
    await f.create();
  }
  return f;
}

getStoredCredential() async {
  var credFile = await storedCredentialFile();
  var contents = await credFile.readAsString();
  if (contents == "") {
    return null;
  }
  return json.decode(contents);
}

getStoredUser() async {
  var credFile = await storedUserFile();
  var contents = await credFile.readAsString();
  if (contents == "") {
    return null;
  }
  return json.decode(contents);
}

void deleteStoredCredential() async {
  var credFile = await storedCredentialFile();
  await credFile.delete();
}

void deleteStoredUser() async {
  var credFile = await storedUserFile();
  await credFile.delete();
}

void setStoredCredential(AuthCodeObject cred) async {
  var credFile = await storedCredentialFile();
  await credFile.writeAsString(cred.jsonString());
}

void setStoredUser(UserObject cred) async {
  var credFile = await storedUserFile();
  await credFile.writeAsString(cred.jsonString());
}
