import csv
from uuid import UUID


class CSVContactsReader():

    def __init__(self, file_name):
        self.file_name = file_name
        self.all_contacts = {}  # {'site': {mail1, mail2, mail3}, }
        self.cleaned_contacts = {}  # {'site': {mail1, mail3}, }

    def read_contacts(self):
        """create self.all_contacts
        """
        with open(self.file_name) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                site = row['site']
                str_mails = row['mails']
                mails = str_mails.split('|')
                mails = [mail.lower() for mail in mails]
                self.all_contacts[site] = set(mails)

    def get_mails_with_site_domain(self, site, mails):
        mails_with_domain = set()
        for mail in mails:
            _, mail_domain = mail.split('@')
            if mail_domain in site:
                mails_with_domain.add(mail)
        return mails_with_domain

    def clean_mails(self, site, mails):
        valid_mails = set()
        for mail in mails:
            is_invalid_mail = False

            if mail.count('@') != 1:
                is_invalid_mail = True
            if mail[-1] == '.':
                is_invalid_mail = True

            mail_body, mail_domain = mail.split('@')

            # unsuported characters
            invalid_characters = """,[]{}()<>?"'`~&%$#!*+^_|\/="""
            for invalid_character in invalid_characters:
                if invalid_character in mail:
                    is_invalid_mail = True
                    break

            # invalid domain contains from digits
            mail_domain_splited = mail_domain.split('.')
            for domain_part in mail_domain_splited:
                try:
                    int(domain_part)
                    is_invalid_mail = True
                except ValueError:
                    pass

            # fake emails
            fake_words = ['example', '@email', '@mail', '@company', '@google.com', 'u00']
            for fake_word in fake_words:
                if fake_word in mail:
                    is_invalid_mail = True
                    break

            # validation uuid
            try:
                UUID(mail_body, version=4)
                is_invalid_mail = True
            except ValueError:
                pass

            if not is_invalid_mail:
                valid_mails.add(mail)

        if len(valid_mails) > 1:
            mails_with_site_domain = self.get_mails_with_site_domain(site, valid_mails)
            if len(mails_with_site_domain):
                valid_mails = mails_with_site_domain
        return valid_mails

    def clean_contacts(self):
        """create self.cleaned_contacts from self.all_contacts
        """
        assert self.all_contacts, "read_contacts() methond must be called first!"
        for site, mails in self.all_contacts.items():
            cleaned_mails = self.clean_mails(site, mails)
            if cleaned_mails:
                self.cleaned_contacts[site] = cleaned_mails

    def get_clean_contacts(self):
        self.read_contacts()
        self.clean_contacts()
        return self.cleaned_contacts


# p = CSVContactsReader('contacts_csv/02_10_17/contacts_total.csv')
# p.read_contacts()
# cs = p.get_clean_contacts()
# print(cs)

# total_mails_counter = 0
# for c in cs.values():
#     # print(list(c))
#     total_mails_counter += len(c)
# # print(cs['http://www.socialplex.com/'])
# print(total_mails_counter)
