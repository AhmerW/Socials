import 'package:http/http.dart' as http;

class ServerResponse {
  late int code;
  String? detail;
  bool ok = false;

  late Map<String, dynamic> data;
  Map<String, String> headers;
  late Map<String, dynamic> error;

  ServerResponse({
    required Map<String, dynamic> raw,
    required this.headers,
    required this.code,
  }) {
    // Format of the api
    // {ok: bool, status: int, error: map, data: map}
    this.ok = raw['ok'] ?? false;
    this.data = raw['data'] ?? {};
    this.detail = raw['detail'];
    this.error = raw['error'] ?? {};
  }
}
