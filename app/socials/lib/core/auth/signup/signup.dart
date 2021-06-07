import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:flutter/scheduler.dart';
import 'package:get_it/get_it.dart';
import 'package:socials/config/theme.dart';
import 'package:socials/core/hinit.dart';
import 'package:socials/data/states/auth_state.dart';
import 'package:socials/widgets/inpfield.dart';

class AuthSignupScreen extends StatefulWidget {
  @override
  _AuthSignupScreenState createState() => _AuthSignupScreenState();
}

class _AuthSignupScreenState extends State<AuthSignupScreen> {
  bool success = false;
  InpField inpUsername = InpField(hintText: 'username');
  InpField inpPassword = InpField(hintText: 'password', isPassword: true);
  InpField inpEmail = InpField(hintText: 'email (optional)');
  String? errorMsg;
  bool errorMsgFail = true;
  int tries = 0;

  @override
  void dispose() {
    inpUsername.textEditingController.dispose();
    inpPassword.textEditingController.dispose();
    inpEmail.textEditingController.dispose();
    super.dispose();
  }

  @override
  void initState() {
    super.initState();
  }

  void attemptLogin() async {
    final String username = inpUsername.getText();
    final String email = inpEmail.getText();
    final String password = inpPassword.getText();

    final AuthStateResponse authStateResponse = await AuthState.fromNew(
      username: username,
      password: password,
      email: email.isEmpty ? null : email,
    );
    if (authStateResponse.ok) {
      Navigator.pushNamed(context, '/auth/confirmation');
    } else {
      setState(() {
        errorMsgFail = !authStateResponse.ok;
        errorMsg = authStateResponse.text;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    bool darkTheme = Theme.of(context).brightness == Brightness.dark;
    return Scaffold(
        backgroundColor: !darkTheme ? Colors.white : null,
        body: Column(
          children: [
            ConstrainedBox(
              constraints: BoxConstraints(maxHeight: 300),
              child: Container(
                  alignment: darkTheme ? Alignment.center : Alignment.topLeft,
                  child: darkTheme
                      ? Image.asset('assets/images/login-transparent.png')
                      : Image.asset(
                          'assets/images/register.png',
                        )),
            ),
            errorMsg != null
                ? Container(
                    child: Text(
                    errorMsg as String,
                    style: TextStyle(
                        color: errorMsgFail ? Colors.red : Colors.green),
                  ))
                : SizedBox.shrink(),
            Container(
              child: Center(
                child: SafeArea(
                  child: Column(
                    children: [
                      inpUsername,
                      Container(
                        padding: EdgeInsets.only(top: 10, bottom: 30),
                        child: inpEmail,
                      ),
                      inpPassword
                    ],
                  ),
                ),
              ),
            ),
            Container(
                padding: EdgeInsets.all(20.0),
                width: 200,
                child: ElevatedButton(
                    onPressed: attemptLogin, child: Text('Register'))),
            Container(
              padding: EdgeInsets.only(top: 20),
              child: TextButton(
                  onPressed: () {
                    Navigator.of(context).pop();
                  },
                  child: Text('Already have an account? Login')),
            )
          ],
        ));
  }
}
