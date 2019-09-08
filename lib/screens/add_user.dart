import 'package:intouch/main.dart';
import 'package:flutter/material.dart';
import 'package:intouch/colors.dart';
import 'package:flutter/services.dart';

class AddUser extends StatefulWidget {
  @override
  _AddUserState createState() => _AddUserState();
}

class _AddUserState extends State<AddUser> {

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Add User'),),
      body: SingleChildScrollView(
      padding: const EdgeInsets.symmetric(horizontal: 16.0),
      child: Column(
        mainAxisAlignment: MainAxisAlignment.spaceEvenly,
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: <Widget>[
          Center(
            child: Padding(
              padding: const EdgeInsets.only(top: 10.0),
              child: Text('Add User', style: TextStyle(fontSize: 20, fontWeight: FontWeight.w500, color: cyan_dark),textAlign: TextAlign.center,),
            ),
          ),
          SizedBox(height: 15.0),
          TextFormField(
            keyboardType: TextInputType.text,
            decoration: const InputDecoration(
                border: OutlineInputBorder(),
                labelText: 'Name',),
            maxLines: 2,
          ),
          SizedBox(height: 24.0),
          TextFormField(
            keyboardType: TextInputType.text,
            decoration: const InputDecoration(
              border: OutlineInputBorder(),
              labelText: 'How often do you want to meet',),
            maxLines: 2,
          ),
          SizedBox(height: 24.0),
          TextFormField(
            keyboardType: TextInputType.datetime,
            decoration: const InputDecoration(
            border: OutlineInputBorder(),
            labelText: 'When did you last time meet',),
            maxLines: 1,
          ),
          SizedBox(height: 24.0),
          Center(child: new OutlineButton(
              onPressed: (){
                Navigator.of(context).pushAndRemoveUntil(new MaterialPageRoute( builder: (BuildContext context) => HomePage()), ModalRoute.withName('/main'));
              },
              child: new Text('Save',
                style: TextStyle(fontSize: 20, color: cyan_dark),)
          ),
          ),
          SizedBox(height: 24.0),
        ],
      ),
    ),
    );
  }
}