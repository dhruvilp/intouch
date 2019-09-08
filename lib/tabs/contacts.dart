import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:font_awesome_flutter/font_awesome_flutter.dart';
import '../colors.dart';
import 'package:random_color/random_color.dart';

class Contacts extends StatefulWidget {
  @override
  ContactsState createState() => ContactsState();
}

class ContactsState extends State<Contacts> {
  List data;
  bool isExpanded = false;
  RandomColor _randomColor = RandomColor();

  @override
  Widget build(BuildContext context) {
    return Container(
      color: white,
      child: Center(
        child: FutureBuilder(
          future: DefaultAssetBundle
              .of(context)
              .loadString("db/contacts.json"),
          builder: (context, snapshot) {
            // Decode the JSON
            var newData = json.decode(snapshot.data.toString());

            return ListView.builder(
              // Build the ListView
              itemBuilder: (BuildContext context, int index) {
                return Card(
                  elevation: 2.0,
                  margin: EdgeInsets.symmetric(horizontal: 10, vertical: 8.0),
                  child: ClipRRect(
                    borderRadius: BorderRadius.circular(15.0),
                    child: Container(
                      child: Column(
                        children: <Widget>[
                          ListTile(
                            leading: Icon(FontAwesomeIcons.userAlt, color: _randomColor.randomColor(),),
                            title: Text(newData[index]['name'],
                              style: TextStyle(fontSize: 18.0, fontWeight: FontWeight.w500),),
                          ),
                          SizedBox(height: 20.0,),
                        ],
                      ),
                    ),
                  ),
                );
              },
              itemCount: newData == null ? 0 : newData.length,
            );
          },
        ),
      ),
    );
  }
}
