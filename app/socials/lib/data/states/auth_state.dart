import 'package:socials/config/constants.dart';
import 'package:socials/data/ext/network.dart';
import 'package:socials/data/ext/response.dart';
import 'package:socials/models/user.dart';

class AuthState {
  final User user;
  final String token;
  String? errorMsg;
  bool authenticated;

  AuthState(this.user, this.token,
      {required this.authenticated, this.errorMsg});

  String authToken() {
    return 'bearer $token';
  }

  static Future<AuthState> create(
      {required String username, required String password}) async {
    ServerResponse req =
        await ServerRequest(serverUrl, '/auth/token', type: 'http').fetch(
            RequestType.Post,
            body: {'username': username, 'password': password});

    if (req.data.containsKey('access_token')) {
      String token = req.data['access_token'];
      ServerResponse details = await ServerRequest(serverUrl, '/user/profile',
              type: 'http')
          .fetch(RequestType.Get, headers: {'Authorization': 'bearer $token'});

      return AuthState(
          User(uid: details.data['uid'], username: details.data['username']),
          token,
          authenticated: true);
    }

    return AuthState(User(uid: 0, username: '0'), '0',
        authenticated: false, errorMsg: req.data['detail']);
  }
}
