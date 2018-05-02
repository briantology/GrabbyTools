import socket
import csv
import re
print("\nStarting GrabbyDNSChecker a tool by Brian Wcisel \n")

# Define Function to check if tuple value is empty or not.
def is_empty(tuple_value):
    if tuple_value:
        #print('Structure is not empty.')
        return False
    else:
        #print('Structure is empty.')
        return True

fqdnRE = re.compile(r'(.+)(,)(\s)(.+)')

# Open the file. Requires two columns, first column has FQDNs and second has IP addresses
inputfile = open('DNSInput.csv', 'rt')

# Create CSV Reader Object
reader = csv.reader(inputfile)
failfile = open('DNSMismatch.txt', 'w')

# Iterate over rows in reader
for row in reader:
    # Make row strings
    row = str(row)
    # Reset values
    resolved_ipaddr = "Unknown"
    resolved_hostname = "Unknown"

    # define local sets
    resolved_ipaddresses_set = set()
    resolved_hostnames_set = set()

    # Use Regex to parse row data
    if re.match(fqdnRE, row):
        # Store FQDN as variable stripping brackets, removing single quotes and forcing lowercase.
        fqdn = ((re.search(fqdnRE, row).group(1)).strip("[]'")).lower()
        # Store ip address as variable
        ipadd = ((re.search(fqdnRE, row).group(4)).strip("[]'")).lower()
        # Use built in Socket method to resolve fqdn
        try:
            resolved_ipaddr = socket.gethostbyname(fqdn)
        except:
            "There is no response for {}".format(fqdn)
        try:
            resolved_hostname = socket.gethostbyaddr(ipadd)
            # Split Tuple into three variables #tuple value 1 is the A Record first returned, tuple value 2 are any additional Aliases detected
            # tuple value 3 is IP Address
            recordA, aliasList, originalIP = resolved_hostname
            # Create a list of aliases to aliases to iterate over and document
            alias_list = []
            for i in aliasList:
                alias_list.append(i)
            originalIP = str(originalIP)
            originalIP = originalIP.strip("'[]")
            # Determine if there are aliases or duplicates returned with getipadrr, tuple 2 will be populated if so
            if is_empty(aliasList) is True:
                pass
            else:
                print("The following PTR records are resolving for {} when there should only be one - {}".format(ipadd, recordA))
                failfile.write("\nThe following PTR records are resolving for {} when there should only be one".format(ipadd))
                failfile.write("\n" + recordA)
                for i in alias_list:
                    print("-{}".format(i))
                    failfile.write("\n" + i)
        except:
            "There is no response for {}".format(ipadd)
        # Perform comparison
        try:
            if ipadd != resolved_ipaddr:
                print('\nDNS-A Record mismatch for {}, it returns {} when it should be {}'.format(fqdn, resolved_ipaddr, ipadd))
                failfile.write('\nDNS-A Record mismatch for {}, it returns {} when it should be {}'.format(fqdn, resolved_ipaddr, ipadd))
        except:
            pass

print("\nAll records, or, all remaining records are valid")