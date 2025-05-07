# ArenaBuilds Vulnerabilities Report

LINK: [github.com/3nd3r1/cyber-project-1](https://github.com/3nd3r1/cyber-project-1)

## Installation Instructions

1. Clone the repository
2. (Optional) Activate the virtual environment: `python -m venv venv && source venv/bin/activate`
3. Install the required packages: `pip install -r requirements.txt`
4. Run the migrations: `python manage.py migrate arenabuilds`
5. Start the server: `python manage.py runserver`

## FLAW 1: Broken Access Control (A01:2021)

**Source:** [views.py#L16-L18](https://github.com/3nd3r1/cyber-project-1/blob/main/arenabuilds/views.py#L16-L18)

**Description:**
This flaw is example of A01 from the OWASP 2021 list.
The create view doesn't have proper access control and allows non-logged users to access the create page by going directly to the url `/create`.
This is a flaw because it allows unauthorized users to create builds without having an account or being logged in.

**Impact Assessment:**
This vulnerability could lead to:

- Spam content flooding the application
- Application errors w
- Database corruption if null values are used where user references are required

**Risk Rating:** High
This vulnerability is easy to exploit and has consequences for application integrity.

**How to fix it:**
The fix is simple add the `@login_required` decorator at the top of the create view.
This decorator checks if the user is authenticated before allowing access to the view.
If the user is not authenticated, they will be redirected to the login page.

Django handles this nicely by preserving the original requested URL in a parameter, allowing the user to be redirected back to the `/create` page after login.

## FLAW 2: SQL Injection (A03:2021)

**Source:** [views.py#L41-L53](https://github.com/3nd3r1/cyber-project-1/blob/main/arenabuilds/views.py#L41-L53)

**Description:**
This is an example of a A03 from the OWASP 2021 list.
The application does an unsanitized SQL query to the database with the `query`.
This allows an attacker to inject SQL code that could be executed by the database.

The raw sql feature is meant for complex queries that the ORM can't handle, but even in that case the parameters should be parameterized.
In this flaw they are directly formatted in the query.

For example, an someone could use payloads like:

- `' OR '1' = '1` to get all search results
- `' UNION SELECT null, username, password, null, null, null, null from auth_user --` to get the username and encrypted password of all users

**Impact Assessment:**

- An attacker can extract sensitive information from any table in the database
- Can allow attackers to log in as any user without knowing passwords
- Data breaches may violate data protection regulations like GDPR

**Risk Rating:** Critical
SQL injection provide direct access to the database.

**How to fix it:**
The fix is to use Django's ORM, which automatically sanitizes inputs and prevents SQL injection.
By using `Q()` objects, Django will automatically sanitize the input and prevent SQL injection.

## FLAW 3: Cryptographic Failures (A02:2021)

**Source:** [settings.py#L11-L14](https://github.com/3nd3r1/cyber-project-1/blob/main/arenabuilds/settings.py#L11-L14)

**Description:**
This is an example of A02 from the OWASP 2021 list.
The app has the Django SECRET_KEY hardcoded in the settings file, which is then included in version control.
This is a security risk because the SECRET_KEY is used for critical security functions in Django like signing session cookies and encrypting data.
If an attacker gains access to this key, they could potentially forge sessions.

**Impact Assessment:**
This could allow attackers to:

- Forge authenticated sessions and impersonate legitimate users
- Craft valid CSRF tokens to bypass CSRF protections
- Generate valid password reset links for any user in the system
- Decrypt sensitive data that was encrypted using this key

**Risk Rating:** High
Exposure of cryptographic keys fundamentally compromises multiple security mechanisms.

**How to fix it:**
The fix is to store the SECRET_KEY in environment variables rather than in source code.
This way, the secret key is not exposed in version control, making it difficult for attackers to obtain.

The SECRET_KEY can then be stored in an .env file that is not committed to version control.

## FLAW 4: Security Logging and Monitoring Failures (A09:2021)

**Source:** [views.py#L70-L87](https://github.com/3nd3r1/cyber-project-1/blob/main/arenabuilds/views.py#L70-L87)

**Description:**
This is an example of A09 from the OWASP 2021 list.
The application does not log login attempts, so detecting security incidents like bruteforce is much harder.
Without logging, administrators have no way to see suspicious patterns of failed login attempts that could indicate an attack.

**Impact Assessment:**

- Bruteforce attacks might go unnoticed until they succeed.
- After a security incident, investigators lack the necessary logs to investigate it.
- Many regulatory frameworks require authentication logging for audit purposes

**Risk Rating:** Medium
Not exploitable, but this negatively impacts security monitoring.

**How to fix it:**
The fix is to implement logging of all authentication events.
The commented-out fix creates a log for every login attempt, recording the username, IP address, and whether the attempt was successful.
This information is crucial for security monitoring.

## FLAW 5: Identification and Authentication Failures (A07:2021)

**Source:** [forms.py#L36-L39](https://github.com/3nd3r1/cyber-project-1/blob/main/arenabuilds/forms.py#L36-L39)

**Description:**
This is an example of A07 from the OWASP 2021 list.
The registration doesn't enforce / validate strong password policies, allowing users to create accounts with very weak passwords like "123" or "password".
This is a risk because weak passwords are easily guessed by attackers.

**Impact Assessment:**
- Weak passwords can be cracked in seconds to minutes with modern hardware
- Attackers can try common passwords across many accounts simultaneously
- Even strong technical security can be bypassed if users are easily compromised
- Compromising one account can lead to escalation of privileges

**Risk Rating:** High
Weak password implementation creates several critical security risks.

**How to fix it:**
The fix is to properly validate passwords during registration.
The commented-out fix calls `validate_password` , which applies built-in validators defined in the `AUTH_PASSWORD_VALIDATORS` setting.
These validators typically check for many common password patterns and requirements.
