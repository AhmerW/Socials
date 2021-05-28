import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';

class InpField extends StatelessWidget {
  final String? hintText;
  final TextEditingController textEditingController = TextEditingController();

  final double widthPercentage;
  final bool isPassword;

  InpField(
      {this.hintText, this.widthPercentage = 0.7, this.isPassword = false});

  String getText() {
    return textEditingController.text;
  }

  @override
  Widget build(BuildContext context) {
    return Container(
        width: MediaQuery.of(context).size.width * widthPercentage,
        child: TextField(
          enableSuggestions: !isPassword,
          autocorrect: !isPassword,
          obscureText: isPassword,
          controller: textEditingController,
          decoration: InputDecoration(hintText: hintText ?? ''),
        ));
  }
}
