import ConfigParser as cp
import requests
import argparse

#####################################
#       Turn on this to Debug       #
#####################################
# import logging
# import httplib

# # Debug logging
# httplib.HTTPConnection.debuglevel = 1
# logging.basicConfig()
# logging.getLogger().setLevel(logging.DEBUG)
# req_log = logging.getLogger('requests.packages.urllib3')
# req_log.setLevel(logging.DEBUG)
# req_log.propagate = True
#####################################
#                                   #
#####################################

description = ''

def args_handler():
    '''
    Function sets up arguments that the script accepts and describes them.
    :return: arguments as a parser object.
    '''
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-a', '--auth', help = 'Path to config file containing sapientia login details.', required=True)
    parser.add_argument('-i','--input', help='Path to file to be uploaded as a gene panel.', required=True)
    parser.add_argument('-pid','--project', help='Project to load the gene panel into.', required=True)
    return parser.parse_args()


def get_dancer_session_details(email, password):
    url = 'https://dev.sapientia.co.uk/login'
    values = {'email': email, 'password': password,}
    r = requests.post(url, data=values)
    dancer_cookie = r.cookies['dancer.session']
    print(r.cookies)
    print(r.content)
    print(r)
    return {'dancer.session': dancer_cookie}


def load_gene_panel_sapientia(project, filename, cookie):
    url = 'https://dev.sapientia.co.uk/project/{project_id}/gene-panel/add/upload/process'.format(project_id=project)
    print(cookie)
    files = {
        'gene_panel_file': open(filename, 'rb'),
    }

    values = {
        'csv_format': 'tsv',
    }

    response = requests.post(url, cookies=cookie,
                             files=files, data=values)

    save_url = response.url + '/save'
    second_response = requests.post(save_url, cookies=cookie)


def main():
    args = args_handler()
    config = cp.SafeConfigParser()
    config.read(args.auth)
    user_email = config.get('Auth', 'email')
    user_password = config.get('Auth', 'password')
    cookie = get_dancer_session_details(user_email, user_password)
    load_gene_panel_sapientia(args.project, args.input, cookie)


if __name__ == "__main__":
    main()