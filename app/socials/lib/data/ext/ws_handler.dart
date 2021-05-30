import 'dart:convert';

import 'package:socials/config/constants.dart';
import 'package:socials/data/ext/network.dart';
import 'package:socials/data/states/auth_state.dart';
import 'package:web_socket_channel/io.dart';
import 'package:web_socket_channel/web_socket_channel.dart';

enum WsEvent { Chat, Message, Notice, Friend }

class WsHandler {
  final Map<WsEvent, List<Function(Map<String, dynamic>)>> events =
      Map.fromIterable(
    WsEvent.values,
    key: (item) => item,
    value: (_) => [],
  );

  late WebSocketChannel channel;

  void connect({
    required String url,
    required AuthState authState,
  }) {
    ServerRequest(
      serverUrl,
      '/code',
      type: 'http',
    ).fetch(
      RequestType.Get,
      headers: {'Authorization': authState.authToken()},
    ).then((response) {
      if (response.code == 200 && response.data.containsKey('code')) {
        this.channel = IOWebSocketChannel.connect(
          Uri.parse('$url?code=${response.data["code"]}'),
          headers: {'Authorization': authState.authToken()},
        );
      }
    });
  }

  void _onReceive(WsEvent event, Map<String, dynamic> data) {
    for (Function func in events[event]!) {
      func(data);
    }
  }

  void subscribe(WsEvent event, Function(Map<String, dynamic>) function) {
    events[event]!.add(function);
  }

  void run() {
    print('listening');
    channel.stream.listen((raw) {
      Map<String, dynamic> data = jsonDecode(raw);
      if (data.containsKey('event') && data.containsKey('data')) {
        late WsEvent? event;
        switch (data['event']) {
          case 'chat':
            event = WsEvent.Chat;
            break;
          case 'message':
            event = WsEvent.Message;
            break;
          case 'friend':
            event = WsEvent.Friend;
            break;
          case 'notice':
            event = WsEvent.Notice;
            break;
        }
        if (event != null) {
          _onReceive(event, data['data']);
        }
      }
    });
  }
}
