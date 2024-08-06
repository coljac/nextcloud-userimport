#!/usr/bin/env python3
import os
import sys
import csv
import html
import random
import string
import requests
import argparse
from tabulate import tabulate

def generate_password():
    return ''.join(random.choices(string.digits, k=10))

def create_user(config, user_data):
    url = f"{config.protocol}://{config.admin_name}:{config.admin_pass}@{config.nc_url}{config.api_url}"
    data = {
        'userid': user_data['username'],
        'displayName': user_data['display_name'],
        'password': user_data['password'],
        'email': user_data['email'],
        'quota': user_data['quota'],
        'language': config.language
    }
    for group in user_data['groups']:
        data[f'groups[]'] = group

    response = requests.post(url, headers={'OCS-APIRequest': 'true'}, data=data, verify=config.ssl_verify)
    return response

def main(args):
    users = []
    with open(args.csv_file, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=args.csv_delimiter)
        for row in reader:
            user = {
                'username': html.escape(row['username']),
                'display_name': html.escape(row['display_name']),
                'password': generate_password() if args.generate_password else html.escape(row['password']),
                'email': html.escape(row['email']),
                'groups': html.escape(row['groups']).split(args.csv_delimiter_groups),
                'quota': html.escape(row['quota'])
            }
            users.append(user)

    print(tabulate([[u['username'], u['display_name'], '*' * len(u['password']), u['email'], u['groups'], u['quota']] for u in users],
                   headers=['Username', 'Display Name', 'Password', 'Email', 'Groups', 'Quota']))

    if not args.dry_run:
        input("\nPress Enter to continue with user creation or Ctrl+C to abort...")

        for user in users:
            response = create_user(args, user)
            print(f"User {user['username']}: {response.status_code} - {response.text}")
    else:
        print("\nDry run completed. No users were created.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Nextcloud User Importer")
    parser.add_argument("--protocol", default="https", help="Protocol (http or https)")
    parser.add_argument("--nc-url", required=True, help="Nextcloud URL")
    parser.add_argument("--admin-name", required=True, help="Admin username")
    parser.add_argument("--admin-pass", required=True, help="Admin password")
    parser.add_argument("--api-url", default="/ocs/v1.php/cloud/users", help="API URL")
    parser.add_argument("--csv-file", required=True, help="Path to CSV file")
    parser.add_argument("--csv-delimiter", default=",", help="CSV delimiter")
    parser.add_argument("--csv-delimiter-groups", default=";", help="CSV delimiter for groups")
    parser.add_argument("--generate-password", action="store_true", help="Generate random passwords")
    parser.add_argument("--no-ssl-verify", action="store_false", dest="ssl_verify", help="Disable SSL verification")
    parser.add_argument("--language", default="en", help="User language")
    parser.add_argument("--dry-run", action="store_true", help="Perform a dry run without creating users")

    args = parser.parse_args()
    
    main(args)

