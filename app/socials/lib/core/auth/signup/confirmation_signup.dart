import 'package:flutter/material.dart';
import 'package:socials/config/theme.dart';

class AuthSignupConfirmation extends StatefulWidget {
  AuthSignupConfirmation({Key? key}) : super(key: key);

  @override
  _AuthSignupConfirmationState createState() => _AuthSignupConfirmationState();
}

class _AuthSignupConfirmationState extends State<AuthSignupConfirmation> {
  @override
  Widget build(BuildContext context) {
    bool darkTheme = Theme.of(context).brightness == Brightness.dark;
    MaterialStateProperty whiteThemeBg =
        MaterialStateProperty.all<Color>(AppColors.colorMain);
    return Scaffold(
      appBar: AppBar(
        title: Text('Socials'),
        automaticallyImplyLeading: false,
      ),
      body: SafeArea(
          child: Center(
              child: Column(children: [
        Text(
          'Welcome!',
          style: TextStyle(fontSize: 20),
        ),
        Text(
            'Please check your email in order to continue the registration process'),
        Container(
            padding: EdgeInsets.only(top: 50),
            width: MediaQuery.of(context).size.width * 0.7,
            child: ElevatedButton(
              child: Row(children: [
                Icon(
                  Icons.send,
                ),
                Text('Resend confirmation link')
              ]),
              onPressed: () {},
            )),
        Container(
            padding: EdgeInsets.only(top: 50),
            width: MediaQuery.of(context).size.width * 0.7,
            child: ElevatedButton(
              child: Row(children: [
                Icon(
                  Icons.login,
                ),
                Text('Login')
              ]),
              onPressed: () {
                Navigator.pushNamed(context, '/auth/login');
              },
            )),
      ]))),
    );
  }
}
