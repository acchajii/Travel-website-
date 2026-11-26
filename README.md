# Roamly Travel – Travel Agency Website

A responsive Flask travel website demo with destination packages, enquiry form, SQLite storage and a simple admin dashboard.

## Run locally
1. Install Python 3.10+.
2. Open a terminal in this folder.
3. Run `pip install -r requirements.txt`.
4. Run `python app.py`.
5. Open `http://127.0.0.1:5000`.

The database and enquiries table are created automatically in `travel.db`.

## Admin
Open `/admin/login`.
Default demo credentials:
- Username: `admin`
- Password: `ChangeMe123!`

Change these immediately using environment variables before deployment. Do not use the demo credentials on a public website.

## Deploy on Render
1. Push all project files to a GitHub repository.
2. Create a Render **Web Service** connected to that repository.
3. Build command: `pip install -r requirements.txt`
4. Start command: `gunicorn app:app`
5. Add environment variables: `SECRET_KEY`, `ADMIN_USERNAME`, `ADMIN_PASSWORD`.

**Important:** Render's local filesystem may be temporary on free services. This demo uses SQLite, so enquiries may be lost after redeploy/restart. For real client use, connect a managed PostgreSQL database and adapt the database layer. Add HTTPS, rate limiting, CSRF protection, backups and stronger access controls before collecting real customer information.

## Customise before showing a real agency
Replace the fictional brand name, phone/email/address, destination prices, package details and image URLs. Prices are sample display prices only and are not live offers. Confirm image licensing and availability before commercial use.
