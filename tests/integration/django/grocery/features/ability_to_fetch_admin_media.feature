Feature: fetch admin media from lettuce + django builtin server
  Scenario: Running on port 7000
    Given my settings.py has "LETTUCE_SERVER_PORT" set to "7000"
    Then I see that requesting "http://127.0.0.1:7000/static/admin/css/base.css" gets "200"

  Scenario: Fetching admin media
    Given I navigate to "/admin/"
    When I try to resolve the assets provided by given HTML
    When all the responses have status code 200
    Then all the responses have are between one of those mime types:
      | mime-type              |
      | text/css               |
      | text/javascript        |
      | application/javascript |

  Scenario: Fetching static files
    Given I navigate to "/static/lettuce.jpg"
    Then it should be an image

  Scenario: Fetching CSS files:
    Given I fetch the urls:
      | url                               |
      | /static/admin/css/base.css        |
      | /static/admin/css/changelists.css |
      | /static/admin/css/dashboard.css   |
      | /static/admin/css/forms.css       |
      | /static/admin/css/ie.css          |
      | /static/admin/css/login.css       |
      | /static/admin/css/rtl.css         |
      | /static/admin/css/widgets.css     |
    When all the responses have status code 200
    Then all the responses have mime type "text/css"

  Scenario: Fetching javascript files:
    Given I fetch the urls:
      | url                                       |
      | /static/admin/js/actions.js               |
      | /static/admin/js/calendar.js              |
      | /static/admin/js/core.js                  |
      | /static/admin/js/timeparse.js             |
      | /static/admin/js/urlify.js                |
    When all the responses have status code 200
    Then all the responses have mime type "application/javascript"
