import 'package:flutter/material.dart';
import 'package:get_it/get_it.dart';
import 'package:socials/core/hinit.dart';
import 'package:socials/data/states/auth_state.dart';

import 'package:socials/widgets/relbutton.dart';

class AuthHome extends StatefulWidget {
  @override
  _AuthHomeState createState() => _AuthHomeState();
}

class _AuthHomeState extends State<AuthHome> {
  String status = 'none';
  @override
  Widget build(BuildContext context) {
    return Scaffold(
        appBar: AppBar(
          automaticallyImplyLeading: false,
          title: Text('Socials'),
        ),
        body: Center(
          child: Column(
            children: [
              Container(
                child: RichText(
                  text: TextSpan(
                      text: 'Welcome to Socials\n',
                      style:
                          TextStyle(fontWeight: FontWeight.bold, fontSize: 20),
                      children: <TextSpan>[
                        TextSpan(
                            text: 'Plaese authenticate yourself',
                            style: TextStyle(
                                fontStyle: FontStyle.italic, fontSize: 15))
                      ]),
                ),
              ),
              Transform.translate(
                  offset:
                      Offset(-MediaQuery.of(context).size.width * 0.4, -20.0),
                  child: Container(
                    alignment: Alignment.topLeft,
                    width: 100,
                    height: 100,
                    child: Image.asset('assets/images/koshi-transparent.png'),
                  )),
              RelButton(text: 'Login', func: () {}),
              RelButton(text: 'Register', func: () {}),
              ElevatedButton(onPressed: () {}, child: Text('Continue'))
            ],
          ),
        ));
  }
}
