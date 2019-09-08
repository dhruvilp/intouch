import 'package:intouch/login_auth/linked_in_auth_response_wrapper.dart';

class AuthCodeObject {
  String code, state;
  LinkedInErrorObject error;

  AuthCodeObject({this.code, this.state, this.error});

  String jsonString() {
    return '{"code": "${this.code}", '
        + '"state": "${this.state}", '
        + '"error": "$this.error"}';
  }

}

class UserObject {
  String firstName, lastName, email, userId, profilePicture, token;

  UserObject({this.firstName, this.lastName, this.email, this.userId, this.profilePicture, this.token});

  String jsonString() {
    return '{"firstName": "${this.firstName}", '
        + '"lastName": "${this.lastName}", '
        + '"email": "${this.email}", '
        + '"userId": "${this.userId}", '
        + '"accessToken": "${this.token}", '
        + '"profilePicture": "${this.profilePicture}"}';
  }

}