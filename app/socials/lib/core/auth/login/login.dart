import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:flutter/scheduler.dart';
import 'package:get_it/get_it.dart';
import 'package:socials/config/theme.dart';
import 'package:socials/core/hinit.dart';
import 'package:socials/data/states/auth_state.dart';
import 'package:socials/widgets/inpfield.dart';

class AuthLoginScreen extends StatefulWidget {
  @override
  _AuthLoginScreenState createState() => _AuthLoginScreenState();
}

class _AuthLoginScreenState extends State<AuthLoginScreen> {
  InpField inpUsername = InpField(hintText: 'username');
  InpField inpPassword = InpField(hintText: 'password', isPassword: true);
  String? errorMsg;
  bool errorMsgFail = true;
  int tries = 0;

  @override
  void dispose() {
    inpUsername.textEditingController.dispose();
    inpPassword.textEditingController.dispose();
    super.dispose();
  }

  @override
  void initState() {
    inpPassword.textEditingController.addListener(() {
      if (errorMsg != null) {
        setState(() {
          errorMsg = null;
        });
      }
    });
    super.initState();
  }

  void attemptLogin() async {
    final String username = inpUsername.getText();
    final String password = inpPassword.getText();

    if (username.isNotEmpty && password.isNotEmpty) {
      AuthState authState =
          await AuthState.create(username: username, password: password);
      if (authState.authenticated) {
        GetIt.I.registerSingleton<AuthState>(authState);

        Navigator.pushNamed(context, '/home/init',
            arguments: HomeInitArguments(checkLocal: false));
        errorMsgFail = false;
      } else {
        errorMsgFail = true;
      }
      setState(() {
        if (errorMsg != null && errorMsg == authState.errorMsg) {
          tries += 1;
        }
        errorMsg = authState.errorMsg;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    bool darkTheme = Theme.of(context).brightness == Brightness.dark;
    return Scaffold(
        appBar: AppBar(
          backgroundColor:
              !darkTheme ? AppColors.colorMain : AppColors.colorDarker,
          automaticallyImplyLeading: false,
          title: Text('Socials'),
        ),
        body: Column(
          children: [
            ConstrainedBox(
              constraints: BoxConstraints(maxHeight: 300),
              child: Container(
                  alignment: darkTheme ? Alignment.center : Alignment.topLeft,
                  child: darkTheme
                      ? Image.asset('assets/images/login-transparent.png')
                      : Image.asset(
                          'assets/images/login.png',
                        )),
            ),
            errorMsg != null
                ? Container(
                    child: Text(
                    '[$tries] ${errorMsg as String}',
                    style: TextStyle(
                        color: errorMsgFail ? Colors.red : Colors.green),
                  ))
                : SizedBox.shrink(),
            Center(
              child: SafeArea(
                child: Column(
                  children: [inpUsername, inpPassword],
                ),
              ),
            ),
            Container(
                padding: EdgeInsets.all(20.0),
                width: 200,
                child: ElevatedButton(
                    onPressed: attemptLogin, child: Text('Login'))),
            Container(
              padding: EdgeInsets.only(top: 20),
              child: TextButton(
                  onPressed: () {}, child: Text('No account? Register')),
            )
          ],
        ));
  }
}
