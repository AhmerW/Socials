import 'package:socials/config/constants.dart';
import 'package:socials/data/ext/network.dart';
import 'package:socials/data/ext/response.dart';
import 'package:socials/models/user.dart';

class AuthStateResponse {
  final bool ok;
  final AuthState? authState;
  final String? text;
  AuthStateResponse({required this.ok, required this.authState, this.text});
}

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

  factory AuthState.empty() {
    return AuthState(User(uid: 0, username: '0'), '', authenticated: false);
  }

  static Future<AuthStateResponse> fromNew({
    required String username,
    required String password,
    required String? email,
  }) async {
    ServerResponse req = await ServerRequest(
      serverUrl,
      '/account/new',
      type: 'http',
    ).fetch(
      RequestType.Post,
      encodeBody: true,
      body: {
        'username': username,
        'password': password,
        'email': email,
      },
    );
    late String? text;

    text = req.detail;
    return AuthStateResponse(
      ok: req.ok,
      authState: null,
      text: text,
    );
  }

  static Future<AuthStateResponse> create({
    required String username,
    required String password,
  }) async {
    ServerResponse req = await ServerRequest(
      serverUrl,
      '/auth/token',
      type: 'http',
    ).fetch(
      RequestType.Post,
      encodeBody: false,
      body: {'username': username, 'password': password},
    );
    print(req.data);
    if (req.data.containsKey('access_token')) {
      String token = req.data['access_token'];
      ServerResponse details = await ServerRequest(
        serverUrl,
        '/user/profile',
        type: 'http',
      ).fetch(
        RequestType.Get,
        headers: {'Authorization': 'bearer $token'},
      );

      return AuthStateResponse(
          ok: true,
          authState: AuthState(
            User(
              uid: details.data['uid'],
              username: details.data['username'],
            ),
            token,
            authenticated: true,
          ));
    }
    return AuthStateResponse(ok: false, authState: null, text: req.detail);
  }
}
