class AppRoutes {
  // The Home-Route. Equals to the main homepage.
  static const home = '/';

  // Login route. The main login page (different from signin & signup)
  static const login = '/login';

  // The signup route where user enters credentials to gain access.
  static const signin = '/signup';

  // Signup route equals to the register page, where user creates a new
  // Socials account.
  static const signup = '/signup';
}

class ChatRoutes {
  // Home of the chat tab.
  // This page lists all chats, including group chats,
  // and general information.
  static const home = '/chat-home';

  // The main chat screen where user interacts
  // With an entry field and views all messages
  // Sorted by the date.
  static const chat = '/chat-screen';
}
