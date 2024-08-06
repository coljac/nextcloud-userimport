# Import Nextcloud users from a CSV file

Credit to [t-markmann](https://github.com/t-markmann/nc-userimporter) for inspiration.

Usage:

```
python3 nextcloud_user_importer.py --nc-url your-nextcloud-url.com --admin-name admin --admin-pass password --csv-file users.csv
```

For help:

```
python3 nextcloud_user_importer.py --help
```

```
usage: nextcloud_user_importer.py [-h] [--protocol PROTOCOL] --nc-url NC_URL --admin-name ADMIN_NAME --admin-pass ADMIN_PASS [--api-url API_URL] --csv-file CSV_FILE
                                  [--csv-delimiter CSV_DELIMITER] [--csv-delimiter-groups CSV_DELIMITER_GROUPS] [--generate-password] [--no-ssl-verify] [--language LANGUAGE]
                                  [--dry-run]

Nextcloud User Importer

optional arguments:
  -h, --help            show this help message and exit
  --protocol PROTOCOL   Protocol (http or https)
  --nc-url NC_URL       Nextcloud URL
  --admin-name ADMIN_NAME
                        Admin username
  --admin-pass ADMIN_PASS
                        Admin password
  --api-url API_URL     API URL
  --csv-file CSV_FILE   Path to CSV file
  --csv-delimiter CSV_DELIMITER
                        CSV delimiter
  --csv-delimiter-groups CSV_DELIMITER_GROUPS
                        CSV delimiter for groups
  --generate-password   Generate random passwords
  --no-ssl-verify       Disable SSL verification
  --language LANGUAGE   User language
  --dry-run             Perform a dry run without creating users

```

Your CSV file should look like this:
```
username,display_name,password,email,groups,quota
jdoe,John Doe,password123,jdoe@example.com,Users;Marketing,5 GB
asmith,Alice Smith,securepass,asmith@example.com,Users;Engineering,10 GB
```
