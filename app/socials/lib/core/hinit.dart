import 'package:flutter/material.dart';
import 'package:get_it/get_it.dart';
import 'package:socials/core/auth/auth_home.dart';
import 'package:socials/core/auth/login/login.dart';
import 'package:socials/core/home/home.dart';
import 'package:socials/data/local/secstorage.dart';
import 'package:socials/data/states/auth_state.dart';

class HomeInitArguments {
  bool checkLocal = true;

  HomeInitArguments({this.checkLocal = true});
}

class HomeInit extends StatefulWidget {
  static const routeName = '${AppHome.routeName}/init';
  @override
  _HomeInitState createState() => _HomeInitState();
}

class _HomeInitState extends State<HomeInit> {
  Future<void> checkStorage() async {
    print('checking storage');

    SecureStorage secureStorage = GetIt.I.get<SecureStorage>();
    AuthState.create(
            username: await secureStorage.read(key: 'username') as String,
            password: await secureStorage.read(key: 'password') as String)
        .then((value) => GetIt.I.registerSingleton<AuthState>(value));
  }

  @override
  Widget build(BuildContext context) {
    return GetIt.I.get<AuthState>().authenticated
        ? AppHome()
        : AuthLoginScreen();
  }
}
