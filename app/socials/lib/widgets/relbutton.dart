import 'package:flutter/material.dart';

class RelButton extends StatelessWidget {
  final String text;
  final Function() func;
  RelButton({required this.text, required this.func});

  @override
  Widget build(BuildContext context) {
    return Container(
        padding: EdgeInsets.only(left: 20, right: 20, top: 10, bottom: 10),
        width: MediaQuery.of(context).size.width * 0.7,
        height: MediaQuery.of(context).size.height * 0.12,
        child: ElevatedButton(onPressed: func, child: Text(text)));
  }
}
