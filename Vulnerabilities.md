**THIS IS THE DOCUMENTATION FOR THE VULNERABILITIES**<br>
**Author - Niskarsh Srivastava**<br>
**Date - 19 Jan, 2025**<br>

# 1. Reflected Cross-Site Scripting (XSS)

## Description

Reflected Cross-Site Scripting (XSS) occurs when an attacker injects malicious scripts into a web application, which are then reflected back to users in a way that executes within their browser. This type of XSS typically occurs when user input is included in server responses without proper sanitization or escaping.

### Example
Consider a search functionality in a web application that takes user input and displays it on the results page:

> https://example.com/search?q=<script>alert('XSS')</script>

If the application directly includes this input in the response without proper encoding, the injected script will execute in the user's browser, displaying an alert box.

## Impact

- **Session Hijacking**: Attackers can steal session cookies and impersonate users.
- **Phishing Attacks**: Users can be tricked into entering credentials on a fake page.
- **Malware Injection**: Malicious scripts can be used to deliver malware to victims.
- **Data Theft**: Sensitive user data can be extracted and sent to an attacker-controlled server.

## Mitigation

- **Input Sanitization**: Ensure user input is properly sanitized before including it in responses.
- **Output Encoding**: Encode user input before rendering it in HTML, JavaScript, or attributes.
- **Content Security Policy (CSP)**: Implement a strong CSP to limit script execution.
- **Use Secure Frameworks**: Utilize frameworks that automatically escape user input, such as React or Angular.
- **Disable Dangerous Functions**: Avoid using functions like `document.write()` and `eval()` that can execute arbitrary code.

---

# 2. Insecure Direct Object References (IDOR)

## Description

Insecure Direct Object References (IDOR) occur when an application exposes internal object references (such as user IDs, file names, or database keys) without proper authorization checks. This vulnerability allows attackers to manipulate these references to access unauthorized data or perform actions on behalf of other users.

### Example
Consider a web application where users can view their account details via the following URL:

> https://example.com/profile?user_id=123

If the application does not properly verify the user's authorization, an attacker can change the user_id parameter to access another user's profile:

https://example.com/profile?user_id=456

If the application directly retrieves and displays the profile data without authorization checks, the attacker gains unauthorized access to another user's information.

## Impact

- **Data Breach**: Attackers can access sensitive user data (e.g., personal details, financial information).
- **Account Takeover**: In some cases, attackers can modify parameters to gain control over other user accounts.
- **Privilege Escalation**: If an attacker manipulates object references related to permissions or roles, they may gain higher privileges.

## Mitigation
- **Access Controls**: Implement strict authorization checks to ensure users can only access their own resources.
- **Use Indirect References**: Instead of exposing internal IDs, use securely mapped references (e.g., UUIDs or hashed values).
- **Validate User Permissions**: Always verify that the authenticated user has the right to access the requested resource.
- **Avoid Sequential Identifiers**: Use unpredictable identifiers to make enumeration attacks more difficult.

---

# 3. Hardcoding Information

## Description

Hardcoding sensitive information, such as passwords, API keys, or database credentials, into the source code of an application. This practice makes the application vulnerable to attacks if the source code is compromised.

## Example

Consider a web application that hardcodes a database password in its configuration file:

> $database_password = 'secretpassword';

If an attacker gains access to the source code, they can easily see and use this password.

## Impact

- Unauthorized Access: Attackers can gain unauthorized access to sensitive data.
- Data Breach: Sensitive data can be stolen or modified.
- Compromise of Other Systems: If the same credentials are used elsewhere, those systems can also be compromised.

## Mitigation

- Configuration Files: Store sensitive information in configuration files that are not included in version control.
- Environment Variables: Use environment variables to store sensitive information.
- Secret Management: Use secret management tools like HashiCorp Vault or AWS Secrets Manager.
- Regular Audits: Regularly audit the codebase for hardcoded sensitive information.

---

# 4. Weak Credentials

## Description

Using default or well-known credentials for administrative or privileged access to systems or applications. This practice makes it easy for attackers to gain unauthorized access if they are aware of the default credentials.

## Example

Consider a router with default credentials like:

> Username: admin
> Password: admin

If an attacker knows these default credentials, they can easily log in and gain control over the router.

## Impact

- Unauthorized Access: Attackers can gain unauthorized access to the system.
- Data Breach: Sensitive data can be stolen or modified.
- System Compromise: The entire system can be compromised.

## Mitigation

- Change Default Credentials: Always change default credentials to strong, unique passwords.
- Complex Passwords: Use complex passwords that are not easily guessable.
- Regular Updates: Make sure to regularly update the account's password

---
