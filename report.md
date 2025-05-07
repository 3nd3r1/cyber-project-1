# ArenaBuilds Vulnerabilities Report

LINK: [github.com/3nd3r1/cyber-project-1](https://github.com/3nd3r1/cyber-project-1)

## Installation Instructions

1. Clone the repository
2. (Optional) Activate the virtual environment: `python -m venv venv && source venv/bin/activate`
2. Install the required packages: `pip install -r requirements.txt`
3. Run the migrations: `python manage.py migrate arenabuilds`
4. Start the server: `python manage.py runserver`

## FLAW 1: Broken Access Control (A01:2021)

**Source:** [views.py#L16-L18](https://github.com/3nd3r1/cyber-project-1/blob/main/arenabuilds/views.py#L16-L18)

**Description:**
This flaw is example of A01 from the OWASP 2021 list.
The create view doesn't have proper access control and allows non-logged users to access the create page by going directly to the url `/create`.
This is a flaw because it allows unauthorized users to create builds without having an account or being logged in.

**How to fix it:**
The fix is simple add the `@login_required` decorator at the top of the create view.
This decorator checks if the user is authenticated before allowing access to the view.
If the user is not authenticated, they will be redirected to the login page.

## FLAW 2: SQL Injection (A03:2021)

**Source:** [views.py#L41-L53](https://github.com/3nd3r1/cyber-project-1/blob/main/arenabuilds/views.py#L41-L53)

**Description:**
This is an example of a A03 from the OWASP 2021 list.
The application does an unsanitized SQL query to the database with the `query`.
This allows an attacker to inject SQL code that could be executed by the database.
For example, an someone could enter `' OR '1'='1` in the search box, which would modify the WHERE clause to always evaluate to true, and return all builds.

**How to fix it:**
The fix is to use Django's ORM, which automatically sanitizes inputs and prevents SQL injection.
By using `Q()` objects, Django will automatically sanitize the input and prevent SQL injection.

## FLAW 3: Cryptographic Failures (A02:2021)

**Source:** [settings.py#L11-L14](https://github.com/3nd3r1/cyber-project-1/blob/main/arenabuilds/settings.py#L11-L14)

**Description:**
This is an example of A02 from the OWASP 2021 list.
The app has the Django SECRET_KEY hardcoded in the settings file, which is then included in version control.
This is a security risk because the SECRET_KEY is used for critical security functions in Django.
If an attacker gains access to this key, they could potentially forge sessions.

**How to fix it:**
The fix is to store the SECRET_KEY in environment variables rather than in source code.
This way, the secret key is not exposed in version control, making it difficult for attackers to obtain.

## FLAW 4: Security Logging and Monitoring Failures (A09:2021)

**Source:** [views.py#L70-L87](https://github.com/3nd3r1/cyber-project-1/blob/main/arenabuilds/views.py#L70-L87)

**Description:**
This is an example of A09 from the OWASP 2021 list.
The application does not log login attempts, so detecting security incidents like bruteforce is much harder.
Without logging, administrators have no way to see suspicious patterns of failed login attempts that could indicate an attack.

**How to fix it:**
The fix is to implement logging of all authentication events.
The commented-out fix creates a log for every login attempt, recording the username, IP address, and whether the attempt was successful.
This information is crucial for security monitoring.

## FLAW 5: Identification and Authentication Failures (A07:2021)

**Source:** [forms.py#L36-L39](https://github.com/3nd3r1/cyber-project-1/blob/main/arenabuilds/forms.py#L36-L39)

**Description:**
This is an example of A07 from the OWASP 2021 list.
The registration doesn't enforce / validate strong password policies, allowing users to create accounts with very weak passwords.
This is a risk because weak passwords are easily guessed by attackers.

**How to fix it:**
The fix is to properly validate passwords during registration.
The commented-out fix calls `validate_password` , which applies built-in validators defined in the `AUTH_PASSWORD_VALIDATORS` setting.
These validators typically check for many common password patterns and requirements.
