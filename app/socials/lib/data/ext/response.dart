import 'package:http/http.dart' as http;

class ServerResponse {
  late int code;
  late Map<String, dynamic> data;
  Map<String, String> headers;

  ServerResponse(
      {required this.headers, int code = 200, Map<String, dynamic>? data}) {
    this.code = code;
    this.data = data ?? {};
  }
}
