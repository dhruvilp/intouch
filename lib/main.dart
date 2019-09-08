import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:groovin_material_icons/groovin_material_icons.dart';
import 'package:intouch/colors.dart';
import 'package:intouch/screens/add_user.dart';
import 'package:intouch/screens/login.dart';
import 'package:intouch/tabs/queue.dart' as _firstTab;
import 'package:intouch/tabs/contacts.dart' as _secondTab;

import 'models/filestore.dart';

void main() => runApp(MyApp());

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'InTouch',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        primaryColor: cyan,
        accentColor: pink,
      ),
      routes: <String, WidgetBuilder> {
        '/login': (BuildContext context) => new Login(),
        '/main': (BuildContext context) => new HomePage(),
        '/adduser': (BuildContext context) => new AddUser(),
      },
      home: Login(),
    );
  }
}

class HomePage extends StatefulWidget {
  HomePage({Key key}) : super(key: key);

  @override
  _HomePageState createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> with TickerProviderStateMixin {
  BottomNavigationBarType _type = BottomNavigationBarType.shifting;
  int _tab = 0;
  var _title_app = null;
  var _title_icon = null;
  PageController _tabController;
  static var credStr = '';
  final _formKey = GlobalKey<FormState>();


  @override
  void initState() {
    super.initState();
    _tabController = new PageController();
    this._title_app = TabItems[0].title;

  }

  void onTap(int tab){
    _tabController.jumpToPage(tab);
  }

  void onTabChanged(int tab) {
    setState((){
      this._tab = tab;
    });

    switch (tab) {
      case 0:   this._title_app = TabItems[0].title; break;
      case 1:   this._title_app = TabItems[1].title; break;
    }
  }

  @override
  void dispose(){
    super.dispose();
    _tabController.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final BottomNavigationBar bottomNavBar = BottomNavigationBar(
      items: TabItems.map((TabItem) {
        return new BottomNavigationBarItem(
          backgroundColor: cyan,
          title: new Text(TabItem.title,),
          icon: new Icon(TabItem.icon, color: off_white,),
        );
      }).toList(),
      currentIndex: _tab,
      type: _type,
      onTap: onTap,
      fixedColor: off_white,
    );

    return Scaffold(
      appBar: AppBar(
        title: Image.asset('assets/app_logo_large.png',),
        backgroundColor: white,
        elevation: 0.0,
        bottom: (_tab != 1) ? PreferredSize(
          preferredSize: const Size.fromHeight(35.0),
          child: Column(
            children: <Widget>[
              Text('Let\'s Keep In Touch',
                style: TextStyle(fontSize: 18.0, color: charcoal, fontWeight: FontWeight.w500),),
              SizedBox(height: 10.0,),
            ],
          ),
        ) : null,
        actions: <Widget>[
        IconButton(icon: Icon(GroovinMaterialIcons.logout, color: cyan,),
            color: cyan,
            splashColor: white,
            onPressed: (){
              Navigator.of(context).pushAndRemoveUntil(new MaterialPageRoute( builder: (BuildContext context) => Login()), ModalRoute.withName('/login'));
              deleteStoredCredential();
              LoginState.credStr = '';
              LinkedInLogInState.user = null;
              LinkedInLogInState.authorizationCode = null;
              LinkedInLogInState.logoutUser = true;
            }),
        ],
      ),
      body: new PageView(
        controller: _tabController,
        onPageChanged: onTabChanged,
        children: <Widget>[
          new _firstTab.Queue(),
          new _secondTab.Contacts(),
        ],
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () {
          Navigator.of(context).push(new MaterialPageRoute( builder: (BuildContext context) => AddUser()));
        },
        tooltip: 'Add',
        child: Icon(GroovinMaterialIcons.plus, size: 30,),
        foregroundColor: white,
        backgroundColor: pink,
      ),
      bottomNavigationBar: Theme.of(context).platform == TargetPlatform.iOS ?
      new CupertinoTabBar(
        backgroundColor: cyan,
        activeColor: off_white,
        currentIndex: _tab,
        onTap: onTap,
        inactiveColor: grey_light,
        items: TabItems.map((TabItem) {
          return new BottomNavigationBarItem(
            title: new Text(TabItem.title),
            icon: new Icon(TabItem.icon),
          );
        }).toList(),
      ):
      bottomNavBar,
    );
  }

}

class TabItem {
  const TabItem({ this.title, this.icon });
  final String title;
  final IconData icon;
}

const List<TabItem> TabItems = const <TabItem>[
  const TabItem(title: 'Queue', icon: GroovinMaterialIcons.clock_alert,),
  const TabItem(title: 'Contacts', icon: GroovinMaterialIcons.timer,),
];
