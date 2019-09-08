import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:font_awesome_flutter/font_awesome_flutter.dart';
import '../colors.dart';
import 'package:random_color/random_color.dart';

class Queue extends StatefulWidget {
  @override
  QueueState createState() => QueueState();
}

class QueueState extends State<Queue> {
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
            .loadString("db/users_in_queue.json"),
          builder: (context, snapshot) {
            // Decode the JSON
            var newData = json.decode(snapshot.data.toString());

            return ListView.builder(
              // Build the ListView
              itemBuilder: (BuildContext context, int index) {
                return Card(
                  elevation: 0.0,
                  color: (isExpanded == true) ? transparent : white,
                  margin: EdgeInsets.symmetric(horizontal: 10, vertical: 8.0),
                  child: ClipRRect(
                    borderRadius: BorderRadius.circular(15.0),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.stretch,
                      children: <Widget>[
                        ExpansionTile(
                          onExpansionChanged: (bool expanding) => setState(() => this.isExpanded = expanding),
                          backgroundColor: cyan_dark,
                          leading: Icon(FontAwesomeIcons.userAlt,),
                          title: Text(newData[index]['name'], style: TextStyle(fontSize: 18.0),),
                            children: <Widget>[
                              new Container(
                                child: Column(
                                  children: <Widget>[
                                    Text('Last Connected: '+newData[index]['last_met'],
                                      style: TextStyle(color: white, fontSize: 18.0, fontWeight: FontWeight.w500),),
                                    SizedBox(height: 5.0,),
                                    Text('Frequency: '+newData[index]['frequency'],
                                      style: TextStyle(color: white),),
                                    SizedBox(height: 20.0,),
                                  ],
                                ),
                              ),
                            ]
                        ),
                      ],
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
