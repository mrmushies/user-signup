import webapp2
import re
from string import letters

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and PASS_RE.match(password)

EMAIL_RE  = re.compile(r'^[\S]+@[\S]+\.[\S]+$')

def valid_email(email):
    return not email or EMAIL_RE.match(email)

head = """
<!DOCTYPE html>
<html>
<head>
    <title>User Signup</title>

</head>

<body>
    <h1>Signup</h1>
"""

foot = """
</body>
</html>
"""

form = """
        <form method="post">
          <table>
            <tr>
              <td>
                Username
              </td>
              <td>
                <input type="text" name="username" value="%(username)s">
              </td>
              <td style="color:red">
                %(username_error)s
              </td>
            </tr>

            <tr>
              <td>
                Password
              </td>
              <td>
                <input type="password" name="password" value="">
              </td>
              <td style="color:red">
                %(password_error)s
              </td>
            </tr>

            <tr>
              <td>
                Verify Password
              </td>
              <td>
                <input type="password" name="verify" value="">
              </td>
              <td style="color:red">
                %(verify_error)s
              </td>
            </tr>

            <tr>
              <td>
                Email (optional)
              </td>
              <td>
                <input type="text" name="email" value="%(email)s">
              </td>
              <td style="color:red">
                %(email_error)s
              </td>
            </tr>
          </table>

          <input type="submit" value="Submit">
        </form>

"""

class MainPage(webapp2.RequestHandler):
    def write_form(self, username="", email="", username_error="", password_error="", verify_error="", email_error=""):
        self.response.out.write(head + form % {"username": username,
                                        "email": email,
                                        "username_error": username_error,
                                        "password_error": password_error,
                                        "verify_error": verify_error,
                                        "email_error": email_error} + foot)

    def get(self):
        #self.response.headers["Content-Type"] = "text/plain"
        self.write_form()

    def post(self):
        have_error = False
        username = self.request.get("username")
        password = self.request.get("password")
        verify = self.request.get("verify")
        email = self.request.get("email")

        username_error = ""
        password_error = ""
        verify_error = ""
        email_error = ""


        if not valid_username(username):
            username_error += "That's not a valid username."
            have_error = True

        if not valid_password(password):
            password_error += "That's not a valid password."
            have_error = True

        elif password != verify:
            verify_error += "Your passwords didn't match."
            have_error = True

        if not valid_email(email):
            email_error += "That's not a valid email."
            have_error = True




        if have_error:
            self.write_form(username, email, username_error, password_error, verify_error, email_error)
        else:
            self.redirect("/welcome?username=" + username)

class WelcomeHandler(webapp2.RequestHandler):
    def get(self):
        username = self.request.get("username")
        welcome_msg = "<b style='font-size:40px'>" + "Welcome, " + username + "!</b>"
        self.response.out.write(welcome_msg)


app = webapp2.WSGIApplication([('/', MainPage),
                               ('/welcome', WelcomeHandler)],
                               debug=True)
