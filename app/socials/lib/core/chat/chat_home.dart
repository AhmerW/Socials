import 'package:flutter/material.dart';
import 'package:get_it/get_it.dart';

import 'package:socials/config/theme.dart';
import 'package:socials/data/states/auth_state.dart';

class ChatHomeScreen extends StatefulWidget {
  final AuthState authState = GetIt.I.get<AuthState>();

  @override
  _ChatHomeScreenState createState() => _ChatHomeScreenState();
}

class _ChatHomeScreenState extends State<ChatHomeScreen> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
        appBar: AppBar(
          automaticallyImplyLeading: false,
          title: Text('Chat'),
          actions: [IconButton(icon: Icon(Icons.settings), onPressed: () {})],
        ),
        body: SafeArea(
          child: Center(
              child: Column(
            children: [
              ElevatedButton(onPressed: () {}, child: Text('Send test '))
            ],
          )),
        ));
  }
}
