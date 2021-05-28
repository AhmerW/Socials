import 'package:flutter/material.dart';
import 'package:get_it/get_it.dart';
import 'package:socials/core/auth/auth_home.dart';
import 'package:socials/core/auth/login/login.dart';
import 'package:socials/core/hinit.dart';

import 'package:socials/core/home/home.dart';
import 'package:socials/config/theme.dart';
import 'package:socials/data/local/secstorage.dart';
import 'package:socials/data/states/auth_state.dart';
import 'package:socials/models/user.dart';

Future<AuthState> setup() async {
  SecureStorage secureStorage = SecureStorage();
  GetIt.I.registerSingleton<SecureStorage>(secureStorage);
  GetIt.I.allowReassignment = true;

  return await AuthState.create(username: 'test', password: 'test');
}

void main() {
  setup().then((value) {
    GetIt.I.registerSingleton<AuthState>(value);
    runApp(SocialsApp());
  });
}

class SocialsApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Socials',
      initialRoute: '/home/init',
      debugShowCheckedModeBanner: false,
      // Light theme data
      theme: ThemeData(
          textTheme: TextTheme(bodyText1: TextStyle(color: Colors.black)),
          primarySwatch: Colors.grey,
          primaryColor: Colors.white,
          brightness: Brightness.light,
          dividerColor: Colors.black12,
          backgroundColor: AppColors.colorWhite,
          accentColor: Colors.black,
          accentIconTheme: IconThemeData(color: Colors.white),
          floatingActionButtonTheme: FloatingActionButtonThemeData(
              backgroundColor: AppColors.colorMain)),
      // Dark theme data
      darkTheme: ThemeData(
          primarySwatch: Colors.grey,
          accentColor: Colors.white,
          primaryColor: AppColors.colorDarker,
          brightness: Brightness.dark,
          accentIconTheme: IconThemeData(color: Colors.black),
          dividerColor: Colors.white54,
          bottomNavigationBarTheme: BottomNavigationBarThemeData(
              selectedItemColor: Colors.white,
              unselectedIconTheme: IconThemeData(color: AppColors.colorUI),
              showUnselectedLabels: false,
              showSelectedLabels: true,
              selectedLabelStyle: TextStyle(color: Colors.grey),
              selectedIconTheme: IconThemeData(color: Colors.white)),
          floatingActionButtonTheme: FloatingActionButtonThemeData(
              foregroundColor: Colors.white,
              backgroundColor: AppColors.colorDarker)),
      // Current theme
      themeMode: ThemeMode.dark,
      routes: {
        '/home': (context) => AppHome(),
        HomeInit.routeName: (context) => HomeInit(),
        '/auth/home': (context) => AuthHome(),
        '/auth/login': (context) => AuthLoginScreen()
      },
    );
  }
}
