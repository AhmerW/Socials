import 'dart:convert';
import 'dart:io';

import 'package:http/http.dart' as http;
import 'package:socials/data/ext/response.dart';

enum RequestType { Post, Get }

class ServerRequest {
  late final Uri url;
  ServerRequest(String urlstring, String path, {String type = 'https'}) {
    this.url = type == 'https'
        ? Uri.https(urlstring, path)
        : Uri.http(urlstring, path);
  }

  Future<ServerResponse> fetch(RequestType type,
      {Map<String, String>? headers, Map<String, dynamic>? body}) async {
    var resp;
    if (type == RequestType.Post) {
      resp = await http.post(url, headers: headers, body: body);
    } else if (type == RequestType.Get) {
      resp = await http.get(url, headers: headers);
    }
    return ServerResponse(
        headers: resp.headers,
        code: resp.statusCode,
        data: jsonDecode(resp.body));
  }
}
