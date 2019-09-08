import 'package:flutter/material.dart';
import 'package:font_awesome_flutter/font_awesome_flutter.dart';
import 'package:intouch/constant.dart';
import 'package:intouch/login_auth/linked_in_auth_code.dart';
import 'package:intouch/login_auth/linked_in_auth_response_wrapper.dart';
import 'package:intouch/main.dart';
import 'package:intouch/models/loading_indicator.dart';
import 'package:intouch/models/models.dart';
import 'package:intouch/models/filestore.dart';

import '../colors.dart';

// @TODO IMPORTANT - you need to change variable values below
// You need to add your own data from LinkedIn application
// From: https://www.linkedin.com/developers/
// Please read step 1 from this link https://developer.linkedin.com/docs/oauth2

class Login extends StatefulWidget {
  // This widget is the root of your application.
  @override
  LoginState createState() => LoginState();
}

class LoginState extends State<Login> {

  static var credStr = '';

  @override
  initState() {
    // if we have a stored credential then login with that
    super.initState();
    getStoredCredential().then((cred) {
      credStr = cred.toString();
      print("init got auth"+cred.toString());
      if (cred != null) {
//        _loginLoad(context);
        Navigator.of(context).pushAndRemoveUntil(
            new MaterialPageRoute( builder: (BuildContext context) => HomePage()), ModalRoute.withName('/main'));
      }
    });
  }

  _loginLoad(context) {
    showDialog(
        barrierDismissible: false,
        context: context,
        builder: (BuildContext context, {barrierDismissible: false}){
          return new AlertDialog(backgroundColor: Colors.transparent, elevation: 0.0,
            title: Center(
              child: Column(
                children: <Widget>[
                  new LoadingIndicator(),
                  new Text('Loading...'),
                ],
              ),
            ),
          );
        }
    );
  }

  @override
  Widget build(BuildContext context) => Scaffold(
    backgroundColor: white,
    body: LinkedInLogIn(),
  );

}

class LinkedInLogIn extends StatefulWidget {
  @override
  State createState() => LinkedInLogInState();
}

class LinkedInLogInState extends State<LinkedInLogIn> {
  static UserObject user;
  static bool logoutUser = false;
  static AuthCodeObject authorizationCode;

  @override
  Widget build(BuildContext context) {
    return Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.start,
        crossAxisAlignment: CrossAxisAlignment.center,
        mainAxisSize: MainAxisSize.max,
        children: <Widget>[
          SizedBox(height: 30.0,),
          Image.asset('assets/app_logo_large.png', width: 300.0,),
          Container(
            margin: EdgeInsets.symmetric(horizontal: 30),
            child: Text('Despite continuous networking, many people find their contacts to be superficial. \n\nInTouch helps turn distant ties into genuine connections using data analysis/optimization',
              style: TextStyle(color: cyan_dark, fontSize: 18.0, fontWeight: FontWeight.w400), textAlign: TextAlign.center, softWrap: true,),
          ),
          SizedBox(height: 50.0,),
          Container(
            margin: EdgeInsets.symmetric(horizontal: 40),
            child: RaisedButton(
              onPressed: _linkedinLogin,
              elevation: 0.0,
              color: white,
              textColor: pink,
              padding: const EdgeInsets.all(0.0),
              child: ClipRRect(
                borderRadius: BorderRadius.circular(15.0),
                child: Container(
                  width: double.infinity,
                  height: 60.0,
                  color: cyan_dark,
                  padding: const EdgeInsets.all(18.0),
                  child: Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: <Widget>[
                      Icon(FontAwesomeIcons.linkedin, color: white,),
                      SizedBox(width: 10.0,),
                      Text(
                        'Sign In With LinkedIn',
                        style: TextStyle(color: white, fontSize: 18, fontWeight: FontWeight.w500),
                        textAlign: TextAlign.center,
                      )
                    ],
                  ),
                ),
              ),
            ),
          ),
          SizedBox(height: 40.0,),
          Text('Terms & Conditions',
            style: TextStyle(decoration: TextDecoration.underline, color: cyan_dark, fontSize: 15.0,),),
          SizedBox(height: 5.0,),
          Text('2019 \u00a9 inTouch',
            style: TextStyle(color: cyan_dark, fontSize: 15.0,),)
        ]),
    );
  }
  
  void _linkedinLogin() async {
    Navigator.push(
      context,
      MaterialPageRoute(
        builder: (BuildContext context) => LinkedInAuthCodeWidget(
          destroySession: logoutUser,
          redirectUrl: redirectUrl,
          clientId: clientId,
          onGetAuthCode: (AuthorizationCodeResponse response) {

            print('auth_code: ${response.code}');
            print('state: ${response.state}');

            authorizationCode = AuthCodeObject(
              code: response.code,
              state: response.state,
              error: response.error,
            );
            setState(() {
              setStoredCredential(authorizationCode);
              logoutUser = false;
            });
            Navigator.of(context).pushAndRemoveUntil(
                new MaterialPageRoute( builder: (BuildContext context) => HomePage()), ModalRoute.withName('/main'));
          },
          catchError: (LinkedInErrorObject error) {
            print('Error description: ${error.description},'
                ' Error code: ${error.statusCode.toString()}');
            Navigator.pop(context);
          },
        ),
        fullscreenDialog: true,
      ),
    );
  }
}