# KIPPForward-SourceStudentDataConnector

## Getting Started

### Setup Environment

1. Clone this repo

```
git clone https://github.com/kippnorcal/KIPPForward-SourceStudentDataConnector.git
```

2. Install dependencies

- Docker can be installed directly from the website at docker.com.
- Pipenv can be installed via Pip or Homebrew, and is only needed for local development or to generate an initial token.

3. Create .env file with project secrets

Database variables are configured in the format used by [Sqlsorcery](https://sqlsorcery.readthedocs.io/en/latest/cookbook/environment.html).

```
# Database variables
DB_SERVER=
DB=
DB_SCHEMA=
DB_USER=
DB_PWD=

# Key for the tracker's Google Sheet
SHEET_KEY=

# Mailgun variables
MG_API_KEY=
MG_API_URL=
MG_DOMAIN=

# Email Notification Variables
SENDER_EMAIL=
RECIPIENT_EMAIL=
```

4. Enable APIs in Developer Console

- Navigate to the [API library](https://console.developers.google.com/apis/library) in the developer console.
- Search for Admin SDK, and Enable it.

5. Create a service account.

- In the Google Developer Console (console.developers.google.com), go to Credentials.
- Click on "Create Credentials -> Service Account"
- Create a name for your service account.
- Select the "Owner" role for the service account.
- Create a key, saving the result file as `service_account_cred.json`. Move this file to the project directory.
- Check the box for "Enable G Suite Domain-Wide Delegation"
- Click "Done".

6. Add scopes for the service account.

- In the Google Admin Console (admin.google.com), go to Security.
- Click on "Advanced Settings -> Manage API client access"
- For the client name, use the Unique ID of the service account.
- In the API Scopes, add the following scopes and click "Authorize".

```
https://www.googleapis.com/auth/admin.directory.user,
https://www.googleapis.com/auth/admin.directory.group
```
### Running the job

Navigate to the project dir and build the Docker image

```
docker build -t source-student-data .
```

Run the job

```
docker run --rm -t source-student-data
```

### Maintenance

* Dates in the `KTC_Match_Tracker_Students.sql` need to be updated every school year
* This job can be paused over the summer
