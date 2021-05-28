import 'package:flutter/material.dart';

enum AppTheme { Light, Dark }

Map<int, Color> colorDark = {};

class AppColors {
  static const AppTheme theme = AppTheme.Light;

  static const Color colorUI = Color(0xFF474747);
  static const Color colorMain = Color(0xFF0099ff);

  static const Color colorDark = Color(0xFF2e2e2e);
  static const Color colorDarker = Color(0xFF292828);

  static const Color colorWhite = Color(0xFFe5e5e5);
}
