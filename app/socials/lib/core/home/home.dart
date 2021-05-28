import 'package:flutter/material.dart';
import 'package:socials/core/chat/chat_home.dart';
import 'package:socials/config/theme.dart';
import 'package:socials/core/home/home_screen.dart';
import 'package:socials/data/states/auth_state.dart';
import 'package:socials/models/user.dart';

class AppHome extends StatefulWidget {
  static const routeName = '/home';
  @override
  _AppHomeState createState() => _AppHomeState();
}

class _AppHomeState extends State<AppHome> {
  int _currentIndex = 0;

  static final _tabChat = ChatHomeScreen();
  static final _tabHome = HomeScreen();

  static final List<Widget> _tabScreens = <Widget>[_tabHome, _tabChat];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      bottomNavigationBar: BottomNavigationBar(
        onTap: (int index) {
          setState(() {
            _currentIndex = index;
          });
        },
        currentIndex: _currentIndex,
        selectedItemColor: Colors.grey,
        showSelectedLabels: true,
        showUnselectedLabels: false,
        items: const <BottomNavigationBarItem>[
          BottomNavigationBarItem(icon: Icon(Icons.home), label: 'home'),
          BottomNavigationBarItem(icon: Icon(Icons.chat), label: 'chat'),
        ],
      ),
      floatingActionButtonAnimator: FloatingActionButtonAnimator.scaling,
      floatingActionButtonLocation: FloatingActionButtonLocation.centerDocked,
      floatingActionButton: Container(
          height: 40,
          width: 40,
          child: FittedBox(
              child: FloatingActionButton(
            heroTag: 'main_fab',
            child: Icon(Icons.add),
            onPressed: () {},
          ))),
      body: _tabScreens[_currentIndex],
    );
  }
}
